"""
TrendZone AI OS — Commercial Intelligence Engine (TCIE)
========================================================

Profit Engine: calcula o lucro real de um produto a partir dos
custos informados (ou estimados a partir do que o Scout já sabe).
"""

from app.commercial_intelligence.domain.profitability import (
    CostBreakdown,
    ProfitResult,
    calculate_profit,
)

# Taxa fixa cobrada pela Shopee por item vendido (modelo oficial de
# vendedor: 14% + R$4 sem Frete Grátis, ou 20% + R$4 aderindo ao
# programa). Só se aplica a quem vende como lojista/dropshipper na
# própria Shopee (ex.: estratégia Kaiross) - não afeta o cálculo de
# comissão de afiliado, que já vem do campo `commission` do produto.
SHOPEE_FIXED_FEE_PER_ITEM = 4.0


def build_costs_from_product(product: dict, overrides: dict | None = None) -> CostBreakdown:
    """
    Monta o CostBreakdown a partir dos dados do produto (Scout) mais
    quaisquer overrides manuais informados pelo usuário (custo do
    produto, frete real, Ads, etc. — dados que a plataforma ainda
    não sabe automaticamente).
    """

    overrides = overrides or {}

    sale_price = float(overrides.get("sale_price") or product.get("price") or 0)
    commission_rate = float(
        overrides.get("commission_rate")
        or product.get("commission")
        or product.get("commissionRate")
        or 0
    )

    return CostBreakdown(
        sale_price=sale_price,
        product_cost=float(overrides.get("product_cost") or 0),
        commission_rate=commission_rate,
        fees=float(overrides.get("fees") or 0),
        shipping_cost=float(overrides.get("shipping_cost") or 0),
        packaging_cost=float(overrides.get("packaging_cost") or 0),
        tax_rate=float(overrides.get("tax_rate") or 0),
        ads_cost=float(overrides.get("ads_cost") or 0),
        estimated_returns_rate=float(overrides.get("estimated_returns_rate") or 0.02),
        operational_cost=float(overrides.get("operational_cost") or 0),
        shopee_fixed_fee=float(
            overrides.get("shopee_fixed_fee")
            if overrides.get("shopee_fixed_fee") is not None
            else (SHOPEE_FIXED_FEE_PER_ITEM if overrides.get("is_shopee_seller") else 0.0)
        ),
    )


def evaluate_profit(product: dict, overrides: dict | None = None) -> ProfitResult:
    costs = build_costs_from_product(product, overrides)
    return calculate_profit(costs)
