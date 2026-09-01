"""
TrendZone AI OS
================================

Trend Product Repository
"""

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.models.trend_product_entity import (
    TrendProductEntity,
)


class TrendProductRepository:

    @staticmethod
    def get_by_item(
        db: Session,
        item_id: int,
        marketplace: str,
    ):

        stmt = (

            select(
                TrendProductEntity
            )

            .where(
                TrendProductEntity.item_id == item_id
            )

            .where(
                TrendProductEntity.marketplace == marketplace
            )

        )

        return db.execute(
            stmt
        ).scalar_one_or_none()

    @staticmethod
    def create(
        db: Session,
        entity: TrendProductEntity,
    ):

        db.add(entity)

        db.commit()

        db.refresh(entity)

        return entity

    @staticmethod
    def update(
        db: Session,
        entity: TrendProductEntity,
    ):

        db.commit()

        db.refresh(entity)

        return entity

    @classmethod
    def save(
        cls,
        db: Session,
        entity: TrendProductEntity,
    ):

        existing = cls.get_by_item(

            db,

            entity.item_id,

            entity.marketplace,

        )

        if existing:

            existing.name = entity.name
            existing.image = entity.image
            existing.category = entity.category
            existing.offer_link = entity.offer_link

            existing.currency = entity.currency

            existing.price = entity.price
            existing.commission = entity.commission
            existing.rating = entity.rating
            existing.sales = entity.sales
            existing.stock = entity.stock

            existing.score = entity.score
            existing.decision = entity.decision
            existing.ranking = entity.ranking

            return cls.update(
                db,
                existing,
            )

        return cls.create(
            db,
            entity,
        )

    @staticmethod
    def get_all(
        db: Session,
    ):

        stmt = select(
            TrendProductEntity
        )

        return db.execute(
            stmt
        ).scalars().all()

    @staticmethod
    def top_score(
        db: Session,
        limit: int = 10,
    ):

        stmt = (

            select(
                TrendProductEntity
            )

            .order_by(
                TrendProductEntity.score.desc()
            )

            .limit(limit)

        )

        return db.execute(
            stmt
        ).scalars().all()

    @staticmethod
    def top_ranking(
        db: Session,
        limit: int = 10,
    ):

        stmt = (

            select(
                TrendProductEntity
            )

            .order_by(
                TrendProductEntity.ranking.asc()
            )

            .limit(limit)

        )

        return db.execute(
            stmt
        ).scalars().all()

    @staticmethod
    def promoted(
        db: Session,
    ):

        stmt = (

            select(
                TrendProductEntity
            )

            .where(
                TrendProductEntity.decision == "PROMOTE"
            )

        )

        return db.execute(
            stmt
        ).scalars().all()

    @staticmethod
    def count(
        db: Session,
    ) -> int:

        stmt = select(
            TrendProductEntity
        )

        return len(
            db.execute(
                stmt
            ).scalars().all()
        )