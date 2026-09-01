"""
TrendZone AI OS
================================

Shopee Provider

Implementação oficial do Provider da Shopee.
"""

from app.integrations.providers.base_provider import BaseProvider
from app.integrations.shopee.shopee_service import ShopeeService


class ShopeeProvider(BaseProvider):

    def __init__(self):

        self.service = ShopeeService()

    # =====================================================
    # PRODUCTS
    # =====================================================

    def search_products(self, **kwargs):

        return self.service.product_offers(**kwargs)

    # =====================================================
    # SHOPS
    # =====================================================

    def search_shops(self, **kwargs):

        return self.service.shop_offers(**kwargs)

    # =====================================================
    # OFFERS
    # =====================================================

    def search_offers(self, **kwargs):

        return self.service.shopee_offers(**kwargs)

    # =====================================================
    # SHORT LINK
    # =====================================================

    def generate_short_link(

        self,

        url: str,

        sub_ids=None,

    ):

        return self.service.generate_short_link(

            source_url=url,

            sub_ids=sub_ids,

        )

    # =====================================================
    # REPORT
    # =====================================================

    def conversion_report(self, **kwargs):

        return self.service.conversion_report(**kwargs)