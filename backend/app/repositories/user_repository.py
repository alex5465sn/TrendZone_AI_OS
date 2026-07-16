"""
TrendZone AI OS
================================

Repository responsável pela entidade User.

Toda regra de autenticação, permissões,
JWT e validações pertencem aos Services.

Este Repository apenas acessa o banco.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository da entidade User.
    """

    model = User

    # =====================================================
    # EMAIL
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
    # LOGIN
    # =====================================================

    @classmethod
    def exists_email(
        cls,
        db: Session,
        email: str,
    ) -> bool:

        return cls.exists(
            db,
            email=email,
        )