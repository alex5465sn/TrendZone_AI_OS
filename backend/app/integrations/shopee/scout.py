"""
TrendZone AI OS
====================================

Shopee Scout

Camada responsável por buscar
dados na API Oficial da Shopee.

Não contém regras de negócio.

Não calcula score.

Não gera relatórios.

Não toma decisões.
"""

from app.integrations.shopee.affiliate_api import ShopeeAffiliateAPI


class ShopeeScout:

    def __init__(self):

        self.api = ShopeeAffiliateAPI()

    # =====================================================
    # PRODUCTS
    # =====================================================

    def get_products(

        self,

        keyword: str | None = None,

        page: int = 1,

        limit: int = 20,

    ):

        response = self.api.get_products(

            keyword=keyword,

            page=page,

            limit=limit,

        )

        return (

            response

            .get("productOfferV2", {})

            .get("nodes", [])

        )

    # =====================================================
    # SHOPS
    # =====================================================

    def get_shops(

        self,

        keyword: str | None = None,

        page: int = 1,

        limit: int = 20,

    ):

        response = self.api.get_shops(

            keyword=keyword,

            page=page,

            limit=limit,

        )

        return (

            response

            .get("shopOfferV2", {})

            .get("nodes", [])

        )

    # =====================================================
    # CAMPAIGNS
    # =====================================================

    def get_campaigns(

        self,

        keyword: str | None = None,

        page: int = 1,

        limit: int = 20,

    ):

        response = self.api.get_campaigns(

            keyword=keyword,

            page=page,

            limit=limit,

        )

        return (

            response

            .get("shopeeOfferV2", {})

            .get("nodes", [])

        )