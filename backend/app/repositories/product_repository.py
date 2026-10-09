"""
TrendZone AI OS
================================

Repository responsável pela entidade Product.

Toda regra de negócio deve permanecer
na camada Service.

Este Repository apenas acessa o banco.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Repository da entidade Product.

    Toda criação/atualização grava um ProductSnapshot
    (deduplicado no MomentumService) — é esse histórico
    que alimenta o cálculo de momentum do Product Radar.
    """

    model = Product

    @classmethod
    def create(cls, db: Session, obj: Product) -> Product:
        entity = super().create(db, obj)

        cls._snapshot(db, entity)

        return entity

    @classmethod
    def update(cls, db: Session, obj: Product) -> Product:
        entity = super().update(db, obj)

        cls._snapshot(db, entity)

        return entity

    @staticmethod
    def _snapshot(db: Session, entity: Product) -> None:
        # Import local evita import circular
        # (momentum_service -> models -> ...).
        from app.services.momentum_service import MomentumService

        MomentumService.record(db, entity)

    # =====================================================
    # ITEM ID
    # =====================================================

    @classmethod
    def get_by_item_id(
        cls,
        db: Session,
        item_id: int,
    ) -> Product | None:

        stmt = (
            select(Product)
            .where(
                Product.item_id == item_id,
                Product.is_active.is_(True),
            )
        )

        return db.execute(stmt).scalar_one_or_none()

    # =====================================================
    # CATEGORY
    # =====================================================

    @classmethod
    def get_by_category(
        cls,
        db: Session,
        category: str,
    ) -> list[Product]:

        stmt = (
            select(Product)
            .where(
                Product.category == category,
                Product.is_active.is_(True),
            )
            .order_by(Product.score.desc())
        )

        return list(db.execute(stmt).scalars().all())

    # =====================================================
    # SEARCH
    # =====================================================

    @classmethod
    def search(
        cls,
        db: Session,
        text: str,
    ) -> list[Product]:

        stmt = (
            select(Product)
            .where(
                Product.name.ilike(f"%{text}%"),
                Product.is_active.is_(True),
            )
            .order_by(Product.score.desc())
        )

        return list(db.execute(stmt).scalars().all())

    # =====================================================
    # TOP SCORE
    # =====================================================

    @classmethod
    def get_top_score(
        cls,
        db: Session,
        limit: int = 10,
        exclude_item_ids: set[int] | None = None,
    ) -> list[Product]:

        stmt = (
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.score.desc())
        )

        if exclude_item_ids:
            stmt = stmt.where(Product.item_id.notin_(exclude_item_ids))

        stmt = stmt.limit(limit)

        return list(db.execute(stmt).scalars().all())

    # =====================================================
    # TOP SALES
    # =====================================================

    @classmethod
    def get_top_sales(
        cls,
        db: Session,
        limit: int = 10,
    ) -> list[Product]:

        stmt = (
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.sales.desc())
            .limit(limit)
        )

        return list(db.execute(stmt).scalars().all())
