"""
TrendZone AI OS
================================

Orchestrator.

Responsável por executar
o Pipeline oficial do sistema.

Não contém regras de negócio.

Sua única responsabilidade é
coordenar a execução dos Agents.
"""

from app.agents.context import AgentContext
from app.agents.factory import AgentFactory
from app.agents.result import AgentResult
from app.agents.default_pipeline import pipeline

from app.core.logger import TZLogger


class Orchestrator:

    def __init__(self):

        self.context = AgentContext()

    # =====================================================
    # EXECUÇÃO
    # =====================================================

    def execute(self):

        TZLogger.info(

            "ORCHESTRATOR",

            "Pipeline iniciado."

        )

        results = []

        for step in pipeline.get_steps():

            agent = AgentFactory.create(

                step.agent_id

            )

            self.context.current_agent = (

                step.agent_id

            )

            TZLogger.info(

                "ORCHESTRATOR",

                f"Executando {step.agent_id}"

            )

            result = agent.run(

                self.context

            )

            results.append(result)

            if isinstance(

                result,

                AgentResult,

            ):

                if not result.success:

                    TZLogger.error(

                        "ORCHESTRATOR",

                        f"{step.agent_id} falhou."

                    )

                    break

        self.context.finish()

        TZLogger.success(

            "ORCHESTRATOR",

            "Pipeline concluído."

        )

        return results

    # =====================================================
    # STATUS
    # =====================================================

    def status(self):

        return {

            "execution_id":

                self.context.execution_id,

            "duration":

                self.context.duration,

            "agents":

                pipeline.names(),

        }