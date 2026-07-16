"""
TrendZone AI OS
================================

Camada Repository.

Responsável exclusivamente pelo acesso
aos dados persistidos.

Nunca coloque regras de negócio aqui.

Fluxo correto:

API
 ↓
Service
 ↓
Repository
 ↓
Database
"""

from app.repositories.base_repository import BaseRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.system_info_repository import SystemInfoRepository
from app.repositories.user_repository import UserRepository

__all__ = (
    "BaseRepository",
    "ProductRepository",
    "SystemInfoRepository",
    "UserRepository",
)