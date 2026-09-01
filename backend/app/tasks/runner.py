"""
TrendZone AI OS
================================

Task Runner

Ponto de entrada para execução
de Tasks e Pipelines.

Responsável por iniciar todo
o fluxo de execução.
"""

from app.core.logger import TZLogger

from app.tasks.scheduler import Scheduler


class Runner:

    def __init__(self):

        self.scheduler = Scheduler()

    def execute(self):

        TZLogger.info(

            "RUNNER",

            "Inicializando execução."

        )

        results = self.scheduler.execute()

        TZLogger.success(

            "RUNNER",

            "Execução finalizada."

        )

        return results