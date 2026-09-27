"""
TrendZone AI OS

Modelo para rastreamento do Plano de Primeira Venda.

Consolida checklist de preparação, execução diária,
e métricas de progresso em direção à primeira venda.
"""

from sqlalchemy import Integer, String, Text, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database.base import BaseModel


class FirstSalePlan(BaseModel):
    """Plano de primeira venda com checklist e métricas."""

    __tablename__ = "first_sale_plans"

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Configuração do plano
    selected_niche: Mapped[str] = mapped_column(String(100), default="")
    selected_niche_keywords: Mapped[str] = mapped_column(Text, default="")

    # Checklist Semana 1
    niche_validated: Mapped[bool] = mapped_column(Boolean, default=False)
    champion_products_identified: Mapped[int] = mapped_column(Integer, default=0)
    whatsapp_groups_count: Mapped[int] = mapped_column(Integer, default=0)
    facebook_groups_count: Mapped[int] = mapped_column(Integer, default=0)
    groups_registered: Mapped[bool] = mapped_column(Boolean, default=False)

    # Execução Semanas 2-3
    posts_published: Mapped[int] = mapped_column(Integer, default=0)
    total_clicks: Mapped[int] = mapped_column(Integer, default=0)
    total_conversions: Mapped[int] = mapped_column(Integer, default=0)
    first_sale_achieved: Mapped[bool] = mapped_column(Boolean, default=False)
    first_sale_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    first_sale_product: Mapped[str] = mapped_column(String(300), default="")
    first_sale_channel: Mapped[str] = mapped_column(String(50), default="")

    # Métricas
    avg_ctr: Mapped[float] = mapped_column(Float, default=0.0)
    conversion_rate: Mapped[float] = mapped_column(Float, default=0.0)
    estimated_commission: Mapped[float] = mapped_column(Float, default=0.0)

    # Status
    current_phase: Mapped[str] = mapped_column(
        String(20), default="preparation"
    )  # preparation, execution, optimization
    phase_started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Notas
    notes: Mapped[str] = mapped_column(Text, default="")
