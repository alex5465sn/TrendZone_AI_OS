"""
TrendZone AI OS
================================

Publisher Agent

Última etapa do Pipeline.

Responsável por publicar, exportar
ou entregar o resultado final.

Não calcula Score.

Não valida produtos.

Não toma decisões.

Apenas publica o resultado produzido
pelos demais Agents.
"""

from app.agents.base_agent import BaseAgent
from app.agents.result import AgentResult


class PublisherAgent(BaseAgent):

    AGENT_ID = "PUBLISHER"

    NAME = "Publisher Agent"

    VERSION = "2.0"

    DESCRIPTION = (
        "Responsável pela publicação "
        "dos resultados do Pipeline."
    )

    def execute(self, context):

        try:

            reports = context.get_reports()

            published = []

            for report in reports:

                #
                # Futuramente:
                #
                # Shopee
                # Amazon
                # Mercado Livre
                # TikTok Shop
                # Instagram
                # Banco
                # Dashboard
                # API REST
                #
                published.append(report)

            context.set_metadata(

                "published_reports",

                len(published),

            )

            return AgentResult(

                success=True,

                agent=self.AGENT_ID,

                message=(
                    f"{len(published)} relatório(s) "
                    "publicado(s)."
                ),

                data=published,

            )

        except Exception as e:

            result = AgentResult(

                success=False,

                agent=self.AGENT_ID,

                message="Erro durante publicação.",

            )

            result.add_error(str(e))

            return result