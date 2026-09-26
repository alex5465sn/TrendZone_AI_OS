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

from app.services.persistence_service import (
    PersistenceService,
)

from app.services.executive_report import (
    ExecutiveReport,
)

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.constants.categories import keyword_to_category


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

        products.sort(key=lambda p: p.score, reverse=True)

        PersistenceService.save_products(

            self.db,

            products,

        )

        self._sync_to_products_table(products, keyword)

        return self._build_reports(products)

    # =====================================================
    # SINCRONIZA COM A TABELA "products"
    # =====================================================
    # A tabela "trend_products" (PersistenceService) guarda o
    # historico bruto do Scout. Porem, Oportunidades, Descoberta,
    # Funil e Automacao leem da tabela "products". Sem este passo
    # os produtos encontrados pelo Scout nunca alimentavam a IA.

    def _sync_to_products_table(self, products, keyword: str = "") -> None:

        category = keyword_to_category(keyword)

        for product in products:

            existing = ProductRepository.get_by_item_id(
                self.db,
                product.item_id,
            )

            if existing:

                existing.name = product.name
                existing.image = product.image
                existing.offer_link = product.offer_link
                existing.price = product.price
                existing.commission = product.commission
                existing.rating = product.rating
                existing.sales = product.sales
                existing.base_score = product.score
                # Preserva o ajuste de performance real ja calculado
                # (ver ProductPerformanceScore) em vez de apagar o
                # aprendizado a cada nova busca do Scout.
                existing.score = round(
                    existing.base_score + (existing.performance_adjustment or 0.0), 2
                )
                existing.recommendation = DecisionEngine.classify(
                    {"score": existing.score}
                )
                existing.category = category

                ProductRepository.update(self.db, existing)

                continue

            entity = Product(
                item_id=product.item_id,
                shop_id=product.shop_id,
                name=product.name,
                image=product.image,
                offer_link=product.offer_link,
                price=product.price,
                commission=product.commission,
                rating=product.rating,
                sales=product.sales,
                score=product.score,
                base_score=product.score,
                performance_adjustment=0.0,
                recommendation=product.decision,
                category=category,
            )

            ProductRepository.create(self.db, entity)

    def _build_reports(self, products):

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