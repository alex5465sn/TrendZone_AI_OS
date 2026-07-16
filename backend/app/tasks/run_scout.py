from app.agents.scout_agent import ScoutAgent
from app.core.logger import TZLogger


def run():

    TZLogger.info(

        "Scout IA",

        "Execução manual iniciada."

    )

    ScoutAgent().run()

    TZLogger.success(

        "Scout IA",

        "Execução concluída."

    )


if __name__ == "__main__":

    run()