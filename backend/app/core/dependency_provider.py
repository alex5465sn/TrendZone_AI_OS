"""
TrendZone AI OS

Dependency Provider
"""

from app.integrations.marketplace.marketplace_manager import (
    MarketplaceManager,
)


class DependencyProvider:

    @staticmethod
    def marketplace():

        return MarketplaceManager()