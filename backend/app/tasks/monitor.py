"""
TrendZone AI OS
================================

Task Monitor

Monitora métricas da execução.

Versão Enterprise.
"""

from time import perf_counter


class TaskMonitor:

    def __init__(self):

        self.start_time = None

        self.end_time = None

        self.executed_tasks = 0

        self.failed_tasks = 0

    def start(self):

        self.start_time = perf_counter()

    def finish(self):

        self.end_time = perf_counter()

    def task_success(self):

        self.executed_tasks += 1

    def task_failed(self):

        self.executed_tasks += 1

        self.failed_tasks += 1

    @property
    def execution_time(self):

        if (

            self.start_time is None

            or self.end_time is None

        ):

            return 0

        return round(

            self.end_time - self.start_time,

            3,

        )

    def report(self):

        return {

            "tasks": self.executed_tasks,

            "failed": self.failed_tasks,

            "success": (

                self.executed_tasks

                - self.failed_tasks

            ),

            "execution_time": self.execution_time,

        }