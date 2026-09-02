from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import BaseModel


class Schedule(BaseModel):
    __tablename__ = "schedules"

    nicho: Mapped[str] = mapped_column(String(200), nullable=False)
    cidade: Mapped[str] = mapped_column(String(200), default="")
    hora: Mapped[str] = mapped_column(String(5), default="09:00")
    dias: Mapped[str] = mapped_column(String(50), default="todos")
    quantos: Mapped[int] = mapped_column(Integer, default=5)
    ultimo_run: Mapped[str] = mapped_column(String(20), default="")
    status: Mapped[str] = mapped_column(String(20), default="ativo")
