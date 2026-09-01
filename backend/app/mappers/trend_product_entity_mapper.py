"""
TrendZone AI OS
================================

Trend Product Entity Mapper

Converte o modelo de domínio
TrendProduct para TrendProductEntity.
"""

from app.domain.product import TrendProduct

from app.models.trend_product_entity import (
    TrendProductEntity,
)


class TrendProductEntityMapper:

    @staticmethod
    def to_entity(
        product: TrendProduct,
    ) -> TrendProductEntity:

        return TrendProductEntity(

            item_id=product.item_id,

            shop_id=product.shop_id,

            marketplace=product.marketplace,

            name=product.name,

            image=product.image or "",

            category=product.category or "",

            offer_link=product.offer_link or "",

            currency=product.currency,

            price=product.price,

            commission=product.commission,

            rating=product.rating,

            sales=product.sales,

            stock=product.stock,

            score=product.score,

            decision=product.decision,

            ranking=product.ranking,

        )

    @staticmethod
    def update_entity(
        entity: TrendProductEntity,
        product: TrendProduct,
    ) -> TrendProductEntity:

        entity.name = product.name
        entity.image = product.image or ""
        entity.category = product.category or ""
        entity.offer_link = product.offer_link or ""
        entity.currency = product.currency

        entity.price = product.price
        entity.commission = product.commission
        entity.rating = product.rating
        entity.sales = product.sales
        entity.stock = product.stock

        entity.score = product.score
        entity.decision = product.decision
        entity.ranking = product.ranking

        return entity