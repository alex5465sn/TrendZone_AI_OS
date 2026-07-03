from sqlalchemy.orm import Session

from backend.app.repositories.system_info_repository import SystemInfoRepository
from backend.app.schemas.system_info import (
    SystemInfoCreate,
)


class SystemInfoService:

    @staticmethod
    def create(
        db: Session,
        data: SystemInfoCreate,
    ):
        return SystemInfoRepository.create(
            db=db,
            app_name=data.app_name,
            version=data.version,
        )

    @staticmethod
    def get_first(db: Session):
        return SystemInfoRepository.get_first(db)