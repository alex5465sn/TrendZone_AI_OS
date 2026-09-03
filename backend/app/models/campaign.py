"""
TrendZone AI OS

Model responsável pelas campanhas de venda
geradas pela IA (Motor de Oportunidades).

Uma Campanha representa o conteúdo de divulgação
gerado para um produto (título, legenda, hashtags,
público-alvo e canal sugerido).

O envio/publicação é sempre confirmado por um
humano (usuário/admin) — o sistema não publica
nem envia mensagens de forma autônoma.
"""

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


class Campaign(BaseModel):
    """
    Campanha de venda gerada pela IA.
    """

    __tablename__ = "campaigns"

    marketplace: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="shopee",
    )

    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    caption: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    hashtags: Mapped[str] = mapped_column(
        String(500),
        default="",
    )

    target_audience: Mapped[str] = mapped_column(
        String(255),
        default="",
    )

    channel: Mapped[str] = mapped_column(
        String(100),
        default="",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="DRAFT",
    )

    tracking_link: Mapped[str] = mapped_column(
        String(500),
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
        default=0.0,
    )
