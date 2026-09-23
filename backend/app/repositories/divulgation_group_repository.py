"""
TrendZone AI OS

Repository da entidade DivulgationGroup.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.divulgation_group import DivulgationGroup
from app.repositories.base_repository import BaseRepository


class DivulgationGroupRepository(BaseRepository[DivulgationGroup]):

    model = DivulgationGroup

    @classmethod
    def get_all_active(cls, db: Session) -> list[DivulgationGroup]:
        stmt = (
            select(DivulgationGroup)
            .where(DivulgationGroup.is_active.is_(True))
            .order_by(DivulgationGroup.platform, DivulgationGroup.name)
        )
        return list(db.execute(stmt).scalars().all())
