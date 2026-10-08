"""
TrendZone AI OS
================================

Health API

Responsável por informar o estado
geral da aplicação.

Enterprise Endpoint.
"""

from fastapi import APIRouter

from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health():

    return ResponseBuilder.success(

        data={

            "status": "online",

            "service": "TrendZone AI OS",

            "version": "2.0",

        },

        message="Sistema operacional.",

    )