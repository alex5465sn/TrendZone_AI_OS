"""
TrendZone AI OS
================================

Response Builder

Padroniza todas as respostas
da API.

Nenhum endpoint deve retornar
JSON manualmente.
"""

from datetime import datetime

from fastapi.responses import JSONResponse


class ResponseBuilder:

    @staticmethod
    def success(

        data=None,

        message="Sucesso.",

        status_code=200,

    ):

        return JSONResponse(

            status_code=status_code,

            content={

                "success": True,

                "message": message,

                "timestamp": datetime.utcnow().isoformat(),

                "data": data,

            },

        )

    @staticmethod
    def error(

        message,

        status_code=400,

        errors=None,

    ):

        return JSONResponse(

            status_code=status_code,

            content={

                "success": False,

                "message": message,

                "timestamp": datetime.utcnow().isoformat(),

                "errors": errors or [],

            },

        )