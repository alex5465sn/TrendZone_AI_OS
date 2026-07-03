from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base import Base


class SystemInfo(Base):
    __tablename__ = "system_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    app_name: Mapped[str] = mapped_column(String(100))

    version: Mapped[str] = mapped_column(String(20))

    status: Mapped[str] = mapped_column(
    String(20),
    default="online",
)