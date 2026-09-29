from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseModel


class PublishedPost(BaseModel):
    __tablename__ = "published_posts"

    tracking_code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    product_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_name: Mapped[str] = mapped_column(String(300), default="")
    product_image: Mapped[str] = mapped_column(String(500), default="")
    destination_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    channel: Mapped[str] = mapped_column(String(30), default="facebook")
    post_format: Mapped[str] = mapped_column(String(20), default="texto")
    message: Mapped[str] = mapped_column(Text, default="")
    click_count: Mapped[int] = mapped_column(Integer, default=0)
