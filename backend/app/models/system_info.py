"""
TrendZone AI OS

Model responsável pelas informações
institucionais do sistema.

Armazena informações gerais da instalação.
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


class SystemInfo(BaseModel):
    """
    Informações do sistema.
    """

    __tablename__ = "system_info"

    __table_args__ = (

        Index("idx_system_uuid", "uuid"),

        Index("idx_system_app", "app_name"),

    )

    app_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="ONLINE",
    )

    environment: Mapped[str] = mapped_column(
        String(20),
        default="development",
    )