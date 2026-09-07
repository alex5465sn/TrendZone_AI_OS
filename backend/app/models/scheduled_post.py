from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseModel


class ScheduledPost(BaseModel):
    __tablename__ = "scheduled_posts"

    product_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    link: Mapped[str] = mapped_column(String(500), default="")
    image_url: Mapped[str] = mapped_column(String(1000), default="")
    video_path: Mapped[str] = mapped_column(String(500), default="")
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pendente")
    error_message: Mapped[str] = mapped_column(String(500), default="")
