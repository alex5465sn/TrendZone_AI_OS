"""
TrendZone AI OS
================================

Ranking Agent

Responsável pelo cálculo
do Score de cada produto.

Não decide.

Não publica.

Não gera relatório.

Sua única responsabilidade
é calcular Score.
"""

from app.agents.base_agent import BaseAgent
from app.agents.result import AgentResult

from app.services.product_score import ProductScore


class RankingAgent(BaseAgent):

    AGENT_ID = "RANKING"

    NAME = "Ranking Agent"

    VERSION = "2.0"

    DESCRIPTION = "Calcula Score dos produtos."

    def execute(self, context):

        try:

            products = context.get_products()

            for product in products:

                score = ProductScore.calculate(

                    commission=product["commission"],

                    rating=product["rating"],

                    sales=product["sales"],

                )

                product["score"] = score

            context.set_products(products)

            context.set_metadata(

                "ranking_finished",

                True,

            )

            return AgentResult(

                success=True,

                agent=self.AGENT_ID,

                message=f"{len(products)} produtos ranqueados.",

                data=products,

            )

        except Exception as e:

            result = AgentResult(

                success=False,

                agent=self.AGENT_ID,

                message="Erro durante Ranking.",

            )

            result.add_error(str(e))

            return result