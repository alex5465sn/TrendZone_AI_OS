from fastapi import APIRouter

from app.core.settings import settings

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
def health():

    return {
        "backend": "online",
        "database": "online",
        "dashboard": "online",
        "frontend": "online",
        "scout": "development",
        "shopee": "disconnected",
        "version": settings.VERSION,
    }