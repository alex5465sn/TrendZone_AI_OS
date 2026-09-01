"""
TrendZone AI OS
================================

Product GraphQL Response.

Responsável por transformar
a resposta oficial da Shopee
em uma lista simples de produtos.
"""


class ProductResponse:

    @staticmethod
    def parse(response: dict):

        if not response:

            return []

        data = response.get("data", {})

        offers = data.get("productOfferV2", {})

        return offers.get("nodes", [])