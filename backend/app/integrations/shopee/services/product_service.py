"""
TrendZone AI OS
================================

Shopee Product Service.

Responsável pelas operações
relacionadas aos produtos da API
de Afiliados da Shopee.
"""

from app.integrations.shopee.graphql.repository import (
    GraphQLRepository,
)

from app.integrations.shopee.graphql.parser import (
    GraphQLParser,
)


class ProductService:

    def __init__(
        self,
        access_token: str | None = None,
    ):

        self.repository = GraphQLRepository(
            access_token=access_token,
        )

    # =====================================================
    # PRODUCT OFFER V2
    # =====================================================

    def list_products(
        self,
        keyword: str = "",
        page: int = 1,
        limit: int = 20,
        sortType: int = 1,
        listType: int = 0,
        matchId: int | None = None,
        itemId: int | None = None,
        shopId: int | None = None,
        productCatId: int | None = None,
        isAMSOffer: bool | None = None,
        isKeySeller: bool | None = None,
        **kwargs,
    ):

        variables = {
            "listType": listType,
            "matchId": matchId,
            "keyword": keyword,
            "sortType": sortType,
            "page": page,
            "limit": limit,
            "itemId": itemId,
            "shopId": shopId,
            "productCatId": productCatId,
            "isAMSOffer": isAMSOffer,
            "isKeySeller": isKeySeller,
        }

        variables.update(kwargs)

        response = self.repository.product_offer(
            variables
        )

        return GraphQLParser.product_offer(
            response
        )

    # =====================================================
    # COMPATIBILIDADE
    # =====================================================

    def search_products(
        self,
        keyword: str = "",
        page: int = 1,
        limit: int = 20,
        sortType: int = 1,
        **kwargs,
    ):

        return self.list_products(
            keyword=keyword,
            page=page,
            limit=limit,
            sortType=sortType,
            **kwargs,
        )


ShopeeProductService = ProductService