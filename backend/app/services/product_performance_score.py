"""
TrendZone AI OS
================================

Product Performance Score Service.

Fecha o loop de dados do Scout: em vez de confiar apenas no
Score heuristico (comissao + avaliacao + vendas reportadas pelo
marketplace), este servico observa o que REALMENTE converteu nos
canais rastreados (Canais & SubIDs) e ajusta o Score dos produtos
para cima ou para baixo com base na performance real.

Nao substitui o ProductScore (que continua calculando o Score
heuristico de produtos novos, sem historico ainda). Este servico
roda periodicamente e aplica um ajuste (bonus/penalidade) sobre o
"base_score", gerando o "score" final usado em toda a plataforma.
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.database.session import SessionLocal
from app.models.channel_tracking import ChannelTracking
from app.models.product import Product
from app.models.sale import Sale
from app.services.base_service import BaseService
from app.services.decision_engine import DecisionEngine


class ProductPerformanceScore(BaseService):
    """
    Motor de reponderacao do Score com base em performance real.
    """

    SERVICE_NAME = "PRODUCT_PERFORMANCE_SCORE"

    # Cliques minimos para o produto ter "voz" no ajuste. Abaixo
    # disso a amostra e pequena demais para confiar na taxa.
    MIN_CLICKS_FOR_SIGNAL = 15

    # Quanto o ajuste pode empurrar o score para cima/baixo.
    MAX_ADJUSTMENT = 15.0

    # Escala de sensibilidade do ajuste em relacao ao desvio da
    # taxa de conversao do produto frente a media da plataforma.
    ADJUSTMENT_SCALE = 40.0

    # Vendas reais confirmadas pela Shopee sao um sinal muito mais
    # forte que um simples clique rastreado internamente: cada venda
    # confirmada soma um bonus direto ao score, independente de ter
    # ou nao volume de cliques suficiente para o ajuste por taxa.
    REAL_SALE_BONUS = 3.0
    REAL_SALE_MAX_BONUS = 20.0

    @classmethod
    def recalculate_all(cls, db: Session) -> dict:
        """
        Recalcula o ajuste de performance de todos os produtos com
        dados suficientes em Canais & SubIDs e/ou vendas reais
        confirmadas na Shopee, e atualiza score/recommendation
        em "products".
        """

        cls.log_info("Recalculando Score com base em performance real...")

        rows = (
            db.query(
                ChannelTracking.product_id,
                func.sum(ChannelTracking.clicks).label("clicks"),
                func.sum(ChannelTracking.conversions).label("conversions"),
            )
            .filter(
                ChannelTracking.product_id.isnot(None),
                ChannelTracking.is_active == True,  # noqa: E712
            )
            .group_by(ChannelTracking.product_id)
            .having(func.sum(ChannelTracking.clicks) >= cls.MIN_CLICKS_FOR_SIGNAL)
            .all()
        )

        baseline = cls._baseline_conversion_rate(rows) if rows else 0.0

        click_adjustments = {
            row.product_id: cls._adjustment(row.conversions / row.clicks, baseline)
            for row in rows
        }
        sales_adjustments = cls._real_sales_adjustment(db)

        product_ids = set(click_adjustments) | set(sales_adjustments)

        if not product_ids:
            cls.log_info("Sem dados suficientes de cliques ou vendas reais ainda. Nada a ajustar.")
            return {
                "products_analyzed": 0,
                "products_boosted": 0,
                "products_penalized": 0,
                "products_with_real_sales": 0,
            }

        boosted = 0
        penalized = 0

        for product_id in product_ids:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                continue

            adjustment = round(
                click_adjustments.get(product_id, 0.0)
                + sales_adjustments.get(product_id, 0.0),
                2,
            )

            product.performance_adjustment = adjustment
            product.score = round((product.base_score or 0.0) + adjustment, 2)
            product.recommendation = DecisionEngine.classify({"score": product.score})

            if adjustment > 0:
                boosted += 1
            elif adjustment < 0:
                penalized += 1

        db.commit()

        summary = {
            "products_analyzed": len(product_ids),
            "products_boosted": boosted,
            "products_penalized": penalized,
            "products_with_real_sales": len(sales_adjustments),
        }

        cls.log_success(
            "Score reponderado: "
            f"{summary['products_analyzed']} produtos analisados, "
            f"{summary['products_boosted']} valorizados, "
            f"{summary['products_penalized']} penalizados, "
            f"{summary['products_with_real_sales']} com vendas reais confirmadas."
        )

        return summary

    @classmethod
    def _real_sales_adjustment(cls, db: Session) -> dict[int, float]:
        """
        Bonus de score por vendas reais confirmadas na Shopee,
        por produto (quando a venda pode ser atribuida a um
        produto conhecido via subId/utm_content).
        """
        rows = (
            db.query(
                Sale.product_id,
                func.count(Sale.id).label("confirmed_sales"),
            )
            .filter(
                Sale.product_id.isnot(None),
                Sale.status == "confirmada",
                Sale.is_active == True,  # noqa: E712
            )
            .group_by(Sale.product_id)
            .all()
        )

        return {
            row.product_id: round(
                min(row.confirmed_sales * cls.REAL_SALE_BONUS, cls.REAL_SALE_MAX_BONUS),
                2,
            )
            for row in rows
        }

    @classmethod
    def _baseline_conversion_rate(cls, rows) -> float:
        total_clicks = sum(r.clicks for r in rows)
        total_conversions = sum(r.conversions for r in rows)
        if total_clicks <= 0:
            return 0.0
        return total_conversions / total_clicks

    @classmethod
    def _adjustment(cls, conversion_rate: float, baseline: float) -> float:
        if baseline <= 0:
            return 0.0

        relative_deviation = (conversion_rate - baseline) / baseline

        adjustment = relative_deviation * cls.ADJUSTMENT_SCALE

        return round(
            max(-cls.MAX_ADJUSTMENT, min(cls.MAX_ADJUSTMENT, adjustment)),
            2,
        )


def run_performance_recalculation() -> dict:
    """
    Ponto de entrada usado pelo FacebookSchedulerService para rodar
    a reponderacao periodicamente, sem exigir cron/APScheduler.
    """

    db = SessionLocal()
    try:
        return ProductPerformanceScore.recalculate_all(db)
    except Exception as e:
        logger.warning(f"[PRODUCT_PERFORMANCE_SCORE] Erro ao recalcular: {e}")
        return {"error": str(e)}
    finally:
        db.close()
