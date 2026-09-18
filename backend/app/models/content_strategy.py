from sqlalchemy import (
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


class ContentStrategy(BaseModel):

    __tablename__ = "content_strategies"

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

    content_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    script: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    hashtags: Mapped[str] = mapped_column(
        String(500),
        default="",
    )

    cta: Mapped[str] = mapped_column(
        String(255),
        default="",
    )

    best_time: Mapped[str] = mapped_column(
        String(50),
        default="",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="DRAFT",
    )

    performance_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
