"""
TrendZone AI OS
================================

Task History

Responsável por registrar
todo histórico de execução
das Tasks e Pipelines.
"""

from datetime import datetime


class TaskHistory:

    def __init__(self):

        self._executions = []

    def add(

        self,

        task: str,

        success: bool,

        message: str,

        duration: float = 0,

    ):

        self._executions.append(

            {

                "timestamp": datetime.utcnow(),

                "task": task,

                "success": success,

                "message": message,

                "duration": duration,

            }

        )

    def all(self):

        return self._executions

    def clear(self):

        self._executions.clear()

    def count(self):

        return len(self._executions)

    def success_count(self):

        return sum(

            1

            for item in self._executions

            if item["success"]

        )

    def failed_count(self):

        return sum(

            1

            for item in self._executions

            if not item["success"]

        )