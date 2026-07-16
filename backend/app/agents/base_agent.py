"""
TrendZone AI OS
================================

Base Agent.

Classe base para todos os agentes
do sistema.

Todos os Agents deverão herdar
desta classe.

Nunca implemente um Agent
sem utilizar BaseAgent.
"""

from abc import ABC
from abc import abstractmethod
from time import perf_counter
from uuid import uuid4

from app.core.logger import TZLogger


class BaseAgent(ABC):

    NAME = "BASE_AGENT"

    VERSION = "1.0"

    DESCRIPTION = ""

    def __init__(self):

        self.id = str(uuid4())

        self.execution_time = 0

        self.initialized = False

        self.finished = False

    # =====================================================
    # LIFECYCLE
    # =====================================================

    def initialize(self):

        self.initialized = True

        TZLogger.info(

            self.NAME,

            "Inicializado."

        )

    def validate(self):

        return True

    def before_execute(self):

        pass

    @abstractmethod
    def execute(self, context):

        """
        Método obrigatório.
        """

    def after_execute(self):

        pass

    def finish(self):

        self.finished = True

        TZLogger.success(

            self.NAME,

            "Finalizado."

        )

    # =====================================================
    # EXECUÇÃO
    # =====================================================

    def run(self, context=None):

        start = perf_counter()

        self.initialize()

        self.validate()

        self.before_execute()

        result = self.execute(context)

        self.after_execute()

        self.execution_time = (

            perf_counter() - start

        )

        self.finish()

        return result

    # =====================================================
    # STATUS
    # =====================================================

    def status(self):

        return {

            "id": self.id,

            "name": self.NAME,

            "version": self.VERSION,

            "initialized": self.initialized,

            "finished": self.finished,

            "execution_time": round(

                self.execution_time,

                4,

            ),

        }