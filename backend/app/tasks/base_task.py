"""
TrendZone AI OS
================================

BaseTask

Classe base para todas as Tasks do sistema.

Toda Task deve herdar desta classe.

Responsibilities
----------------
• Padronizar execução
• Padronizar nome
• Padronizar retorno
• Padronizar logs
"""

from abc import ABC, abstractmethod

from app.core.logger import TZLogger


class BaseTask(ABC):

    TASK_ID = "BASE"

    NAME = "Base Task"

    VERSION = "1.0"

    DESCRIPTION = "Classe base das Tasks."

    def before_execute(self):

        TZLogger.info(

            self.TASK_ID,

            "Iniciando Task..."

        )

    def after_execute(self):

        TZLogger.success(

            self.TASK_ID,

            "Task concluída."

        )

    @abstractmethod
    def execute(self, context):

        """
        Executa a Task.

        Deve retornar TaskResult.
        """

        pass

    def run(self, context):

        self.before_execute()

        result = self.execute(context)

        self.after_execute()

        return result