"""
TrendZone AI OS
================================

Shopee Service

Camada de alto nível responsável por
consumir a API Oficial da Shopee.

Nenhuma outra parte do sistema deve
conhecer GraphQL.

Todas as consultas passam por aqui.
"""

from __future__ import annotations

from app.integrations.shopee.graphql_executor import GraphQLExecutor

from app.integrations.shopee.graphql import (
    PRODUCT_OFFER_V2,
    SHOP_OFFER_V2,
    SHOPEE_OFFER_V2,
    GENERATE_SHORT_LINK,
    CONVERSION_REPORT,
)


class ShopeeService:

    def __init__(
        self,
        access_token: str | None = None,
    ) -> None:

        self.executor = GraphQLExecutor(
            access_token=access_token,
        )

    # =====================================================
    # PRODUCT OFFERS
    # =====================================================

    def product_offers(self, **variables):

        defaults = {
            "listType": 0,
            "matchId": None,
            "keyword": "",
            "sortType": 1,
            "page": 1,
            "limit": 20,
            "itemId": None,
            "shopId": None,
            "productCatId": None,
            "isAMSOffer": None,
            "isKeySeller": None,
        }

        defaults.update(variables)

        data = self.executor.execute(

            query=PRODUCT_OFFER_V2,

            variables=defaults,

        )

        return data.get(
            "productOfferV2",
            {},
        )

    # =====================================================
    # SHOP OFFERS
    # =====================================================

    def shop_offers(self, **variables):

        defaults = {
            "keyword": "",
            "shopType": None,
            "sortType": 1,
            "sellerCommCoveRatio": None,
            "page": 1,
            "limit": 20,
            "shopId": None,
            "isKeySeller": None,
        }

        defaults.update(variables)

        data = self.executor.execute(

            query=SHOP_OFFER_V2,

            variables=defaults,

        )

        return data.get(
            "shopOfferV2",
            {},
        )

    # =====================================================
    # SHOPEE OFFERS
    # =====================================================

    def shopee_offers(self, **variables):

        defaults = {
            "keyword": "",
            "sortType": 1,
            "page": 1,
            "limit": 20,
        }

        defaults.update(variables)

        data = self.executor.execute(

            query=SHOPEE_OFFER_V2,

            variables=defaults,

        )

        return data.get(
            "shopeeOfferV2",
            {},
        )

    # =====================================================
    # SHORT LINK
    # =====================================================

    def generate_short_link(
        self,
        source_url: str,
        sub_ids: list[str] | None = None,
    ):

        variables = {

            "originUrl": source_url,

            "subIds": sub_ids or [],

        }

        data = self.executor.execute(

            query=GENERATE_SHORT_LINK,

            variables=variables,

        )

        return data.get(
            "generateShortLink",
            {},
        )

    # =====================================================
    # CONVERSION REPORT
    # =====================================================

    def conversion_report(self, **variables):

        data = self.executor.execute(

            query=CONVERSION_REPORT,

            variables=variables,

        )

        return data.get(
            "conversionReport",
            {},
        )