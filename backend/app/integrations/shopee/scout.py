from app.integrations.shopee.client import ShopeeClient
from app.integrations.shopee.graphql import ShopeeGraphQL


class ShopeeScout:

    def __init__(self, token: str | None = None):

        self.client = ShopeeClient(token)
        self.graphql = ShopeeGraphQL(token)

    def status(self):

        return {
            "status": "online",
            "client": self.client.__class__.__name__,
            "graphql": self.graphql.__class__.__name__,
        }

    def get_products(self):

        """
        Futuramente este método fará a consulta real
        na API GraphQL da Shopee.

        Neste momento retornamos dados simulados
        exatamente no formato da API da Shopee.
        """

        return [

            {
                "itemId": 1001,
                "shopId": 500,
                "productName": "Mouse Gamer RGB",
                "price": 129.90,
                "commissionRate": 14.5,
                "ratingStar": 4.9,
                "sales": 8200,
                "imageUrl": "https://teste.com/mouse.jpg",
                "offerLink": "https://shopee.com/produto1",
            },

            {
                "itemId": 1002,
                "shopId": 501,
                "productName": "Teclado Mecânico",
                "price": 249.90,
                "commissionRate": 9.5,
                "ratingStar": 4.6,
                "sales": 3200,
                "imageUrl": "https://teste.com/teclado.jpg",
                "offerLink": "https://shopee.com/produto2",
            },

        ]