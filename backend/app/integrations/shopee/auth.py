from app.integrations.shopee.client import (
    ShopeeClient,
)


class ShopeeAuth:

    def __init__(
        self,
        access_token: str,
    ):
        self.client = ShopeeClient(
            access_token
        )

    def headers(self):
        return self.client.get_headers()