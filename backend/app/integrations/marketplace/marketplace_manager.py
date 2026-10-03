"""
TrendZone AI OS
================================

Marketplace Manager

Responsável por localizar o Provider
correto para cada Marketplace e
delegar as operações.

Nenhuma regra de negócio aqui.
"""

from app.integrations.providers import (
    ShopeeProvider,
    MercadoLivreProvider,
)


class MarketplaceManager:

    def __init__(self):

        self._providers = {

            "shopee": ShopeeProvider(),

            "mercado_livre": MercadoLivreProvider(),

        }

    # =====================================================
    # Provider
    # =====================================================

    def get_provider(
        self,
        marketplace: str,
    ):

        marketplace = marketplace.lower()

        if marketplace not in self._providers:

            raise ValueError(
                f"Marketplace '{marketplace}' não suportado."
            )

        return self._providers[marketplace]

    # =====================================================
    # Products
    # =====================================================

    def search_products(
        self,
        marketplace: str,
        **kwargs,
    ):

        provider = self.get_provider(
            marketplace
        )

        return provider.search_products(
            **kwargs
        )

    # =====================================================
    # Shops
    # =====================================================

    def search_shops(
        self,
        marketplace: str,
        **kwargs,
    ):

        provider = self.get_provider(
            marketplace
        )

        return provider.search_shops(
            **kwargs
        )

    # =====================================================
    # Offers
    # =====================================================

    def search_offers(
        self,
        marketplace: str,
        **kwargs,
    ):

        provider = self.get_provider(
            marketplace
        )

        return provider.search_offers(
            **kwargs
        )

    # =====================================================
    # Conversion Report
    # =====================================================

    def conversion_report(
        self,
        marketplace: str,
        **kwargs,
    ):

        provider = self.get_provider(
            marketplace
        )

        return provider.conversion_report(
            **kwargs
        )

    # =====================================================
    # Short Link
    # =====================================================

    def generate_short_link(
        self,
        marketplace: str,
        url: str,
        sub_ids=None,
    ):

        provider = self.get_provider(
            marketplace
        )

        return provider.generate_short_link(
            url=url,
            sub_ids=sub_ids,
        )
