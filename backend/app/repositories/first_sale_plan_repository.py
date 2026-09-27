"""
Repository para FirstSalePlan.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.first_sale_plan import FirstSalePlan
from app.repositories.base_repository import BaseRepository


class FirstSalePlanRepository(BaseRepository[FirstSalePlan]):
    model = FirstSalePlan

    @classmethod
    def get_by_user(cls, db: Session, user_id: int) -> FirstSalePlan | None:
        stmt = select(FirstSalePlan).where(FirstSalePlan.user_id == user_id)
        return db.execute(stmt).scalars().first()

    @classmethod
    def get_or_create(cls, db: Session, user_id: int) -> FirstSalePlan:
        plan = cls.get_by_user(db, user_id)
        if not plan:
            plan = FirstSalePlan(user_id=user_id)
            db.add(plan)
            db.commit()
            db.refresh(plan)
        return plan

    @classmethod
    def update_metrics(
        cls,
        db: Session,
        plan: FirstSalePlan,
        total_clicks: int,
        total_conversions: int,
        posts_published: int,
    ) -> FirstSalePlan:
        plan.total_clicks = total_clicks
        plan.total_conversions = total_conversions
        plan.posts_published = posts_published

        if total_clicks > 0:
            plan.conversion_rate = round(total_conversions / total_clicks, 4)

        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan
