from app.integrations.shopee.services.product_service import (
    ProductService,
)


class ProductRepository:
    """
    Repositório responsável por fornecer
    produtos ao restante do TrendZone AI OS.
    """

    def __init__(
        self,
        service: ProductService,
    ):

        self.service = service

    def list(
        self,
        filters: dict | None = None,
    ):

        return self.service.list_products(
            **(filters or {})
        )

    def list_products(
        self,
        **filters,
    ):

        return self.service.list_products(
            **filters
        )