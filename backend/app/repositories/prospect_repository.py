from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.prospect import Prospect
from app.repositories.base_repository import BaseRepository


class ProspectRepository(BaseRepository[Prospect]):
    model = Prospect

    @classmethod
    def get_by_status(cls, db: Session, status: str) -> list[Prospect]:
        stmt = (
            select(Prospect)
            .where(Prospect.status == status, Prospect.is_active.is_(True))
            .order_by(Prospect.score.desc())
        )
        return list(db.execute(stmt).scalars().all())

    @classmethod
    def get_by_temperatura(cls, db: Session, temp: str) -> list[Prospect]:
        stmt = (
            select(Prospect)
            .where(Prospect.temperatura == temp, Prospect.is_active.is_(True))
            .order_by(Prospect.score.desc())
        )
        return list(db.execute(stmt).scalars().all())
