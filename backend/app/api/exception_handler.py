"""
TrendZone AI OS
================================

Global Exception Handler

Centraliza todas as exceções
da API.

Nenhum endpoint deverá utilizar
try/except desnecessariamente.
"""

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError

from app.api.response import ResponseBuilder
from app.core.logger import TZLogger


class ExceptionHandler:

    @staticmethod
    def register(app: FastAPI):

        @app.exception_handler(ValueError)
        async def value_error_handler(
            request: Request,
            exc: ValueError,
        ):

            TZLogger.error(

                "VALUE_ERROR",

                str(exc),

            )

            return ResponseBuilder.error(

                message=str(exc),

                status_code=400,

            )

        @app.exception_handler(RequestValidationError)
        async def validation_error_handler(
            request: Request,
            exc: RequestValidationError,
        ):

            TZLogger.error(

                "VALIDATION",

                str(exc),

            )

            return ResponseBuilder.error(

                message="Erro de validação.",

                status_code=422,

                errors=exc.errors(),

            )

        @app.exception_handler(Exception)
        async def generic_error_handler(
            request: Request,
            exc: Exception,
        ):

            TZLogger.error(

                "SERVER",

                str(exc),

            )

            return ResponseBuilder.error(

                message="Erro interno do servidor.",

                status_code=500,

            )