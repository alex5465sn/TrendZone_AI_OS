"""
TrendZone AI OS

Camada de Models.

Todos os Models oficiais do sistema
devem ser exportados por este módulo.

Nunca importe Models diretamente
de outros arquivos.
"""

from app.models.product import Product
from app.models.system_info import SystemInfo
from app.models.user import User

__all__ = [
    "Product",
    "SystemInfo",
    "User",
]