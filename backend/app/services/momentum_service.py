"""
TrendZone AI OS

Momentum Service.

Coração do Product Radar: mede se um produto
está COMEÇANDO a ficar vencedor (momentum
positivo) ou saturando (momentum negativo).

Responsabilidades:

1. record()      — grava snapshot de produto com
                   deduplicação (nada mudou em menos
                   de 6h => nada é gravado).
2. momentum()    — compara estado atual com o
                   baseline (até 7 dias) e devolve
                   crescimento de vendas, variação de
                   preço e tendência.
3. radar()       — ranqueia produtos combinando
                   momentum (40%) + score interno
                   (25%) + aderência à faixa de preço
                   ideal R$20–100 (15%) + sinal do
                   Google Trends (20%), com motivos
                   legíveis para o card da UI.

Não decide (isso é do DecisionEngine) e não
substitui o Score — complementa com tempo.
"""

import re

from datetime import datetime, timedelta

from sqlalchemy import func, select

from sqlalchemy.orm import Session

from app.core.logger import logger

from app.models.product import Product

from app.models.product_snapshot import ProductSnapshot

from app.repositories.product_snapshot_repository import (
    ProductSnapshotRepository,
)


# Deduplicação: intervalo mínimo entre snapshots
# do mesmo produto (horas).
SNAPSHOT_MIN_INTERVAL_HOURS = 6

# Crescimento de vendas (fração) para considerar
# tendência de alta / baixa.
TREND_UP_THRESHOLD = 0.10

TREND_DOWN_THRESHOLD = -0.10

# Faixa de preço ideal (doc "Operação 1ª Venda"):
# baixa barreira psicológica de compra.
PRICE_BAND_MIN = 20.0

PRICE_BAND_MAX = 100.0

# Pesos do radar_score (0–100). O sinal do Google Trends
# (20%) entrou rebalanceando momentum/score/preço.
WEIGHT_MOMENTUM = 0.40

WEIGHT_SCORE = 0.25

WEIGHT_PRICE = 0.15

WEIGHT_TREND = 0.20

# Score do sinal de tendência do Google Trends (0–100).
# "unknown" (sem dados) é neutro — ausência de sinal não
# deve penalizar nem premiar o produto.
TREND_SIGNAL_SCORE = {
    "rising": 85.0,
    "stable": 50.0,
    "declining": 15.0,
}

TREND_SIGNAL_SCORE_DEFAULT = 50.0


