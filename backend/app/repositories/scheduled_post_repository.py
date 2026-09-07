from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.scheduled_post import ScheduledPost
from app.repositories.base_repository import BaseRepository


class ScheduledPostRepository(BaseRepository[ScheduledPost]):
    model = ScheduledPost

    @classmethod
    def get_due(cls, db: Session, now: datetime) -> list[ScheduledPost]:
        stmt = (
            select(ScheduledPost)
            .where(
                ScheduledPost.status == "pendente",
                ScheduledPost.scheduled_at <= now,
                ScheduledPost.is_active.is_(True),
            )
            .order_by(ScheduledPost.scheduled_at.asc())
        )
        return list(db.execute(stmt).scalars().all())

    @classmethod
    def get_all_ordered(cls, db: Session) -> list[ScheduledPost]:
        stmt = (
            select(ScheduledPost)
            .where(ScheduledPost.is_active.is_(True))
            .order_by(ScheduledPost.scheduled_at.asc())
        )
        return list(db.execute(stmt).scalars().all())
