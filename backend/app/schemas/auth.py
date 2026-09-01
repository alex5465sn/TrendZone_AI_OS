"""
TrendZone AI OS
================================

Auth Schemas

Schemas para autenticação e autorização.
"""

from pydantic import BaseModel, EmailStr, Field


# =====================================================
# LOGIN
# =====================================================

class LoginRequest(BaseModel):
    """Requisição de login."""

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=255,
    )


class LoginResponse(BaseModel):
    """Resposta de login."""

    access_token: str

    refresh_token: str

    token_type: str = "bearer"

    user: dict


# =====================================================
# REGISTER
# =====================================================

class RegisterRequest(BaseModel):
    """Requisição de registro."""

    name: str = Field(
        min_length=3,
        max_length=120,
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=255,
    )

    company: str = ""


class RegisterResponse(BaseModel):
    """Resposta de registro."""

    id: int

    uuid: str

    name: str

    email: str

    role: str

    plan: str


# =====================================================
# REFRESH TOKEN
# =====================================================

class RefreshTokenRequest(BaseModel):
    """Requisição de refresh token."""

    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Resposta de refresh token."""

    access_token: str

    token_type: str = "bearer"


# =====================================================
# USER INFO
# =====================================================

class UserInfo(BaseModel):
    """Informações do usuário autenticado."""

    id: int

    uuid: str

    name: str

    email: str

    role: str

    plan: str

    company: str

    avatar: str

    is_active: bool
