"""
TrendZone AI OS
================================

Shopee GraphQL Parser

Responsável por converter as respostas
da API GraphQL da Shopee em DTOs
padronizados do TrendZone AI OS.
"""

from app.integrations.shopee.dto.product_dto import ProductDTO


class GraphQLParser:

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _to_product(item: dict) -> ProductDTO:

        return ProductDTO(

            item_id=item.get("itemId", 0),

            shop_id=item.get("shopId", 0),

            name=item.get("productName", ""),

            image=item.get("imageUrl"),

            price=float(item.get("price", 0)),

            commission=float(item.get("commissionRate", 0)),

            rating=float(item.get("ratingStar", 0)),

            sales=int(item.get("sales", 0)),

            stock=int(item.get("stock", 0)),

            currency=item.get("currency", "BRL"),

            offer_link=item.get("offerLink"),

            category=item.get("categoryName"),

            marketplace="Shopee",

        )

    # =====================================================
    # Product Offer
    # =====================================================

    @classmethod
    def product_offer(
        cls,
        data: dict,
    ) -> list[ProductDTO]:

        offer = data.get("productOfferV2", {})

        nodes = offer.get("nodes", [])

        return [

            cls._to_product(node)

            for node in nodes

        ]

    # =====================================================
    # Shop Offer
    # =====================================================

    @classmethod
    def shop_offer(
        cls,
        data: dict,
    ) -> list[ProductDTO]:

        offer = data.get("shopOfferV2", {})

        nodes = offer.get("nodes", [])

        return [

            cls._to_product(node)

            for node in nodes

        ]

    # =====================================================
    # Shopee Offer
    # =====================================================

    @classmethod
    def shopee_offer(
        cls,
        data: dict,
    ) -> list[ProductDTO]:

        offer = data.get("shopeeOfferV2", {})

        nodes = offer.get("nodes", [])

        return [

            cls._to_product(node)

            for node in nodes

        ]

    # =====================================================
    # Feed
    # =====================================================

    @classmethod
    def item_feed(
        cls,
        data: dict,
    ) -> list[ProductDTO]:

        feed = data.get("itemFeed", {})

        nodes = feed.get("nodes", [])

        return [

            cls._to_product(node)

            for node in nodes

        ]