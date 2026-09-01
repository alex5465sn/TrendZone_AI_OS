"""
TrendZone AI OS
================================

Trend Product Mapper

Converte DTOs de qualquer marketplace
para o modelo interno do TrendZone.
"""

from app.models.trend_product import TrendProduct

from app.integrations.shopee.dto.product_dto import (
    ProductDTO,
)


class TrendProductMapper:

    @staticmethod
    def from_shopee(
        dto: ProductDTO,
    ) -> TrendProduct:

        return TrendProduct(

            item_id=dto.item_id,

            shop_id=dto.shop_id,

            name=dto.name,

            image=dto.image,

            price=dto.price,

            commission=dto.commission,

            rating=dto.rating,

            sales=dto.sales,

            stock=dto.stock,

            currency=dto.currency,

            offer_link=dto.offer_link,

            category=dto.category,

            marketplace=dto.marketplace,

        )