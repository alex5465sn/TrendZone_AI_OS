"""
TrendZone AI OS
================================

Pacote oficial das Tasks.

Todas as Tasks do sistema devem
ser importadas por este módulo.

Nunca importe diretamente
os arquivos individuais.
"""

from app.tasks.base_task import BaseTask

from app.tasks.task_context import TaskContext
from app.tasks.task_result import TaskResult

from app.tasks.task_registry import TaskRegistry
from app.tasks.task_factory import TaskFactory

from app.tasks.task_pipeline import TaskPipeline

from app.tasks.scheduler import Scheduler
from app.tasks.runner import Runner

from app.tasks.retry import RetryPolicy

from app.tasks.history import TaskHistory
from app.tasks.monitor import TaskMonitor


__all__ = [

    "BaseTask",

    "TaskContext",

    "TaskResult",

    "TaskRegistry",

    "TaskFactory",

    "TaskPipeline",

    "Scheduler",

    "Runner",

    "RetryPolicy",

    "TaskHistory",

    "TaskMonitor",

]