"""
TrendZone AI OS
===============

Shopee Feed Service.

Responsável pelas operações relacionadas
aos feeds de produtos da Shopee Affiliate API.
"""

from __future__ import annotations

from app.integrations.shopee.graphql.repository import (
    GraphQLRepository,
)


class FeedService:

    def __init__(
        self,
        access_token: str | None = None,
    ) -> None:

        self.repository = GraphQLRepository(
            access_token=access_token,
        )

    # =====================================================
    # LIST ITEM FEEDS
    # =====================================================

    def item_feed(
        self,
        page: int = 1,
        limit: int = 20,
    ):

        variables = {
            "page": page,
            "limit": limit,
        }

        return self.repository.list_item_feeds(
            variables
        )

    # =====================================================
    # GET ITEM FEED DATA
    # =====================================================

    def get_item_feed_data(
        self,
        **variables,
    ):

        return self.repository.get_item_feed_data(
            variables
        )

    # =====================================================
    # COMPATIBILIDADE
    # =====================================================

    def list_item_feeds(
        self,
        page: int = 1,
        limit: int = 20,
    ):

        return self.item_feed(
            page=page,
            limit=limit,
        )

    # =====================================================
    # DATA FEEDS (usado pelo FeedRepository)
    # =====================================================

    def list_feeds(
        self,
        feed_mode: str | None = None,
    ):

        variables = {}

        if feed_mode:
            variables["feedMode"] = feed_mode

        return self.repository.list_item_feeds(
            variables
        )

    def feed_data(
        self,
        datafeed_id: str,
        offset: int = 0,
        limit: int = 500,
    ):

        variables = {
            "datafeedId": datafeed_id,
            "offset": offset,
            "limit": limit,
        }

        return self.repository.get_item_feed_data(
            variables
        )
