from sqlalchemy.orm import Session

from backend.app.models.system_info import SystemInfo


class SystemInfoRepository:

    @staticmethod
    def create(
        db: Session,
        app_name: str,
        version: str,
    ) -> SystemInfo:

        system = SystemInfo(
            app_name=app_name,
            version=version,
        )

        db.add(system)
        db.commit()
        db.refresh(system)

        return system

    @staticmethod
    def get_first(db: Session):

        return db.query(SystemInfo).first()