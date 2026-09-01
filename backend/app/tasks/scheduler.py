"""
TrendZone AI OS
================================

Task Scheduler

Controla execuções automáticas
do Pipeline.

Nesta primeira versão o Scheduler
é manual.

No futuro suportará:

- Cron
- APScheduler
- Celery
- Redis
- Docker Workers
"""

from app.core.logger import TZLogger

from app.tasks.task_pipeline import TaskPipeline


class Scheduler:

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

        TZLogger.success(

            "SCHEDULER",

            "Scheduler iniciado."

        )

    def stop(self):

        TZLogger.warning(

            "SCHEDULER",

            "Scheduler encerrado."

        )