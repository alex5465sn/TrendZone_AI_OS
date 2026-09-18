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


class SeasonalEvent(BaseModel):

    __tablename__ = "seasonal_events"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    event_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    prep_start: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        default="",
    )

    niches: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    strategy_notes: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PLANNED",
    )
