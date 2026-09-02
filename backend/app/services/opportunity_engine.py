"""
TrendZone AI OS
================================

Opportunity Engine

Motor de Oportunidades de Venda.

Combina Ranking + Decisão + Geração de
Conteúdo para apontar quais produtos têm
maior potencial de venda agora, já com
material de divulgação pronto para revisão
humana.

Não publica, não envia mensagens e não
acessa grupos/redes de terceiros.
"""

from typing import List

from app.core.constants import Decision
from app.services.base_service import BaseService
from app.services.ranking_engine import RankingEngine
from app.services.decision_engine import DecisionEngine
from app.services.content_generator_service import ContentGeneratorService


class OpportunityEngine(BaseService):
    """
    Motor oficial de Oportunidades
    do TrendZone AI OS.
    """

    SERVICE_NAME = "OPPORTUNITY_ENGINE"

    _ELIGIBLE_DECISIONS = {
        Decision.PROMOTE.value,
        Decision.TEST.value,
    }

    # =====================================================
    # OPORTUNIDADES
    # =====================================================

    @classmethod
    def find(
        cls,
        products: List[dict],
        limit: int = 10,
    ) -> List[dict]:

        cls.log_info(
            "Buscando oportunidades de venda..."
        )

        ranked = RankingEngine.rank(products)

        opportunities = []

        for product in ranked:

            try:
                decision = DecisionEngine.classify(product)
            except Exception:
                continue

            if decision not in cls._ELIGIBLE_DECISIONS:
                continue

            content = ContentGeneratorService.generate(product)

            opportunities.append(
                {
                    "product": product,
                    "decision": decision,
                    "content": content,
                }
            )

            if len(opportunities) >= limit:
                break

        cls.log_success(
            f"{len(opportunities)} oportunidade(s) encontrada(s)."
        )

        return opportunities
