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


class WhatsAppConnection(BaseModel):

    __tablename__ = "whatsapp_connections"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    session_name: Mapped[str] = mapped_column(
        String(100),
        default="default",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="disconnected",
    )

    phone_number: Mapped[str] = mapped_column(
        String(30),
        default="",
    )

    qr_code_base64: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    last_error: Mapped[str] = mapped_column(
        Text,
        default="",
    )


class WhatsAppMessage(BaseModel):

    __tablename__ = "whatsapp_messages"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    funnel_card_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("funnel_cards.id"),
        nullable=True,
    )

    contact_phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    contact_name: Mapped[str] = mapped_column(
        String(200),
        default="",
    )

    direction: Mapped[str] = mapped_column(
        String(10),
        default="in",
    )

    body: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    is_from_agent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
