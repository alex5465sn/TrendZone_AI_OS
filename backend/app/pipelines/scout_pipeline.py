"""
TrendZone AI OS
================================

Scout Pipeline

Pipeline oficial de prospecção
do TrendZone AI OS.
"""

from sqlalchemy.orm import Session

from app.integrations.shopee.services.product_service import (
    ShopeeProductService,
)

from app.mappers.trend_product_mapper import (
    TrendProductMapper,
)

from app.services.product_validator import (
    ProductValidator,
)

from app.services.product_score import (
    ProductScore,
)

from app.services.decision_engine import (
    DecisionEngine,
)

from app.services.ranking_engine import (
    RankingEngine,
)

from app.services.persistence_service import (
    PersistenceService,
)

from app.services.executive_report import (
    ExecutiveReport,
)


class ScoutPipeline:

    def __init__(

        self,

        db: Session,

    ):

        self.db = db

        self.product_service = ShopeeProductService()

    # =====================================================
    # RUN
    # =====================================================

    def run(

        self,

        keyword: str = "",

        page: int = 1,

        limit: int = 20,

    ):

        dto_products = self.product_service.search_products(

            keyword=keyword,

            page=page,

            limit=limit,

        )

        products = [

            TrendProductMapper.from_shopee(dto)

            for dto in dto_products

        ]

        for product in products:

            ProductValidator.validate(

                {

                    "item_id": product.item_id,

                    "shop_id": product.shop_id,

                    "name": product.name,

                    "price": product.price,

                    "commission": product.commission,

                    "rating": product.rating,

                    "sales": product.sales,

                }

            )

            product.score = ProductScore.calculate(

                commission=product.commission,

                rating=product.rating,

                sales=product.sales,

            )

            product.decision = DecisionEngine.classify(

                {

                    "score": product.score,

                }

            )

        RankingEngine.rank(products)

        PersistenceService.save_products(

            self.db,

            products,

        )

        return [

            ExecutiveReport.build(

                {

                    "name": product.name,

                    "score": product.score,

                    "decision": product.decision,

                    "commission": product.commission,

                    "rating": product.rating,

                    "sales": product.sales,

                    "price": product.price,

                }

            )

            for product in products

        ]