"""
TrendZone AI OS

Model responsavel pelos grupos de divulgacao
(WhatsApp, Facebook) usados no Robo Divulgador
para facilitar a distribuicao manual do
conteudo gerado pela IA.
"""

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import BaseModel


class DivulgationGroup(BaseModel):
    __tablename__ = "divulgation_groups"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    platform: Mapped[str] = mapped_column(String(20), nullable=False, default="facebook")
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="geral")
    description: Mapped[str] = mapped_column(Text, default="")
    link: Mapped[str] = mapped_column(String(500), default="")
    best_time: Mapped[str] = mapped_column(String(50), default="")
    member_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="ativo")
