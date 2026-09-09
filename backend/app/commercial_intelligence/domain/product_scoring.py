"""
TrendZone AI OS — Commercial Intelligence Engine (TCIE)
========================================================

Domínio: Product Opportunity Score.

Calcula o "Product Opportunity Score" de um produto a partir
de sinais de demanda, tendência, concorrência, margem, ticket,
saturação, diferenciação e potencial de kit/conteúdo.

Este módulo não conhece marketplace nenhum: recebe apenas
sinais numéricos normalizados (0-100) e devolve o score final.
Quem traduz dados brutos da Shopee/Mercado Livre/Amazon para
esses sinais são os Adapters (app/commercial_intelligence/adapters).
"""

from dataclasses import dataclass, field


@dataclass
class OpportunitySignals:
    demand: float = 0.0
    trend: float = 0.0
    competition: float = 0.0
    margin_potential: float = 0.0
    ticket: float = 0.0
    saturation: float = 0.0
    differentiation: float = 0.0
    kit_potential: float = 0.0
    content_potential: float = 0.0


@dataclass
class OpportunityResult:
    score: float
    status: str
    breakdown: dict = field(default_factory=dict)


WEIGHTS = {
    "demand": 0.18,
    "trend": 0.15,
    "competition": 0.10,
    "margin_potential": 0.20,
    "ticket": 0.08,
    "saturation": 0.09,
    "differentiation": 0.10,
    "kit_potential": 0.05,
    "content_potential": 0.05,
}


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def calculate_opportunity_score(signals: OpportunitySignals) -> OpportunityResult:
    """
    Calcula o Product Opportunity Score (0-100).

    'competition' e 'saturation' são sinais invertidos: quanto MAIOR
    o valor recebido, MENOR a concorrência/saturação real — ou seja,
    o chamador já deve enviar o sinal como "espaço livre no mercado"
    (100 = mercado livre, 0 = mercado saturado/dominado).
    """

    breakdown = {}
    total = 0.0

    for field_name, weight in WEIGHTS.items():
        value = _clamp(getattr(signals, field_name))
        contribution = value * weight
        breakdown[field_name] = {
            "value": round(value, 1),
            "weight": weight,
            "contribution": round(contribution, 2),
        }
        total += contribution

    score = round(_clamp(total), 1)
    status = classify_status(score)

    return OpportunityResult(score=score, status=status, breakdown=breakdown)


def classify_status(score: float) -> str:
    if score >= 80:
        return "ESCALAR"
    if score >= 65:
        return "TESTAR"
    if score >= 45:
        return "AJUSTAR"
    return "MATAR"
