"""
TrendZone AI OS
===============================

Schemas responsáveis pelos Usuários.

Representam o contrato entre
Frontend, API e Banco de Dados.
"""

from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


# =====================================================
# CREATE
# =====================================================

class UserCreate(BaseModel):
    """
    Cadastro de usuário.
    """

    name: str = Field(
        min_length=3,
        max_length=120,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=255,
    )


# =====================================================
# UPDATE
# =====================================================

class UserUpdate(BaseModel):
    """
    Atualização parcial.
    """

    name: str | None = None

    email: EmailStr | None = None

    password: str | None = None

    company: str | None = None

    avatar: str | None = None

    role: str | None = None

    plan: str | None = None

    is_active: bool | None = None


# =====================================================
# RESPONSE
# =====================================================

class UserResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    uuid: str

    name: str

    email: EmailStr

    company: str

    avatar: str

    role: str

    plan: str

    is_active: bool

    created_at: datetime

    updated_at: datetime


# =====================================================
# LIST RESPONSE
# =====================================================

class UserListResponse(BaseModel):

    items: list[UserResponse]

    total: int

    page: int

    page_size: int