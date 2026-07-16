from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.security.dependencies import get_current_user

from app.services.scout_service import ScoutService

router = APIRouter(
    prefix="/scout",
    tags=["Scout"],
)


@router.get("/search")
def search_products(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = ScoutService(db)

    return service.search_products()