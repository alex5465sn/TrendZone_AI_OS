from app.agents.orchestrator import Orchestrator
from app.core.logger import TZLogger


def run_pipeline():

    TZLogger.info(

        "Pipeline",

        "Inicializando execução automática."

    )

    orchestrator = Orchestrator()

    result = orchestrator.run()

    TZLogger.success(

        "Pipeline",

        "Execução finalizada."

    )

    return result


if __name__ == "__main__":

    run_pipeline()