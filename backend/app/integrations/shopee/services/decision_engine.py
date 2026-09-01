"""
TrendZone AI OS
================================

Decision Engine V2

Responsável por tomar decisões
estratégicas sobre produtos.

Utiliza Score e regras de negócio.
"""

from app.core.constants import Decision

from app.services.base_service import BaseService


class DecisionEngine(BaseService):

    SERVICE_NAME = "DECISION_ENGINE"

    PROMOTE_SCORE = 80

    TEST_SCORE = 60

    OBSERVE_SCORE = 40

    MIN_RATING = 4.5

    MIN_COMMISSION = 8

    MIN_SALES = 500

    MAX_PRICE = 500

    @classmethod
    def classify(cls, product: dict):

        cls.log_info("Analisando produto...")

        score = product["score"]

        if cls._can_promote(product):

            decision = Decision.PROMOTE.value

        elif score >= cls.TEST_SCORE:

            decision = Decision.TEST.value

        elif score >= cls.OBSERVE_SCORE:

            decision = Decision.OBSERVE.value

        else:

            decision = Decision.DISCARD.value

        cls.log_success(

            f"Decisão: {decision}"

        )

        return decision

    # =====================================================
    # REGRAS
    # =====================================================

    @classmethod
    def _can_promote(cls, product):

        if product["score"] < cls.PROMOTE_SCORE:

            return False

        if product["commission"] < cls.MIN_COMMISSION:

            return False

        if product["rating"] < cls.MIN_RATING:

            return False

        if product["sales"] < cls.MIN_SALES:

            return False

        if product["price"] > cls.MAX_PRICE:

            return False

        return True