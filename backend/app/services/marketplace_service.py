"""
TrendZone AI OS
================================

Marketplace Business Service.

Camada de serviço responsável pelas
operações de negócio relacionadas aos
marketplaces.

O serviço utiliza o DependencyProvider
para obter o MarketplaceManager.

Nenhuma lógica de infraestrutura deve
ser implementada diretamente aqui.
"""

from app.core.dependency_provider import DependencyProvider

from app.services.base_service import BaseService


class MarketplaceBusiness(BaseService):

    SERVICE_NAME = "MARKETPLACE"

    # =====================================================
    # Dependency
    # =====================================================

    def __init__(self):

        super().__init__()

        self.marketplace = (
            DependencyProvider.marketplace()
        )

    # =====================================================
    # Products
    # =====================================================

    def search_products(

        self,

        marketplace_name: str,

        **kwargs,

    ):

        return self.marketplace.search_products(

            marketplace_name,

            **kwargs,

        )

    # =====================================================
    # Shops
    # =====================================================

    def search_shops(

        self,

        marketplace_name: str,

        **kwargs,

    ):

        return self.marketplace.search_shops(

            marketplace_name,

            **kwargs,

        )

    # =====================================================
    # Offers
    # =====================================================

    def search_offers(

        self,

        marketplace_name: str,

        **kwargs,

    ):

        return self.marketplace.search_offers(

            marketplace_name,

            **kwargs,

        )

    # =====================================================
    # Reports
    # =====================================================

    def conversion_report(

        self,

        marketplace_name: str,

        **kwargs,

    ):

        return self.marketplace.conversion_report(

            marketplace_name,

            **kwargs,

        )

    # =====================================================
    # Links
    # =====================================================

    def generate_short_link(

        self,

        marketplace_name: str,

        url: str,

        sub_ids=None,

    ):

        return self.marketplace.generate_short_link(

            marketplace_name,

            url,

            sub_ids,

        )