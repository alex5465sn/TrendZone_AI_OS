"""
TrendZone AI OS
================================

Base Service.

Classe base para todos os Services
da aplicação.

Centraliza:

- Logging
- Tratamento de exceções
- Respostas padronizadas
- Métodos utilitários

Nenhuma regra de negócio deve ficar aqui.
"""

from typing import Any

from app.core.logger import TZLogger


class BaseService:
    """
    Classe base dos Services.
    """

    SERVICE_NAME = "BASE"

    @classmethod
    def log_info(
        cls,
        message: str,
    ) -> None:

        TZLogger.info(
            cls.SERVICE_NAME,
            message,
        )

    @classmethod
    def log_success(
        cls,
        message: str,
    ) -> None:

        TZLogger.success(
            cls.SERVICE_NAME,
            message,
        )

    @classmethod
    def log_warning(
        cls,
        message: str,
    ) -> None:

        TZLogger.warning(
            cls.SERVICE_NAME,
            message,
        )

    @classmethod
    def log_error(
        cls,
        message: str,
    ) -> None:

        TZLogger.error(
            cls.SERVICE_NAME,
            message,
        )

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Operação realizada com sucesso.",
    ) -> dict:

        return {
            "success": True,
            "message": message,
            "data": data,
        }

    @staticmethod
    def error(
        message: str,
        data: Any = None,
    ) -> dict:

        return {
            "success": False,
            "message": message,
            "data": data,
        }