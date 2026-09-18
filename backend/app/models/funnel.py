from sqlalchemy import (
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import BaseModel


class FunnelStage(BaseModel):

    __tablename__ = "funnel_stages"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    color: Mapped[str] = mapped_column(
        String(20),
        default="#2563EB",
    )

    position: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )


class FunnelCard(BaseModel):

    __tablename__ = "funnel_cards"

    stage_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("funnel_stages.id"),
        nullable=False,
    )

    product_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("products.id"),
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="MEDIUM",
    )

    position: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    estimated_revenue: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    channel: Mapped[str] = mapped_column(
        String(100),
        default="",
    )

    notes: Mapped[str] = mapped_column(
        Text,
        default="",
    )
