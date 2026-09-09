"""
TrendZone AI OS — Commercial Intelligence Engine (TCIE)
========================================================

Opportunity Engine: recebe dados brutos de um produto (do Scout,
de qualquer marketplace) e devolve o Product Opportunity Score.
"""

from app.commercial_intelligence.domain.product_scoring import (
    OpportunitySignals,
    OpportunityResult,
    calculate_opportunity_score,
)


def estimate_signals_from_product(product: dict) -> OpportunitySignals:
    """
    Traduz um produto (formato já usado pelo Scout: sales, rating,
    commissionRate/commission, priceDiscountRate) em sinais 0-100
    para o Opportunity Score.

    Isso é uma estimativa inicial simples (heurística), pensada para
    já funcionar com os dados que o TrendZone coleta hoje da Shopee.
    Pode ser refinada por marketplace através dos Adapters.
    """

    sales = float(product.get("sales") or 0)
    rating = float(product.get("rating") or product.get("ratingStar") or 0)
    commission = float(product.get("commission") or product.get("commissionRate") or 0)
    discount = float(product.get("priceDiscountRate") or 0)

    demand = min(sales / 10, 100)
    trend = min(discount * 1.2, 100)
    competition_free_space = max(100 - min(sales / 20, 100), 20)
    margin_potential = min(commission * 100 * 3, 100)
    ticket = min(float(product.get("price") or 0) / 2, 100)
    saturation_free_space = max(100 - min(sales / 15, 100), 15)
    differentiation = min(rating / 5 * 100, 100)
    kit_potential = 60.0
    content_potential = min(rating / 5 * 100, 100)

    return OpportunitySignals(
        demand=demand,
        trend=trend,
        competition=competition_free_space,
        margin_potential=margin_potential,
        ticket=ticket,
        saturation=saturation_free_space,
        differentiation=differentiation,
        kit_potential=kit_potential,
        content_potential=content_potential,
    )


def evaluate_opportunity(product: dict, signals: OpportunitySignals | None = None) -> OpportunityResult:
    """Calcula o Opportunity Score de um produto."""

    resolved_signals = signals or estimate_signals_from_product(product)
    return calculate_opportunity_score(resolved_signals)
