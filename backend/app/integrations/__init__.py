"""
TrendZone AI OS
===============================

Camada oficial de integrações externas.

Todas as integrações do sistema devem ser
acessadas através deste package.

Exemplo:

from app.integrations import MarketplaceManager
"""

from app.integrations.marketplace.marketplace_manager import (
    MarketplaceManager,
)

__all__ = (
    "MarketplaceManager",
)