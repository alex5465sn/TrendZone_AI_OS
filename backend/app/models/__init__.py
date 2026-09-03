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
from app.models.prospect import Prospect
from app.models.schedule import Schedule
from app.models.sale import Sale
from app.models.marketplace_account import MarketplaceAccount

__all__ = (
    "Product",
    "SystemInfo",
    "User",
    "Campaign",
    "Prospect",
    "Schedule",
    "Sale",
    "MarketplaceAccount",
)