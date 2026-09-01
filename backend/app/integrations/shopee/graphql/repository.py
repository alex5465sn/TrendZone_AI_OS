"""
TrendZone AI OS
================================

Shopee GraphQL Repository.

Centraliza todas as chamadas GraphQL
da Shopee.

Nenhum Service deve conversar
diretamente com o Executor.

Toda operação oficial passa
por esta camada.
"""

from __future__ import annotations

from typing import Any

from app.integrations.shopee.graphql_executor import (
    GraphQLExecutor,
)

from app.integrations.shopee.graphql.products import (
    PRODUCT_OFFER_V2,
)

from app.integrations.shopee.graphql.campaigns import (
    SHOP_OFFER_V2,
    SHOPEE_OFFER_V2,
)

from app.integrations.shopee.graphql.feeds import (
    LIST_ITEM_FEEDS,
    GET_ITEM_FEED_DATA,
)

from app.integrations.shopee.graphql.links import (
    GENERATE_SHORT_LINK,
    GENERATE_BATCH_SHORT_LINK,
)

from app.integrations.shopee.graphql.reports import (
    CONVERSION_REPORT,
    VALIDATED_REPORT,
)


class GraphQLRepository:
    """
    Repositório central para operações
    GraphQL da Shopee Affiliate API.
    """

    def __init__(
        self,
        access_token: str | None = None,
    ) -> None:

        self.executor = GraphQLExecutor(
            access_token=access_token,
        )

    # =====================================================
    # PRODUCTS
    # =====================================================

    def product_offer(
        self,
        variables: dict,
    ) -> dict[str, Any]:

        return self.executor.execute(
            query=PRODUCT_OFFER_V2,
            variables=variables,
        )

    # =====================================================
    # CAMPAIGNS
    # =====================================================

    def shop_offer(
        self,
        variables: dict,
    ) -> dict[str, Any]:

        return self.executor.execute(
            query=SHOP_OFFER_V2,
            variables=variables,
        )

    def shopee_offer(
        self,
        variables: dict,
    ) -> dict[str, Any]:

        return self.executor.execute(
            query=SHOPEE_OFFER_V2,
            variables=variables,
        )

    # =====================================================
    # FEEDS
    # =====================================================

    def list_item_feeds(
        self,
        variables: dict | None = None,
    ) -> dict[str, Any]:

        return self.executor.execute(
            query=LIST_ITEM_FEEDS,
            variables=variables or {},
        )

    def get_item_feed_data(
        self,
        variables: dict,
    ) -> dict[str, Any]:

        return self.executor.execute(
            query=GET_ITEM_FEED_DATA,
            variables=variables,
        )

    # =====================================================
    # LINKS
    # =====================================================

    def generate_short_link(
        self,
        variables: dict,
    ) -> dict[str, Any]:

        return self.executor.execute(
            query=GENERATE_SHORT_LINK,
            variables=variables,
        )

    def generate_batch_short_link(
        self,
        variables: dict,
    ) -> dict[str, Any]:

        return self.executor.execute(
            query=GENERATE_BATCH_SHORT_LINK,
            variables=variables,
        )

    # =====================================================
    # REPORTS
    # =====================================================

    def conversion_report(
        self,
        variables: dict,
    ) -> dict[str, Any]:

        return self.executor.execute(
            query=CONVERSION_REPORT,
            variables=variables,
        )

    def validated_report(
        self,
        variables: dict,
    ) -> dict[str, Any]:

        return self.executor.execute(
            query=VALIDATED_REPORT,
            variables=variables,
        )