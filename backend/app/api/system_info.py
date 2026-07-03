from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.schemas.system_info import (
    SystemInfoCreate,
    SystemInfoResponse,
)
from backend.app.services.system_info_service import (
    SystemInfoService,
)

router = APIRouter(
    prefix="/system-info",
    tags=["System Info"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=SystemInfoResponse)
def create_system(
    data: SystemInfoCreate,
    db: Session = Depends(get_db),
):
    return SystemInfoService.create(db, data)


@router.get("/", response_model=SystemInfoResponse | None)
def get_system(
    db: Session = Depends(get_db),
):
    return SystemInfoService.get_first(db)