class MomentumService:

    # =====================================================
    # SNAPSHOT (com deduplicação)
    # =====================================================

    @classmethod
    def record(
        cls,
        db: Session,
        product: Product,
    ) -> ProductSnapshot | None:
        """
        Grava um snapshot do produto se:
        - não houver snapshot recente (>= 6h), ou
        - algum valor comercial mudou desde o último.

        Nunca propaga exceção — snapshot é efeito
        colateral e não pode quebrar a operação
        que o chamou.
        """

        try:
            marketplace = (product.marketplace or "shopee").strip()

            item_id = int(product.item_id)

            latest = ProductSnapshotRepository.get_latest(
                db, marketplace, item_id
            )

            now = datetime.utcnow()

            if latest is not None:
                age_hours = (
                    now - latest.captured_at
                ).total_seconds() / 3600.0

                unchanged = (
                    abs(float(latest.price) - float(product.price)) < 0.005
                    and abs(float(latest.commission) - float(product.commission)) < 0.005
                    and abs(float(latest.rating) - float(product.rating)) < 0.005
                    and int(latest.sales) == int(product.sales)
                )

                if unchanged and age_hours < SNAPSHOT_MIN_INTERVAL_HOURS:
                    return None

            snapshot = ProductSnapshot(
                marketplace=marketplace,
                item_id=item_id,
                price=float(product.price),
                commission=float(product.commission),
                rating=float(product.rating),
                sales=int(product.sales),
                captured_at=now,
            )

            return ProductSnapshotRepository.create(db, snapshot)

        except Exception:
            logger.exception(
                "[MOMENTUM] Falha ao gravar snapshot do produto "
                f"{getattr(product, 'item_id', '?')} — ignorando."
            )

            return None

    # =====================================================
    # MOMENTUM DE UM PRODUTO
    # =====================================================

    @classmethod
    def momentum(
        cls,
        db: Session,
        marketplace: str,
        item_id: int,
        current_sales: int,
        current_price: float,
    ) -> dict:

        baseline = ProductSnapshotRepository.get_baseline(
            db, marketplace, item_id
        )

        if baseline is None:
            return {
                "has_baseline": False,
                "sales_growth_pct": None,
                "price_change_pct": None,
                "trend": "sem_base",
            }

        ref_sales = max(int(baseline.sales), 1)

        sales_growth = (int(current_sales) - int(baseline.sales)) / ref_sales

        ref_price = float(baseline.price)

        price_change = (
            (float(current_price) - ref_price) / ref_price
            if ref_price > 0
            else 0.0
        )

        if sales_growth >= TREND_UP_THRESHOLD:
            trend = "up"

        elif sales_growth <= TREND_DOWN_THRESHOLD:
            trend = "down"

        else:
            trend = "flat"

        return {
            "has_baseline": True,
            "baseline_at": baseline.captured_at.isoformat(),
            "sales_growth_pct": round(sales_growth * 100, 2),
            "price_change_pct": round(price_change * 100, 2),
            "trend": trend,
        }

    # =====================================================
    # PRODUCT RADAR
    # =====================================================

    @classmethod
    def radar(
        cls,
        db: Session,
        limit: int = 20,
    ) -> list[dict]:
        """
        Ranqueia produtos ativos por radar_score:

        50% momentum (crescimento de vendas desde o
        baseline, penalizando queda) + 25% score
        interno + 15% aderência à faixa de preço
        R$20–100 + 20% sinal do Google Trends
        (trend_signal via GoogleTrendsService, com
        cache de 1h e lote de até 5 keywords por
        requisição).

        Produtos sem baseline ainda aparecem (score +
        preço), mas atrás de quem tem momentum
        comprovado — exatamente o viés do documento:
        priorizar o que está COMEÇANDO a vencer.
        """

        products = (
            db.query(Product)
            .filter(Product.is_active.is_(True))
            .order_by(Product.score.desc())
            .limit(500)
            .all()
        )

        # Purga oportunista de snapshots antigos
        # (no máximo 1x por dia).
        cls._purge_once_per_day(db)

        # Bulk-load dos snapshots da janela (1 query):
        # baseline = snapshot mais antigo por produto na
        # janela de 7 dias com pelo menos 6h de idade.
        now = datetime.utcnow()

        window_start = now - timedelta(days=7)

        window_end = now - timedelta(hours=6)

        window_snaps = (
            db.query(ProductSnapshot)
            .filter(
                ProductSnapshot.captured_at >= window_start,
                ProductSnapshot.captured_at <= window_end,
            )
            .all()
        )

        baselines: dict[tuple[str, int], ProductSnapshot] = {}

        for s in window_snaps:
            key = (s.marketplace, s.item_id)

            current = baselines.get(key)

            if current is None or s.captured_at < current.captured_at:
                baselines[key] = s

        items: list[dict] = []

        for p in products:
            key = ((p.marketplace or "shopee").strip(), p.item_id)

            baseline = baselines.get(key)

            if baseline is None:
                m = {
                    "has_baseline": False,
                    "sales_growth_pct": None,
                    "price_change_pct": None,
                    "trend": "sem_base",
                }
            else:
                ref_sales = max(int(baseline.sales), 1)

                sales_growth = (int(p.sales) - int(baseline.sales)) / ref_sales

                ref_price = float(baseline.price)

                price_change = (
                    (float(p.price) - ref_price) / ref_price
                    if ref_price > 0
                    else 0.0
                )

                if sales_growth >= TREND_UP_THRESHOLD:
                    trend = "up"

                elif sales_growth <= TREND_DOWN_THRESHOLD:
                    trend = "down"

                else:
                    trend = "flat"

                m = {
                    "has_baseline": True,
                    "baseline_at": baseline.captured_at.isoformat(),
                    "sales_growth_pct": round(sales_growth * 100, 2),
                    "price_change_pct": round(price_change * 100, 2),
                    "trend": trend,
                }

            momentum_component = 0.0

            if m["has_baseline"]:
                growth = m["sales_growth_pct"] / 100.0

                # +50% de vendas => 100 pts. Quedas ficam negativas.
                momentum_component = growth * 200.0

                momentum_component = max(-100.0, min(100.0, momentum_component))

            score_component = max(0.0, min(100.0, float(p.score or 0)))

            price_component = cls._price_band_fit(float(p.price))

            radar_score = round(
                max(
                    0.0,
                    min(
                        100.0,
                        WEIGHT_MOMENTUM * momentum_component
                        + WEIGHT_SCORE * score_component
                        + WEIGHT_PRICE * price_component
                        + WEIGHT_TREND * TREND_SIGNAL_SCORE_DEFAULT,
                    ),
                ),
                2,
            )

            reasons = cls._build_reasons(
                m,
                float(p.price),
                float(p.score or 0),
            )

            items.append(
                {
                    "id": p.id,
                    "name": p.name,
                    "image": p.image,
                    "price": float(p.price),
                    "commission": round(float(p.commission) * 100, 2),
                    "rating": p.rating,
                    "sales": p.sales,
                    "score": p.score,
                    "recommendation": p.recommendation,
                    "offer_link": p.offer_link,
                    "marketplace": p.marketplace,
                    "momentum_pct": m["sales_growth_pct"],
                    "price_change_pct": m["price_change_pct"],
                    "trend": m["trend"],
                    "trend_signal": None,
                    "radar_score": radar_score,
                    "reasons": reasons,
                }
            )

        # Sinal do Google Trends (20% do radar_score): busca em
        # lote apenas para os itens retornados, com keyword curta
        # (nomes longos de marketplace não retornam dados). A
        # busca é bloqueante, mas roda na threadpool do FastAPI e
        # o cache de 1h do GoogleTrendsService evita refetch.
        cls._apply_trend_signal(items[:limit])

        items.sort(key=lambda x: x["radar_score"], reverse=True)

        return items[:limit]

    # =====================================================
    # HELPERS
    # =====================================================

    @classmethod
    def _apply_trend_signal(cls, items: list[dict]) -> None:
        """
        Busca o sinal do Google Trends para os itens do radar e
        aplica ao radar_score (peso WEIGHT_TREND). Nunca propaga
        exceção — falha de trends degrada para sinal neutro.
        """
        if not items:
            return

        from app.services.google_trends_service import GoogleTrendsService

        keywords = {
            item["id"]: cls._trend_keyword(item["name"]) for item in items
        }

        unique_keywords = sorted({kw for kw in keywords.values() if kw})

        if not unique_keywords:
            return

        try:
            signals = GoogleTrendsService.get_trend_signal_sync(unique_keywords)
        except Exception:
            logger.exception(
                "[MOMENTUM] Falha ao buscar sinal do Google Trends — "
                "radar segue com sinal neutro."
            )

            return

        for item in items:
            signal = signals.get(keywords.get(item["id"]) or "")

            if not signal:
                continue

            item["trend_signal"] = signal

            trend_component = TREND_SIGNAL_SCORE.get(
                signal, TREND_SIGNAL_SCORE_DEFAULT
            )

            base_without_trend = item["radar_score"] - (
                WEIGHT_TREND * TREND_SIGNAL_SCORE_DEFAULT
            )

            item["radar_score"] = round(
                max(
                    0.0,
                    min(
                        100.0,
                        base_without_trend + WEIGHT_TREND * trend_component,
                    ),
                ),
                2,
            )

            if signal == "rising":
                item["reasons"].insert(0, "Em alta no Google Trends")

            elif signal == "declining":
                item["reasons"].append("Perdendo busca no Google Trends")

    @staticmethod
    def _trend_keyword(name: str) -> str:
        """
        Reduz um nome longo de produto a uma keyword curta
        (3 primeiras palavras, sem pontuação) — nomes completos
        de marketplace não retornam dados no Google Trends.
        """
        words = re.sub(r"[^\w\s]", " ", (name or "")).split()

        return " ".join(words[:3]).strip().lower()

    @staticmethod
    def _price_band_fit(price: float) -> float:
        """
        Aderência à faixa de preço ideal (0–100).
        """

        if PRICE_BAND_MIN <= price <= PRICE_BAND_MAX:
            return 100.0

        if 10.0 <= price < PRICE_BAND_MIN or PRICE_BAND_MAX < price <= 200.0:
            return 60.0

        return 30.0

    @staticmethod
    def _build_reasons(
        momentum: dict,
        price: float,
        score: float,
    ) -> list[str]:

        reasons: list[str] = []

        if momentum["has_baseline"]:
            growth = momentum["sales_growth_pct"]

            if growth >= 10:
                reasons.append(
                    f"+{growth:.0f}% de vendas desde o último acompanhamento"
                )

            elif growth <= -10:
                reasons.append(
                    f"Vendas em queda ({growth:.0f}%) — atenção à saturação"
                )

            price_change = momentum["price_change_pct"]

            if price_change <= -3:
                reasons.append("Preço caiu — boa janela de oferta")

        if PRICE_BAND_MIN <= price <= PRICE_BAND_MAX:
            reasons.append("Preço na faixa ideal de conversão (R$ 20–100)")

        if score >= 80:
            reasons.append(f"Score interno alto ({score:.0f})")

        if not reasons:
            reasons.append("Aguardando mais histórico para calcular momentum")

        return reasons

    _last_purge_at: datetime | None = None

    @classmethod
    def _purge_once_per_day(cls, db: Session) -> None:
        now = datetime.utcnow()

        if (
            cls._last_purge_at is not None
            and (now - cls._last_purge_at).total_seconds() < 86400
        ):
            return

        try:
            removed = ProductSnapshotRepository.purge_old(db)

            cls._last_purge_at = now

            if removed:
                logger.info(
                    "[MOMENTUM] Purga de snapshots: "
                    f"{removed} linha(s) removida(s)."
                )

        except Exception:
            logger.exception("[MOMENTUM] Falha ao purgar snapshots antigos.")
