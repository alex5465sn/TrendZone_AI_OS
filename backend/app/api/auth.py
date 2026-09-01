"""
TrendZone AI OS
================================

Auth API

Endpoints de autenticação.
"""

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    LoginResponse,
    RegisterResponse,
    UserInfo,
)
from app.services.auth_service import AuthService
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=dict)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    """Registra um novo usuário."""

    user = AuthService.register(db, data)

    return ResponseBuilder.success(
        data=user.model_dump(),
        message="Usuário registrado com sucesso.",
        status_code=201,
    )


@router.post("/login", response_model=dict)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    """Faz login de um usuário."""

    response = AuthService.login(db, data)

    return ResponseBuilder.success(
        data=response.model_dump(),
        message="Login realizado com sucesso.",
    )


@router.post("/refresh", response_model=dict)
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """Renova o access token."""

    access_token = AuthService.refresh_access_token(
        db,
        data.refresh_token,
    )

    return ResponseBuilder.success(
        data={
            "access_token": access_token,
            "token_type": "bearer",
        },
        message="Token renovado com sucesso.",
    )


@router.get("/me", response_model=dict)
def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    """Retorna as informações do usuário autenticado."""

    if not authorization or not authorization.startswith("Bearer "):
        return ResponseBuilder.error(
            message="Token não fornecido.",
            status_code=401,
        )

    token = authorization.replace("Bearer ", "")

    user = AuthService.get_current_user(db, token)

    return ResponseBuilder.success(
        data=UserInfo(
            id=user.id,
            uuid=user.uuid,
            name=user.name,
            email=user.email,
            role=user.role,
            plan=user.plan,
            company=user.company,
            avatar=user.avatar,
            is_active=user.is_active,
        ).model_dump(),
    )
