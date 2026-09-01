from typing import Any

from app.integrations.shopee.gateway import ShopeeGateway


class ShopeeProducts:
    """
    Responsável pelas operações relacionadas aos produtos
    da Shopee Affiliate Open API.
    """

    def __init__(
        self,
        gateway: ShopeeGateway,
    ):
        self.gateway = gateway

    def get_offer_list(
        self,
        limit: int = 100,
        scroll_id: str | None = None,
    ):

        variables: dict[str, Any] = {
            "limit": limit,
        }

        if scroll_id:
            variables["scrollId"] = scroll_id

        return self.gateway.execute(
            query="",
            variables=variables,
        )

    def get_offer(
        self,
        item_id: int,
    ):

        variables = {
            "itemId": item_id,
        }

        return self.gateway.execute(
            query="",
            variables=variables,
        )

    def search_products(
        self,
        keyword: str,
        limit: int = 100,
    ):

        variables = {
            "keyword": keyword,
            "limit": limit,
        }

        return self.gateway.execute(
            query="",
            variables=variables,
        )