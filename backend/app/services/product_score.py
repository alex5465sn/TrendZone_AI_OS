"""
TrendZone AI OS
================================

Product Score Service.

Responsável pelo cálculo do Score
dos produtos.

Não decide.

Não salva.

Não gera relatórios.

Sua única responsabilidade é calcular
o Score do produto.
"""

from app.services.base_service import BaseService


class ProductScore(BaseService):
    """
    Motor de Score do TrendZone AI OS.
    """

    SERVICE_NAME = "PRODUCT_SCORE"

    # =====================================================
    # PESOS
    # =====================================================

    COMMISSION_WEIGHT = 0.50

    RATING_WEIGHT = 10

    SALES_DIVISOR = 1000

    SALES_LIMIT = 100

    # =====================================================
    # SCORE
    # =====================================================

    @classmethod
    def calculate(
        cls,
        *,
        commission: float,
        rating: float,
        sales: int,
    ) -> float:

        cls.log_info(
            "Calculando Score..."
        )

        commission_score = cls._commission_score(
            commission
        )

        rating_score = cls._rating_score(
            rating
        )

        sales_score = cls._sales_score(
            sales
        )

        final_score = (

            commission_score

            + rating_score

            + sales_score

        )

        final_score = round(
            final_score,
            2,
        )

        cls.log_success(
            f"Score calculado: {final_score}"
        )

        return final_score

    # =====================================================
    # COMISSÃO
    # =====================================================

    @classmethod
    def _commission_score(
        cls,
        commission: float,
    ) -> float:

        return commission * cls.COMMISSION_WEIGHT

    # =====================================================
    # RATING
    # =====================================================

    @classmethod
    def _rating_score(
        cls,
        rating: float,
    ) -> float:

        return rating * cls.RATING_WEIGHT

    # =====================================================
    # SALES
    # =====================================================

    @classmethod
    def _sales_score(
        cls,
        sales: int,
    ) -> float:

        return min(

            sales / cls.SALES_DIVISOR,

            cls.SALES_LIMIT,

        )