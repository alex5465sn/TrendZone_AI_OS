"""
TrendZone AI OS
================================

Trend Product Entity

Entidade oficial utilizada para
persistência dos produtos analisados
pelo TrendZone AI OS.
"""

from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    Float,
    DateTime,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class TrendProductEntity(Base):

    __tablename__ = "trend_products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    item_id: Mapped[int] = mapped_column(
        Integer,
        index=True,
    )

    shop_id: Mapped[int] = mapped_column(
        Integer,
        index=True,
    )

    marketplace: Mapped[str] = mapped_column(
        String(30),
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
    )

    image: Mapped[str] = mapped_column(
        String(500),
        default="",
    )

    category: Mapped[str] = mapped_column(
        String(120),
        default="",
    )

    offer_link: Mapped[str] = mapped_column(
        String(500),
        default="",
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="BRL",
    )

    price: Mapped[float] = mapped_column(
        Float,
    )

    commission: Mapped[float] = mapped_column(
        Float,
    )

    rating: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    sales: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    decision: Mapped[str] = mapped_column(
        String(40),
        default="",
    )

    ranking: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )