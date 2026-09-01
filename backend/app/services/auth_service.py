"""
TrendZone AI OS
================================

Auth Service

Responsável pela lógica de autenticação.
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    LoginResponse,
    RegisterResponse,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.exceptions import (
    InvalidCredentials,
    UserAlreadyExists,
    UserNotFound,
)
from app.services.base_service import BaseService


class AuthService(BaseService):

    SERVICE_NAME = "AUTH_SERVICE"

    # =====================================================
    # REGISTER
    # =====================================================

    @classmethod
    def register(
        cls,
        db: Session,
        data: RegisterRequest,
    ) -> RegisterResponse:

        cls.log_info("Registrando novo usuário...")

        existing = UserRepository.get_by_email(
            db,
            data.email,
        )

        if existing:
            cls.log_warning("Usuário já existe.")
            raise UserAlreadyExists()

        user = User(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
            company=data.company,
            role="USER",
            plan="FREE",
        )

        user = UserRepository.create(db, user)

        cls.log_success("Usuário registrado com sucesso.")

        return RegisterResponse(
            id=user.id,
            uuid=user.uuid,
            name=user.name,
            email=user.email,
            role=user.role,
            plan=user.plan,
        )

    # =====================================================
    # LOGIN
    # =====================================================

    @classmethod
    def login(
        cls,
        db: Session,
        data: LoginRequest,
    ) -> LoginResponse:

        cls.log_info("Autenticando usuário...")

        user = UserRepository.get_by_email(
            db,
            data.email,
        )

        if not user or not verify_password(
            data.password,
            user.password_hash,
        ):
            cls.log_warning("Credenciais inválidas.")
            raise InvalidCredentials()

        if not user.is_active:
            cls.log_warning("Usuário inativo.")
            raise InvalidCredentials()

        access_token = create_access_token(
            subject=user.uuid,
            role=user.role,
        )

        refresh_token = create_refresh_token(
            subject=user.uuid,
        )

        cls.log_success("Usuário autenticado com sucesso.")

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user={
                "id": user.id,
                "uuid": user.uuid,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "plan": user.plan,
                "company": user.company,
                "avatar": user.avatar,
            },
        )

    # =====================================================
    # REFRESH TOKEN
    # =====================================================

    @classmethod
    def refresh_access_token(
        cls,
        db: Session,
        refresh_token: str,
    ) -> str:

        cls.log_info("Renovando access token...")

        payload = decode_token(refresh_token)

        if not payload or payload.type != "refresh":
            cls.log_warning("Refresh token inválido.")
            raise InvalidCredentials()

        user = UserRepository.get_by_uuid(
            db,
            payload.sub,
        )

        if not user or not user.is_active:
            cls.log_warning("Usuário não encontrado ou inativo.")
            raise UserNotFound()

        access_token = create_access_token(
            subject=user.uuid,
            role=user.role,
        )

        cls.log_success("Access token renovado.")

        return access_token

    # =====================================================
    # GET USER
    # =====================================================

    @classmethod
    def get_current_user(
        cls,
        db: Session,
        token: str,
    ) -> User:

        payload = decode_token(token)

        if not payload:
            raise InvalidCredentials()

        user = UserRepository.get_by_uuid(
            db,
            payload.sub,
        )

        if not user or not user.is_active:
            raise UserNotFound()

        return user
