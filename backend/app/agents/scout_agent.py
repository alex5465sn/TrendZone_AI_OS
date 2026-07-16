"""
TrendZone AI OS
================================

Scout Agent

Responsável por localizar produtos
nos marketplaces.

Não realiza ranking.

Não toma decisões.

Não publica anúncios.

Sua única responsabilidade é
descobrir produtos.
"""

from app.agents.base_agent import BaseAgent
from app.agents.result import AgentResult

from app.services.scout_service import ScoutService


class ScoutAgent(BaseAgent):

    AGENT_ID = "SCOUT"

    NAME = "Scout Agent"

    VERSION = "2.0"

    DESCRIPTION = "Localiza produtos nos Marketplaces."

    def __init__(self):

        super().__init__()

        self.service = ScoutService()

    def validate(self):

        return True

    def execute(self, context):

        try:

            products = self.service.search_products()

            context.set_products(products)

            context.set_metadata(

                "products_found",

                len(products),

            )

            return AgentResult(

                success=True,

                agent=self.AGENT_ID,

                message=f"{len(products)} produtos encontrados.",

                data=products,

            )

        except Exception as e:

            result = AgentResult(

                success=False,

                agent=self.AGENT_ID,

                message="Falha durante Scout.",

            )

            result.add_error(str(e))

            return result