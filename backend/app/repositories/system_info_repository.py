"""
TrendZone AI OS
================================

Repository responsável pelas informações
institucionais do sistema.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.system_info import SystemInfo
from app.repositories.base_repository import BaseRepository


class SystemInfoRepository(BaseRepository[SystemInfo]):
    """
    Repository da entidade SystemInfo.
    """

    model = SystemInfo

    # =====================================================
    # PRIMEIRO REGISTRO
    # =====================================================

    @classmethod
    def get_first(
        cls,
        db: Session,
    ) -> SystemInfo | None:

        stmt = (
            select(SystemInfo)
            .limit(1)
        )

        return db.execute(stmt).scalar_one_or_none()