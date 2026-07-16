"""
TrendZone AI OS
================================

System Info Service.

Responsável pelas informações
institucionais do sistema.
"""

from sqlalchemy.orm import Session

from app.repositories.system_info_repository import (
    SystemInfoRepository,
)

from app.schemas.system_info import (
    SystemInfoCreate,
)

from app.services.base_service import BaseService

from app.core.exceptions import (
    SystemInfoNotFound,
)


class SystemInfoService(BaseService):

    SERVICE_NAME = "SYSTEM_INFO_SERVICE"

    # =====================================================
    # CREATE
    # =====================================================

    @classmethod
    def create(
        cls,
        db: Session,
        data: SystemInfoCreate,
    ):

        cls.log_info(
            "Criando informações do sistema..."
        )

        system = SystemInfoRepository.create(

            db=db,

            app_name=data.app_name,

            version=data.version,

        )

        cls.log_success(
            "Informações cadastradas."
        )

        return system

    # =====================================================
    # GET
    # =====================================================

    @classmethod
    def get_first(
        cls,
        db: Session,
    ):

        system = SystemInfoRepository.get_first(
            db
        )

        if not system:

            raise SystemInfoNotFound()

        return system