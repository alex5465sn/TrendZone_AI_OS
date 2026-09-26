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

import time

from app.core.dependency_provider import DependencyProvider

from app.services.base_service import BaseService


# Cache simples em memória para buscas de produtos.
# A API da Shopee pode levar vários segundos para responder;
# como a mesma categoria/palavra-chave costuma ser pesquisada
# de novo em poucos minutos (usuário reabrindo a tela, agente
# de auto-scout, etc.), reaproveitar a resposta recente evita
# nova espera sem impactar a atualidade dos dados.
_PRODUCTS_CACHE: dict = {}
_PRODUCTS_CACHE_TTL_SECONDS = 180


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

        cache_key = (marketplace_name, tuple(sorted(kwargs.items())))
        now = time.time()

        cached = _PRODUCTS_CACHE.get(cache_key)
        if cached and (now - cached[0]) < _PRODUCTS_CACHE_TTL_SECONDS:
            return cached[1]

        result = self.marketplace.search_products(

            marketplace_name,

            **kwargs,

        )

        _PRODUCTS_CACHE[cache_key] = (now, result)

        return result

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