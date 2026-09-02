from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.schedule import Schedule
from app.repositories.base_repository import BaseRepository


class ScheduleRepository(BaseRepository[Schedule]):
    model = Schedule

    @classmethod
    def get_active(cls, db: Session) -> list[Schedule]:
        stmt = (
            select(Schedule)
            .where(Schedule.status == "ativo", Schedule.is_active.is_(True))
            .order_by(Schedule.created_at.desc())
        )
        return list(db.execute(stmt).scalars().all())
