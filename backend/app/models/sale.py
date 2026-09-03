from sqlalchemy import (
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import BaseModel


class Sale(BaseModel):
    __tablename__ = "sales"

    conversion_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False,
    )
    order_id: Mapped[str] = mapped_column(String(100), default="")
    order_status: Mapped[str] = mapped_column(String(50), default="")
    shop_type: Mapped[str] = mapped_column(String(50), default="")
    buyer_type: Mapped[str] = mapped_column(String(50), default="")
    device: Mapped[str] = mapped_column(String(50), default="")
    product_type: Mapped[str] = mapped_column(String(100), default="")
    click_time: Mapped[str] = mapped_column(String(30), default="")
    purchase_time: Mapped[str] = mapped_column(String(30), default="")
    total_commission: Mapped[float] = mapped_column(Float, default=0.0)
    seller_commission: Mapped[float] = mapped_column(Float, default=0.0)
    shopee_commission: Mapped[float] = mapped_column(Float, default=0.0)
    net_commission: Mapped[float] = mapped_column(Float, default=0.0)
    utm_content: Mapped[str] = mapped_column(String(200), default="")
    status: Mapped[str] = mapped_column(String(30), default="pendente")
