from datetime import datetime

from sqlalchemy import (
    DateTime,
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


class FollowUp(BaseModel):

    __tablename__ = "follow_ups"

    card_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("funnel_cards.id"),
        nullable=True,
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

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    due_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="MEDIUM",
    )
