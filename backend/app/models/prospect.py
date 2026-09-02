from sqlalchemy import (
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import BaseModel


class Prospect(BaseModel):
    __tablename__ = "prospects"

    nicho: Mapped[str] = mapped_column(String(200), nullable=False)
    cidade: Mapped[str] = mapped_column(String(200), default="")
    busca: Mapped[str] = mapped_column(String(500), default="")
    nome: Mapped[str] = mapped_column(String(300), default="")
    score: Mapped[int] = mapped_column(Integer, default=0)
    temperatura: Mapped[str] = mapped_column(String(20), default="frio")
    abordagem: Mapped[str] = mapped_column(Text, default="")
    dossie: Mapped[str] = mapped_column(Text, default="")
    canal_sugerido: Mapped[str] = mapped_column(String(200), default="")
    status: Mapped[str] = mapped_column(String(30), default="novo")
    produto_ids: Mapped[str] = mapped_column(Text, default="")
    qtd_produtos: Mapped[int] = mapped_column(Integer, default=0)
    preco_medio: Mapped[float] = mapped_column(Float, default=0.0)
    comissao_media: Mapped[float] = mapped_column(Float, default=0.0)
    vendas_total: Mapped[int] = mapped_column(Integer, default=0)
