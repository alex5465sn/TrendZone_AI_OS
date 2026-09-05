"""
TrendZone AI OS
================================

Facebook API — publicação automática de posts de produtos na página.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_current_user
from app.models.user import User
from app.api.response import ResponseBuilder
from app.integrations.facebook.facebook_client import (
    FacebookClient,
    FacebookConfigError,
    FacebookAPIError,
)

router = APIRouter(
    prefix="/facebook",
    tags=["Facebook"],
)


class FacebookPostRequest(BaseModel):
    message: str
    link: str | None = None
    image_url: str | None = None


@router.get("/status")
def status(current_user: User = Depends(get_current_user)):
    client = FacebookClient()
    return ResponseBuilder.success(data={"configured": client.is_configured()})


@router.post("/post")
def post(payload: FacebookPostRequest, current_user: User = Depends(get_current_user)):

    client = FacebookClient()

    try:
        result = client.publish_post(
            message=payload.message,
            link=payload.link,
            image_url=payload.image_url,
        )
    except FacebookConfigError as exc:
        return ResponseBuilder.error(message=str(exc), status_code=400)
    except FacebookAPIError as exc:
        return ResponseBuilder.error(message=str(exc), status_code=502)

    return ResponseBuilder.success(data=result, message="Publicado no Facebook com sucesso.")
