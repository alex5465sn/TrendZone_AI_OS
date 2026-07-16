"""
TrendZone AI OS
================================

User Service.

Responsável pelas regras de negócio
dos usuários do sistema.
"""

from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository

from app.schemas.user import UserCreate

from app.security.hash import hash_password

from app.services.base_service import BaseService

from app.core.exceptions import (
    UserAlreadyExists,
    UserNotFound,
)


class UserService(BaseService):

    SERVICE_NAME = "USER_SERVICE"

    # =====================================================
    # CREATE
    # =====================================================

    @classmethod
    def create(
        cls,
        db: Session,
        data: UserCreate,
    ):

        cls.log_info(
            "Criando usuário..."
        )

        existing = UserRepository.get_by_email(
            db,
            data.email,
        )

        if existing:

            cls.log_warning(
                "Usuário já cadastrado."
            )

            raise UserAlreadyExists()

        password = hash_password(
            data.password
        )

        user = UserRepository.create(

            db=db,

            name=data.name,

            email=data.email,

            password_hash=password,

        )

        cls.log_success(
            "Usuário criado."
        )

        return user

    # =====================================================
    # GET
    # =====================================================

    @classmethod
    def get_all(
        cls,
        db: Session,
    ):

        return UserRepository.get_all(db)

    @classmethod
    def get_by_email(
        cls,
        db: Session,
        email: str,
    ):

        user = UserRepository.get_by_email(
            db,
            email,
        )

        if not user:

            raise UserNotFound()

        return user