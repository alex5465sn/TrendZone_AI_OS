"""
TrendZone AI OS
================================

User Repository

Responsável pelo acesso aos dados de usuários.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository da entidade User."""

    model = User

    # =====================================================
    # GET BY EMAIL
    # =====================================================

    @classmethod
    def get_by_email(
        cls,
        db: Session,
        email: str,
    ) -> User | None:

        stmt = (
            select(User)
            .where(
                User.email == email,
                User.is_active.is_(True),
            )
        )

        return db.execute(stmt).scalar_one_or_none()

    # =====================================================
    # GET BY ROLE
    # =====================================================

    @classmethod
    def get_by_role(
        cls,
        db: Session,
        role: str,
    ) -> list[User]:

        stmt = (
            select(User)
            .where(
                User.role == role,
                User.is_active.is_(True),
            )
        )

        return list(db.execute(stmt).scalars().all())

    # =====================================================
    # GET ADMINS
    # =====================================================

    @classmethod
    def get_admins(
        cls,
        db: Session,
    ) -> list[User]:

        return cls.get_by_role(db, "ADMIN")
