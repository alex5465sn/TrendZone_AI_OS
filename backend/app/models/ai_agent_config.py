from sqlalchemy import (
    Boolean,
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


class AIAgentConfig(BaseModel):

    __tablename__ = "ai_agent_configs"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    auto_reply_whatsapp: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    provider: Mapped[str] = mapped_column(
        String(30),
        default="abacus",
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        default="gpt-4o",
    )

    system_prompt: Mapped[str] = mapped_column(
        Text,
        default="Você é um assistente de vendas do TrendZone. Responda de forma curta, simpática e objetiva, ajudando o cliente a decidir a compra do produto anunciado.",
    )
