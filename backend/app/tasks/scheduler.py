"""
TrendZone AI OS
================================

Task Scheduler

Controla execuções automáticas do Pipeline
e dos serviços de background (Auto-Scout,
Auto-Publisher, Facebook Auto Post).

Usa asyncio nativo (compatível com FastAPI)
para agendar tarefas periódicas sem
dependências externas.
"""

import asyncio
from datetime import datetime

from app.core.logger import TZLogger
from app.tasks.task_pipeline import TaskPipeline


class Scheduler:

    _tasks: list = []
    _running = False

    def __init__(self):

        self.pipeline = TaskPipeline()

    def register_pipeline(self, pipeline: TaskPipeline):

        self.pipeline = pipeline

    def execute(self):

        TZLogger.info(
            "SCHEDULER",
            "Executando Pipeline..."
        )

        return self.pipeline.run()

    def start(self):

        if self._running:
            return

        self._running = True

        try:
            from app.services.auto_scout_service import AutoScoutService
            AutoScoutService.start()
            TZLogger.info("SCHEDULER", "Auto-Scout multi-marketplace ativo.")
        except Exception as e:
            TZLogger.warning("SCHEDULER", f"Auto-Scout falhou ao iniciar: {e}")

        try:
            from app.services.auto_publisher_service import AutoPublisherService
            AutoPublisherService.start()
            TZLogger.info("SCHEDULER", "Auto-Publisher ativo.")
        except Exception as e:
            TZLogger.warning("SCHEDULER", f"Auto-Publisher falhou ao iniciar: {e}")

        TZLogger.info(
            "SCHEDULER",
            "Scheduler iniciado com todos os serviços automáticos."
        )

    def stop(self):

        self._running = False

        try:
            from app.services.auto_scout_service import AutoScoutService
            AutoScoutService.stop()
        except Exception:
            pass

        try:
            from app.services.auto_publisher_service import AutoPublisherService
            AutoPublisherService.stop()
        except Exception:
            pass

        TZLogger.warning(
            "SCHEDULER",
            "Scheduler encerrado."
        )