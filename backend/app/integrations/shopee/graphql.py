from app.integrations.shopee.client import ShopeeClient


class ShopeeGraphQL:

    def __init__(
        self,
        access_token: str | None = None,
    ):
        self.client = ShopeeClient(
            access_token
        )

    def execute(
        self,
        query: str,
        variables: dict | None = None,
    ):
        return self.client.execute(
            query=query,
            variables=variables,
        )