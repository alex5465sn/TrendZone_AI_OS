"""
TrendZone AI OS
================================

Task Factory

Responsável por instanciar
Tasks registradas.

Nenhuma classe externa deverá
instanciar Tasks diretamente.

Toda criação acontece aqui.
"""

from app.tasks.task_registry import TaskRegistry


class TaskFactory:

    @staticmethod
    def create(task_id: str):

        task_class = TaskRegistry.get(task_id)

        if task_class is None:

            raise ValueError(

                f"Task '{task_id}' não registrada."

            )

        return task_class()

    @staticmethod
    def exists(task_id: str):

        return TaskRegistry.exists(task_id)