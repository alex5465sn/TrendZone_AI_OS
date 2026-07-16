"""
TrendZone AI OS
================================

CEO Agent

Responsável por decidir
a estratégia dos produtos.

Não calcula Score.

Não publica anúncios.

Sua única responsabilidade
é gerar a decisão executiva.
"""

from app.agents.base_agent import BaseAgent
from app.agents.result import AgentResult

from app.services.decision_engine import DecisionEngine
from app.services.executive_report import ExecutiveReport


class CEOAgent(BaseAgent):

    AGENT_ID = "CEO"

    NAME = "CEO Agent"

    VERSION = "2.0"

    DESCRIPTION = "Tomada de decisão estratégica."

    def execute(self, context):

        try:

            products = context.get_products()

            reports = []

            for product in products:

                decision = DecisionEngine.classify(product)

                product["decision"] = decision

                report = ExecutiveReport.build(product)

                reports.append(report)

            context.set_reports(reports)

            context.set_metadata(

                "reports_generated",

                len(reports),

            )

            return AgentResult(

                success=True,

                agent=self.AGENT_ID,

                message=f"{len(reports)} relatórios executivos gerados.",

                data=reports,

            )

        except Exception as e:

            result = AgentResult(

                success=False,

                agent=self.AGENT_ID,

                message="Erro durante análise estratégica.",

            )

            result.add_error(str(e))

            return result