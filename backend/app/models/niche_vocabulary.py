from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import BaseModel


class NicheVocabulary(BaseModel):

    __tablename__ = "niche_vocabularies"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    niche_name: Mapped[str] = mapped_column(
        String(100),
        default="E-commerce",
    )

    term_lead: Mapped[str] = mapped_column(
        String(50),
        default="Lead",
    )

    term_prospect: Mapped[str] = mapped_column(
        String(50),
        default="Prospect",
    )

    term_customer: Mapped[str] = mapped_column(
        String(50),
        default="Cliente",
    )

    term_deal: Mapped[str] = mapped_column(
        String(50),
        default="Oportunidade",
    )

    term_hot: Mapped[str] = mapped_column(
        String(50),
        default="Quente",
    )

    term_cold: Mapped[str] = mapped_column(
        String(50),
        default="Frio",
    )
