"""
TrendZone AI OS
================================

Task Pipeline

Responsável por executar uma sequência
de Tasks registradas.

Arquitetura Enterprise.
"""

from app.core.logger import TZLogger

from app.tasks.task_context import TaskContext
from app.tasks.task_factory import TaskFactory


class TaskPipeline:

    def __init__(self):

        self.tasks: list[str] = []

    def add(self, task_id: str):

        self.tasks.append(task_id)

        return self

    def clear(self):

        self.tasks.clear()

    def run(self, context: TaskContext | None = None):

        if context is None:

            context = TaskContext()

        results = []

        TZLogger.info(

            "TASK_PIPELINE",

            f"Iniciando Pipeline ({len(self.tasks)} Tasks)"

        )

        for task_id in self.tasks:

            task = TaskFactory.create(task_id)

            result = task.run(context)

            results.append(result)

            context.add_history(

                f"{task_id}: {result.message}"

            )

            if result.failed:

                TZLogger.error(

                    "TASK_PIPELINE",

                    f"Pipeline interrompido na Task {task_id}"

                )

                break

        TZLogger.success(

            "TASK_PIPELINE",

            "Pipeline finalizado."

        )

        return results