"""
TrendZone AI OS
================================

Task Registry

Responsável por registrar todas
as Tasks do sistema.

Novas Tasks são registradas
automaticamente.

Arquitetura Enterprise.
"""

from typing import Type

from app.tasks.base_task import BaseTask


class TaskRegistry:

    _registry: dict[str, Type[BaseTask]] = {}

    @classmethod
    def register(cls, task: Type[BaseTask]):

        cls._registry[task.TASK_ID] = task

    @classmethod
    def get(cls, task_id: str):

        return cls._registry.get(task_id)

    @classmethod
    def exists(cls, task_id: str):

        return task_id in cls._registry

    @classmethod
    def all(cls):

        return cls._registry

    @classmethod
    def clear(cls):

        cls._registry.clear()