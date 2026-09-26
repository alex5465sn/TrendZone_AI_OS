"""
TrendZone AI OS

Model responsável pelos produtos
monitorados pelo sistema.

Atualmente suporta Shopee.

Arquitetura preparada para:

- Mercado Livre
- Amazon
- Magalu
- AliExpress
- TikTok Shop

Todos os produtos da plataforma
deverão utilizar este Model.
"""

from sqlalchemy import (
    Float,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import BaseModel


class Product(BaseModel):
    """
    Produto monitorado pelo TrendZone AI OS.
    """

    __tablename__ = "products"

    __table_args__ = (

        Index("idx_product_uuid", "uuid"),

        Index("idx_product_marketplace", "marketplace"),

        Index("idx_product_item", "item_id"),

        Index("idx_product_category", "category"),

        Index("idx_product_shop", "shop_id"),

        Index("idx_product_score", "score"),

        Index("idx_product_sales", "sales"),

        Index("idx_product_rating", "rating"),

        Index("idx_product_created", "created_at"),

        UniqueConstraint(
            "marketplace",
            "item_id",
            name="uq_product_marketplace_item",
        ),

    )

    # =====================================================
    # Marketplace
    # =====================================================

    marketplace: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="shopee",
    )

    item_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    shop_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
        default="geral",
    )

    # =====================================================
    # Informações Comerciais
    # =====================================================

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    image: Mapped[str] = mapped_column(
        String(700),
        default="",
    )

    offer_link: Mapped[str] = mapped_column(
        String(700),
        default="",
    )

    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    commission: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0,
    )

    # =====================================================
    # Indicadores
    # =====================================================

    rating: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    sales: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # =====================================================
    # Inteligência Artificial
    # =====================================================

    score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    base_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    performance_adjustment: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    recommendation: Mapped[str] = mapped_column(
        String(30),
        default="OBSERVAR",
    )