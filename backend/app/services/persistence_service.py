"""
TrendZone AI OS
================================

Persistence Service

Responsável pela persistência dos
produtos analisados pelo TrendZone AI OS.

Esta camada converte o modelo de domínio
(TrendProduct) para a entidade SQLAlchemy
(TrendProductEntity) utilizando o Mapper.

Fluxo

TrendProduct
      ↓
TrendProductEntityMapper
      ↓
TrendProductEntity
      ↓
TrendProductRepository
      ↓
Banco de Dados
"""

from sqlalchemy.orm import Session

from app.domain.product import TrendProduct

from app.mappers.trend_product_entity_mapper import (
    TrendProductEntityMapper,
)

from app.models.trend_product_entity import (
    TrendProductEntity,
)

from app.repositories.trend_product_repository import (
    TrendProductRepository,
)

from app.services.base_service import BaseService


class PersistenceService(BaseService):
    """
    Serviço responsável pela persistência
    dos produtos do domínio.
    """

    SERVICE_NAME = "PERSISTENCE_SERVICE"

    # =====================================================
    # SAVE PRODUCT
    # =====================================================

    @classmethod
    def save_product(
        cls,
        db: Session,
        product: TrendProduct,
    ) -> TrendProductEntity:

        cls.log_info(
            f"Persistindo produto: {product.name}"
        )

        entity = TrendProductEntityMapper.to_entity(
            product
        )

        entity = TrendProductRepository.save(
            db=db,
            entity=entity,
        )

        cls.log_success(
            f"Produto persistido: {product.name}"
        )

        return entity

    # =====================================================
    # SAVE PRODUCTS
    # =====================================================

    @classmethod
    def save_products(
        cls,
        db: Session,
        products: list[TrendProduct],
    ) -> list[TrendProductEntity]:

        cls.log_info(
            f"Persistindo {len(products)} produto(s)..."
        )

        entities: list[TrendProductEntity] = []

        for product in products:

            entity = cls.save_product(
                db=db,
                product=product,
            )

            entities.append(entity)

        cls.log_success(
            f"{len(entities)} produto(s) persistido(s) com sucesso."
        )

        return entities

    # =====================================================
    # GET ALL
    # =====================================================

    @classmethod
    def get_all(
        cls,
        db: Session,
    ) -> list[TrendProductEntity]:

        cls.log_info(
            "Buscando produtos persistidos..."
        )

        return TrendProductRepository.get_all(db)

    # =====================================================
    # TOP SCORE
    # =====================================================

    @classmethod
    def top_score(
        cls,
        db: Session,
        limit: int = 10,
    ) -> list[TrendProductEntity]:

        cls.log_info(
            f"Buscando Top {limit} Score..."
        )

        return TrendProductRepository.top_score(
            db=db,
            limit=limit,
        )

    # =====================================================
    # TOP RANKING
    # =====================================================

    @classmethod
    def top_ranking(
        cls,
        db: Session,
        limit: int = 10,
    ) -> list[TrendProductEntity]:

        cls.log_info(
            f"Buscando Top {limit} Ranking..."
        )

        return TrendProductRepository.top_ranking(
            db=db,
            limit=limit,
        )

    # =====================================================
    # PROMOTED
    # =====================================================

    @classmethod
    def promoted(
        cls,
        db: Session,
    ) -> list[TrendProductEntity]:

        cls.log_info(
            "Buscando produtos promovidos..."
        )

        return TrendProductRepository.promoted(db)

    # =====================================================
    # COUNT
    # =====================================================

    @classmethod
    def count(
        cls,
        db: Session,
    ) -> int:

        return TrendProductRepository.count(db)