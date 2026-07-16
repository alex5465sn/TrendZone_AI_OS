"""
TrendZone AI OS
================================

Analyst Agent

Responsável por validar
os produtos encontrados.

Não calcula Score.

Não define prioridade.

Não publica anúncios.
"""

from app.agents.base_agent import BaseAgent
from app.agents.result import AgentResult

from app.services.product_validator import ProductValidator


class AnalystAgent(BaseAgent):

    AGENT_ID = "ANALYST"

    NAME = "Analyst Agent"

    VERSION = "2.0"

    DESCRIPTION = "Validação dos produtos encontrados."

    def execute(self, context):

        try:

            approved = []

            rejected = []

            products = context.get_products()

            for product in products:

                try:

                    ProductValidator.validate(product)

                    approved.append(product)

                except Exception as e:

                    rejected.append(

                        {

                            "product": product,

                            "reason": str(e),

                        }

                    )

            context.set_products(

                approved

            )

            context.set_metadata(

                "approved_products",

                len(approved),

            )

            context.set_metadata(

                "rejected_products",

                len(rejected),

            )

            return AgentResult(

                success=True,

                agent=self.AGENT_ID,

                message=(

                    f"{len(approved)} produtos aprovados."

                ),

                data=approved,

                metadata={

                    "rejected": rejected

                }

            )

        except Exception as e:

            result = AgentResult(

                success=False,

                agent=self.AGENT_ID,

                message="Falha no Analyst.",

            )

            result.add_error(str(e))

            return result