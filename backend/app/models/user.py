"""
TrendZone AI OS

Model responsável pelos usuários do sistema.

Este Model representa qualquer usuário
autenticado na plataforma.

Preparado para:

- Multi Tenant
- Planos
- Controle de Permissões
- Assinaturas
- Equipes
"""

from sqlalchemy import (
    Index,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import BaseModel


class User(BaseModel):
    """
    Usuário do TrendZone AI OS.
    """

    __tablename__ = "users"

    __table_args__ = (

        Index("idx_user_uuid", "uuid"),

        Index("idx_user_email", "email"),

        Index("idx_user_plan", "plan"),

        Index("idx_user_created", "created_at"),

    )

    # =====================================================
    # Dados Pessoais
    # =====================================================

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # =====================================================
    # SaaS
    # =====================================================

    plan: Mapped[str] = mapped_column(
        String(30),
        default="FREE",
    )

    role: Mapped[str] = mapped_column(
        String(30),
        default="USER",
    )

    company: Mapped[str] = mapped_column(
        String(120),
        default="",
    )

    avatar: Mapped[str] = mapped_column(
        String(500),
        default="",
    )