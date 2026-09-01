"""
TrendZone AI OS
================================

Campaign Service.
"""

from app.integrations.shopee.graphql.repository import (
    GraphQLRepository,
)


class CampaignService:

    def __init__(
        self,
        access_token: str | None = None,
    ):

        self.repository = GraphQLRepository(
            access_token=access_token,
        )

    # =====================================================
    # SHOP OFFER
    # =====================================================

    def shop_offer(
        self,
        **filters,
    ):

        return self.repository.shop_offer(
            filters
        )

    # =====================================================
    # SHOPEE OFFER
    # =====================================================

    def shopee_offer(
        self,
        **filters,
    ):

        return self.repository.shopee_offer(
            filters
        )
    