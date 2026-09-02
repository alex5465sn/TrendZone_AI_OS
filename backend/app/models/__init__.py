"""
TrendZone AI OS
===============================

Models Oficiais da Aplicação.

Este módulo centraliza a exportação de todos
os Models SQLAlchemy utilizados pelo sistema.

Sempre importe os Models através deste package,
evitando importações diretas dos arquivos.

Exemplo:

from app.models import Product
from app.models import User

Nunca:

from app.models.product import Product
"""

from app.models.product import Product
from app.models.system_info import SystemInfo
from app.models.user import User
from app.models.campaign import Campaign

__all__ = (
    "Product",
    "SystemInfo",
    "User",
    "Campaign",
)