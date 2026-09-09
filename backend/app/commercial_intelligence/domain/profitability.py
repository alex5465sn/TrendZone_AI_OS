"""
TrendZone AI OS — Commercial Intelligence Engine (TCIE)
========================================================

Domínio: Profitability (lucro real).

"Não basta descobrir que um produto vende. É preciso descobrir
quanto realmente sobra." Este módulo calcula o lucro líquido real
de um produto, descontando todos os custos — não apenas o preço
de venda menos o custo do produto.
"""

from dataclasses import dataclass


@dataclass
class CostBreakdown:
    sale_price: float
    product_cost: float = 0.0
    commission_rate: float = 0.0
    fees: float = 0.0
    shipping_cost: float = 0.0
    packaging_cost: float = 0.0
    tax_rate: float = 0.0
    ads_cost: float = 0.0
    estimated_returns_rate: float = 0.0
    operational_cost: float = 0.0


@dataclass
class ProfitResult:
    net_profit: float
    net_margin_pct: float
    roi_pct: float
    breakeven_roas: float
    max_cac: float
    min_viable_price: float
    ideal_price: float


def calculate_profit(costs: CostBreakdown) -> ProfitResult:

    commission_value = costs.sale_price * costs.commission_rate
    tax_value = costs.sale_price * costs.tax_rate
    returns_value = costs.sale_price * costs.estimated_returns_rate

    total_costs = (
        costs.product_cost
        + commission_value
        + costs.fees
        + costs.shipping_cost
        + costs.packaging_cost
        + tax_value
        + costs.ads_cost
        + returns_value
        + costs.operational_cost
    )

    net_profit = round(costs.sale_price - total_costs, 2)

    net_margin_pct = round(
        (net_profit / costs.sale_price * 100) if costs.sale_price else 0.0, 2
    )

    invested = total_costs - costs.ads_cost
    roi_pct = round((net_profit / invested * 100) if invested > 0 else 0.0, 2)

    fixed_costs_no_ads = total_costs - costs.ads_cost
    breakeven_roas = round(
        (costs.sale_price / (costs.sale_price - fixed_costs_no_ads))
        if (costs.sale_price - fixed_costs_no_ads) > 0
        else 0.0,
        2,
    )

    max_cac = round(max(net_profit + costs.ads_cost, 0.0), 2)

    min_viable_price = round(total_costs, 2)
    ideal_price = round(total_costs * 1.35, 2)

    return ProfitResult(
        net_profit=net_profit,
        net_margin_pct=net_margin_pct,
        roi_pct=roi_pct,
        breakeven_roas=breakeven_roas,
        max_cac=max_cac,
        min_viable_price=min_viable_price,
        ideal_price=ideal_price,
    )
