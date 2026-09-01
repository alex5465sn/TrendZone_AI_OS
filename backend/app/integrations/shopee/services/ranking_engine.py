"""
TrendZone AI OS
================================

Ranking Engine

Responsável por ordenar produtos
de acordo com o potencial de venda.

Não calcula Score.

Não toma decisões.

Apenas organiza os produtos.
"""

from app.services.base_service import BaseService


class RankingEngine(BaseService):

    SERVICE_NAME = "RANKING_ENGINE"

    @classmethod
    def rank(cls, products: list[dict]) -> list[dict]:

        cls.log_info(
            "Gerando ranking..."
        )

        ranking = sorted(

            products,

            key=lambda product: (

                product["score"],

                product["sales"],

                product["commission"],

                product["rating"],

            ),

            reverse=True,

        )

        cls.log_success(

            f"{len(ranking)} produtos classificados."

        )

        return ranking

    @classmethod
    def top(cls, products, limit=10):

        return cls.rank(products)[:limit]