"""
TrendZone AI OS — Commercial Intelligence Engine (TCIE) v1.0 (fase 1)
=======================================================================

Endpoints iniciais do motor de inteligência comercial:
- /commercial-intelligence/opportunity-score
- /commercial-intelligence/profit
- /commercial-intelligence/analyze (combina os dois + decisão)

Fases seguintes (não implementadas ainda): Market Position Engine,
Offer Engine, Listing Conversion Engine, Test Engine, Scale Engine,
Adapters por marketplace.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_current_user
from app.models.user import User
from app.api.response import ResponseBuilder

from app.commercial_intelligence.engines.opportunity_engine import evaluate_opportunity
from app.commercial_intelligence.engines.profit_engine import evaluate_profit

router = APIRouter(
    prefix="/commercial-intelligence",
    tags=["Commercial Intelligence Engine"],
)


class ProductPayload(BaseModel):
    price: float = 0
    sales: int = 0
    rating: float = 0
    commission: float = 0
    priceDiscountRate: float = 0
    productName: str = ""


class ProfitOverrides(BaseModel):
    sale_price: float | None = None
    product_cost: float | None = None
    commission_rate: float | None = None
    fees: float | None = None
    shipping_cost: float | None = None
    packaging_cost: float | None = None
    tax_rate: float | None = None
    ads_cost: float | None = None
    estimated_returns_rate: float | None = None
    operational_cost: float | None = None


class AnalyzeRequest(BaseModel):
    product: ProductPayload
    costs: ProfitOverrides | None = None


@router.post("/opportunity-score")
def opportunity_score(payload: ProductPayload, current_user: User = Depends(get_current_user)):
    result = evaluate_opportunity(payload.model_dump())
    return ResponseBuilder.success(data={
        "score": result.score,
        "status": result.status,
        "breakdown": result.breakdown,
    })


@router.post("/profit")
def profit(
    product: ProductPayload,
    costs: ProfitOverrides | None = None,
    current_user: User = Depends(get_current_user),
):
    overrides = costs.model_dump(exclude_none=True) if costs else {}
    result = evaluate_profit(product.model_dump(), overrides)
    return ResponseBuilder.success(data=result.__dict__)


@router.post("/analyze")
def analyze(payload: AnalyzeRequest, current_user: User = Depends(get_current_user)):
    """
    Decision Engine (fase 1): combina Opportunity Score + Profit Engine
    em uma decisão única: MATAR / AJUSTAR / TESTAR / ESCALAR.
    """

    product_dict = payload.product.model_dump()
    overrides = payload.costs.model_dump(exclude_none=True) if payload.costs else {}

    opportunity = evaluate_opportunity(product_dict)
    profit_result = evaluate_profit(product_dict, overrides)

    decision = opportunity.status
    if profit_result.net_margin_pct < 5 and decision in ("ESCALAR", "TESTAR"):
        decision = "AJUSTAR"
    if profit_result.net_profit <= 0:
        decision = "MATAR"

    return ResponseBuilder.success(data={
        "decision": decision,
        "opportunity": {
            "score": opportunity.score,
            "status": opportunity.status,
            "breakdown": opportunity.breakdown,
        },
        "profit": profit_result.__dict__,
        "reasoning": {
            "demand": opportunity.breakdown["demand"]["value"],
            "margin": opportunity.breakdown["margin_potential"]["value"],
            "competition_free_space": opportunity.breakdown["competition"]["value"],
            "net_margin_pct": profit_result.net_margin_pct,
            "net_profit": profit_result.net_profit,
        },
    })
