"""
TrendZone AI OS

Model Product Snapshot.

Histórico de estado dos produtos observados
pelo Auto Scout / Scout Pipeline.

Cada linha registra o estado comercial de um
produto (marketplace + item_id) em um instante
no tempo. Comparações entre snapshots geram o
MOMENTUM do produto — crescimento de vendas,
variação de preço — insumo do Product Radar
para separar produtos em ascensão de produtos
saturados.

A gravação é deduplicada (ver MomentumService):
sem mudança de valores em menos de 6 horas,
nenhum snapshot novo é criado.
"""

from sqlalchemy import (
    DateTime,
    Float,
    Index,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from datetime import datetime

from app.database.base import BaseModel


class ProductSnapshot(BaseModel):
    """
    Snapshot de estado de um produto monitorado.
    """

    __tablename__ = "product_snapshots"

    __table_args__ = (
        Index(
            "idx_snapshot_product_time",
            "marketplace",
            "item_id",
            "captured_at",
        ),
    )

    marketplace: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="shopee",
    )

    item_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    commission: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    rating: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    sales: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    captured_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
