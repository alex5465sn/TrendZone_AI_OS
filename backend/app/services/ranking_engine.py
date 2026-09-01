"""
TrendZone AI OS
================================

Ranking Engine

Responsável por ordenar produtos
de acordo com seu potencial.

Não calcula Score.

Não toma decisões.

Não gera relatórios.

Sua única responsabilidade é
classificar produtos.
"""

from typing import List

from app.services.base_service import BaseService


class RankingEngine(BaseService):
    """
    Motor oficial de Ranking
    do TrendZone AI OS.
    """

    SERVICE_NAME = "RANKING_ENGINE"

    @classmethod
    def rank(
        cls,
        products: List[dict],
    ) -> List[dict]:

        cls.log_info(
            "Gerando ranking de produtos..."
        )

        ranking = sorted(

            products,

            key=lambda product: (

                product.get("score", 0),

                product.get("sales", 0),

                product.get("commission", 0),

                product.get("rating", 0),

            ),

            reverse=True,

        )

        cls.log_success(
            f"{len(ranking)} produto(s) classificados."
        )

        return ranking

    @classmethod
    def top(
        cls,
        products: List[dict],
        limit: int = 10,
    ) -> List[dict]:

        return cls.rank(products)[:limit]