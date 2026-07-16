"""
TrendZone AI OS
================================

Decision Engine.

Responsável pela decisão estratégica
de cada produto.

Não calcula Score.

Não gera relatórios.

Não salva no banco.

Sua única responsabilidade é
classificar o produto conforme
as regras de negócio.
"""

from app.core.constants import (
    Decision,
    MIN_SCORE_OBSERVE,
    MIN_SCORE_TEST,
    MIN_SCORE_PROMOTE,
)

from app.core.exceptions import DecisionException

from app.services.base_service import BaseService


class DecisionEngine(BaseService):
    """
    Motor oficial de decisões do
    TrendZone AI OS.
    """

    SERVICE_NAME = "DECISION_ENGINE"

    @classmethod
    def classify(
        cls,
        product: dict,
    ) -> str:

        cls.log_info(
            "Analisando decisão..."
        )

        if "score" not in product:

            cls.log_error(
                "Produto sem Score."
            )

            raise DecisionException(
                "Produto não possui Score."
            )

        score = product["score"]

        decision = cls._decision_by_score(
            score
        )

        cls.log_success(
            f"Decisão: {decision}"
        )

        return decision

    # =====================================================
    # REGRAS
    # =====================================================

    @classmethod
    def _decision_by_score(
        cls,
        score: float,
    ) -> str:

        if score >= MIN_SCORE_PROMOTE:

            return Decision.PROMOTE.value

        if score >= MIN_SCORE_TEST:

            return Decision.TEST.value

        if score >= MIN_SCORE_OBSERVE:

            return Decision.OBSERVE.value

        return Decision.DISCARD.value