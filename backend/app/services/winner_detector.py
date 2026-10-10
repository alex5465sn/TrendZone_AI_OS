"""
TrendZone AI OS
================================

Winner Detector Service (Fase 3 do Product Hunter)

Responsável por identificar produtos vencedores
baseado em cliques + vendas reais.

Consolida dados de:
- PublishedPost (cliques por tracking code)
- Sale (vendas confirmadas)
- Product (dados do produto)

Calcula:
- Taxa de conversão (vendas / cliques)
- ROI estimado (comissão total / custo de aquisição)
- Momentum de vendas (últimas 24h vs. 7 dias)
- Recomendação de ação (DUPLICAR / OTIMIZAR / PAUSAR)
"""

from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.services.base_service import BaseService
from app.models.published_post import PublishedPost
from app.models.sale import Sale
from app.models.product import Product


class WinnerDetector(BaseService):
    """
    Motor de detecção de produtos vencedores.
    """

    SERVICE_NAME = "WINNER_DETECTOR"

    # =====================================================
    # THRESHOLDS
    # =====================================================

    MIN_CLICKS_FOR_ANALYSIS = 5  # Precisa de pelo menos 5 cliques
    MIN_CONVERSION_RATE = 0.05  # 5% de conversão é bom
    MIN_SALES_FOR_WINNER = 2  # Pelo menos 2 vendas confirmadas

    # =====================================================
    # ANÁLISE DE PRODUTO
    # =====================================================

    @classmethod
    def analyze_product(
        cls,
        db: Session,
        product_item_id: int,
        days_back: int = 7,
    ) -> Optional[dict]:
        """
        Analisa um produto específico e retorna:
        - cliques totais
        - vendas confirmadas
        - taxa de conversão
        - comissão total
        - momentum (últimas 24h vs. 7 dias)
        - recomendação de ação
        """

        cls.log_info(
            f"Analisando produto {product_item_id}..."
        )

        # Buscar produto
        product = db.query(Product).filter(
            Product.item_id == product_item_id
        ).first()

        if not product:
            cls.log_warning(
                f"Produto {product_item_id} não encontrado"
            )
            return None

        # Data de corte
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        cutoff_24h = datetime.utcnow() - timedelta(hours=24)

        # Cliques totais
        total_clicks = db.query(
            func.sum(PublishedPost.click_count)
        ).filter(
            and_(
                PublishedPost.product_item_id == product_item_id,
                PublishedPost.created_at >= cutoff_date,
            )
        ).scalar() or 0

        # Vendas totais
        total_sales = db.query(func.count(Sale.id)).filter(
            and_(
                Sale.product_item_id == product_item_id,
                Sale.created_at >= cutoff_date,
            )
        ).scalar() or 0

        # Vendas últimas 24h
        sales_24h = db.query(func.count(Sale.id)).filter(
            and_(
                Sale.product_item_id == product_item_id,
                Sale.created_at >= cutoff_24h,
            )
        ).scalar() or 0

        # Comissão total
        total_commission = db.query(
            func.sum(Sale.commission_value)
        ).filter(
            and_(
                Sale.product_item_id == product_item_id,
                Sale.created_at >= cutoff_date,
            )
        ).scalar() or 0.0

        # Taxa de conversão
        conversion_rate = (
            (total_sales / total_clicks * 100)
            if total_clicks > 0
            else 0.0
        )

        # Momentum (crescimento de vendas)
        momentum = (
            ((sales_24h / (total_sales / 7)) * 100 - 100)
            if total_sales > 0
            else 0.0
        )

        # Decisão
        decision = cls._decide_action(
            total_clicks,
            total_sales,
            conversion_rate,
            momentum,
        )

        result = {
            "product_item_id": product_item_id,
            "product_name": product.name,
            "product_image": product.image,
            "total_clicks": int(total_clicks),
            "total_sales": int(total_sales),
            "sales_24h": int(sales_24h),
            "conversion_rate": round(conversion_rate, 2),
            "total_commission": round(float(total_commission), 2),
            "momentum": round(momentum, 1),
            "decision": decision,
            "reason": cls._get_reason(
                total_clicks,
                total_sales,
                conversion_rate,
                momentum,
            ),
        }

        cls.log_success(
            f"Análise concluída: {decision}"
        )

        return result

    # =====================================================
    # RANKING DE VENCEDORES
    # =====================================================

    @classmethod
    def get_top_winners(
        cls,
        db: Session,
        limit: int = 10,
        days_back: int = 7,
    ) -> list[dict]:
        """
        Retorna os produtos vencedores ranqueados por:
        1. Vendas confirmadas
        2. Taxa de conversão
        3. Momentum
        """

        cls.log_info(
            f"Buscando top {limit} vencedores..."
        )

        cutoff_date = datetime.utcnow() - timedelta(days=days_back)

        # Query: produtos com vendas
        products_with_sales = db.query(
            Sale.product_item_id,
            func.count(Sale.id).label("sale_count"),
            func.sum(Sale.commission_value).label("total_commission"),
        ).filter(
            Sale.created_at >= cutoff_date
        ).group_by(
            Sale.product_item_id
        ).order_by(
            func.count(Sale.id).desc()
        ).limit(limit).all()

        winners = []
        for product_id, sale_count, commission in products_with_sales:
            analysis = cls.analyze_product(
                db,
                product_id,
                days_back,
            )
            if analysis:
                winners.append(analysis)

        cls.log_success(
            f"Encontrados {len(winners)} vencedores"
        )

        return winners

    # =====================================================
    # DECISÃO
    # =====================================================

    @classmethod
    def _decide_action(
        cls,
        clicks: int,
        sales: int,
        conversion_rate: float,
        momentum: float,
    ) -> str:
        """
        Decide a ação recomendada baseado em métricas.
        """

        # Sem dados suficientes
        if clicks < cls.MIN_CLICKS_FOR_ANALYSIS:
            return "OBSERVAR"

        # Vencedor claro
        if (
            sales >= cls.MIN_SALES_FOR_WINNER
            and conversion_rate >= cls.MIN_CONVERSION_RATE
            and momentum > 0
        ):
            return "DUPLICAR"

        # Bom desempenho mas pode melhorar
        if (
            sales >= cls.MIN_SALES_FOR_WINNER
            and conversion_rate >= (cls.MIN_CONVERSION_RATE * 0.5)
        ):
            return "OTIMIZAR"

        # Sem vendas ou taxa muito baixa
        if sales == 0 or conversion_rate < (cls.MIN_CONVERSION_RATE * 0.25):
            return "PAUSAR"

        # Padrão
        return "OBSERVAR"

    @classmethod
    def _get_reason(
        cls,
        clicks: int,
        sales: int,
        conversion_rate: float,
        momentum: float,
    ) -> str:
        """
        Retorna motivo legível da decisão.
        """

        if clicks < cls.MIN_CLICKS_FOR_ANALYSIS:
            return "Dados insuficientes para análise"

        if sales == 0:
            return "Nenhuma venda confirmada ainda"

        if conversion_rate >= cls.MIN_CONVERSION_RATE and momentum > 0:
            return f"Conversão forte ({conversion_rate:.1f}%) e momentum positivo (+{momentum:.0f}%)"

        if conversion_rate >= (cls.MIN_CONVERSION_RATE * 0.5):
            return f"Conversão aceitável ({conversion_rate:.1f}%), pode otimizar criativo"

        if momentum < -20:
            return f"Momentum negativo ({momentum:.0f}%), produto perdendo força"

        return f"{sales} venda(s) com {conversion_rate:.1f}% de conversão"
