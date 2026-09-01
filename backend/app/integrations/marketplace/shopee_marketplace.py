"""
TrendZone AI OS
================================

Shopee Marketplace

Implementação oficial do
Marketplace Shopee.
"""

from app.integrations.marketplace.base_marketplace import (
    BaseMarketplace,
)

from app.integrations.shopee.services.product_service import (
    ShopeeProductService,
)


class ShopeeMarketplace(BaseMarketplace):

    def __init__(self):

        self.service = ShopeeProductService()

    def search_products(

        self,

        keyword: str,

        page: int,

        limit: int,

    ):

        return self.service.search_products(

            keyword=keyword,

            page=page,

            limit=limit,

        )