"""
TrendZone AI OS

Modelo para Notificações.

Rastreia todas as notificações enviadas ao usuário
(WhatsApp, Push, Email) para histórico e auditoria.
"""

from sqlalchemy import Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database.base import BaseModel


class Notification(BaseModel):
    """Notificação enviada ao usuário."""

    __tablename__ = "notifications"

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Tipo de notificação
    notification_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # whatsapp, push, email

    # Conteúdo
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    data: Mapped[str] = mapped_column(Text, default="")  # JSON com dados adicionais

    # Status
    sent: Mapped[bool] = mapped_column(Boolean, default=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Rastreamento
    related_entity_type: Mapped[str] = mapped_column(
        String(50), default=""
    )  # published_post, sale, etc
    related_entity_id: Mapped[int] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
