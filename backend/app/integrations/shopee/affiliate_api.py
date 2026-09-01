"""
TrendZone AI OS
====================================

Shopee Affiliate API

Fachada oficial para acesso à
API de Afiliados da Shopee.

Toda comunicação externa deve
passar por esta classe.
"""

from app.integrations.shopee.client import ShopeeClient
from app.integrations.shopee.graphql import (
    PRODUCT_OFFER_V2,
    SHOP_OFFER_V2,
    SHOPEE_OFFER_V2,
    CONVERSION_REPORT,
    VALIDATED_REPORT,
    GENERATE_SHORT_LINK,
    GENERATE_BATCH_SHORT_LINK,
    LIST_ITEM_FEEDS,
    GET_ITEM_FEED_DATA,
)


class ShopeeAffiliateAPI:

    def __init__(self):

        self.client = ShopeeClient()

    # =====================================================
    # PRODUCTS
    # =====================================================

    def get_products(self, **variables):

        return self.client.execute(
            PRODUCT_OFFER_V2,
            variables,
        )

    # =====================================================
    # SHOPS
    # =====================================================

    def get_shops(self, **variables):

        return self.client.execute(
            SHOP_OFFER_V2,
            variables,
        )

    # =====================================================
    # CAMPAIGNS
    # =====================================================

    def get_campaigns(self, **variables):

        return self.client.execute(
            SHOPEE_OFFER_V2,
            variables,
        )

    # =====================================================
    # REPORTS
    # =====================================================

    def conversion_report(self, **variables):

        return self.client.execute(
            CONVERSION_REPORT,
            variables,
        )

    def validated_report(self, **variables):

        return self.client.execute(
            VALIDATED_REPORT,
            variables,
        )

    # =====================================================
    # SHORT LINKS
    # =====================================================

    def generate_short_link(self, **variables):

        return self.client.execute(
            GENERATE_SHORT_LINK,
            variables,
        )

    def generate_batch_short_links(self, **variables):

        return self.client.execute(
            GENERATE_BATCH_SHORT_LINK,
            variables,
        )

    # =====================================================
    # ITEM FEEDS
    # =====================================================

    def list_item_feeds(self, **variables):

        return self.client.execute(
            LIST_ITEM_FEEDS,
            variables,
        )

    def get_item_feed_data(self, **variables):

        return self.client.execute(
            GET_ITEM_FEED_DATA,
            variables,
        )