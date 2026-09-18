from sqlalchemy import (
    ForeignKey,
    Integer,
    Float,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import BaseModel


class ChannelTracking(BaseModel):

    __tablename__ = "channel_trackings"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    product_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("products.id"),
        nullable=True,
    )

    channel: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    sub_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    tracking_url: Mapped[str] = mapped_column(
        String(700),
        default="",
    )

    clicks: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    conversions: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    revenue: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    ctr: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )
