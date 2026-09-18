from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
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


class AutomationRule(BaseModel):

    __tablename__ = "automation_rules"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    trigger_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    trigger_config: Mapped[str] = mapped_column(
        Text,
        default="{}",
    )

    action_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    action_config: Mapped[str] = mapped_column(
        Text,
        default="{}",
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    last_triggered_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    trigger_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
