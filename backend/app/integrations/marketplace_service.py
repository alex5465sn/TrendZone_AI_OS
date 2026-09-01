"""
TrendZone AI OS
================================

Marketplace Service

Responsável por localizar o Provider
correto para cada Marketplace.
"""

from app.integrations.providers import ShopeeProvider


class MarketplaceService:

    def __init__(self):

        self.providers = {

            "shopee": ShopeeProvider(),

        }

    # =====================================================

    def provider(

        self,

        marketplace: str,

    ):

        marketplace = marketplace.lower()

        if marketplace not in self.providers:

            raise ValueError(

                f"Marketplace '{marketplace}' não suportado."

            )

        return self.providers[marketplace]