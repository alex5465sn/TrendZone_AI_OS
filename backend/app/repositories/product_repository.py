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
    """

    model = Product

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
    ) -> list[Product]:

        stmt = (
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.score.desc())
            .limit(limit)
        )

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
