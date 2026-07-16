from time import perf_counter

from app.core.logger import TZLogger
from app.database.base import Base
from app.database.session import engine


class DatabaseInitializer:
    """
    Responsável por inicializar
    toda a estrutura do banco.
    """

    @staticmethod
    def initialize():

        TZLogger.info(
            "DATABASE",
            "Inicializando banco de dados..."
        )

        start = perf_counter()

        try:

            Base.metadata.create_all(bind=engine)

            elapsed = perf_counter() - start

            TZLogger.success(
                "DATABASE",
                f"Banco inicializado com sucesso ({elapsed:.2f}s)"
            )

        except Exception as e:

            TZLogger.error(
                "DATABASE",
                str(e)
            )

            raise


def init_database():

    DatabaseInitializer.initialize()