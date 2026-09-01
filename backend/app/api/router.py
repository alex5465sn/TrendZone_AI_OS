"""
TrendZone AI OS
================================

API Router

Roteador principal da API.

Centraliza todas as rotas da
aplicação.

Versão Enterprise.
"""

from fastapi import APIRouter

api_router = APIRouter(
    prefix="/api/v1",
    tags=["TrendZone AI OS"],
)