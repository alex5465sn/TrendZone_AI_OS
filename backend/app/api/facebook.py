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
from app.services.video_generator import generate_product_video, VideoGenerationError, MEDIA_DIR
from app.services.facebook_auto_post_service import run_daily_auto_schedule, PEAK_HOURS

router = APIRouter(
    prefix="/facebook",
    tags=["Facebook"],
)


class FacebookPostRequest(BaseModel):
    message: str
    link: str | None = None
    image_url: str | None = None


class GenerateVideoRequest(BaseModel):
    image_url: str
    title: str
    price: str
    discount_rate: int | None = None


class PostVideoRequest(BaseModel):
    file: str
    description: str = ""


@router.get("/status")
def status(current_user: User = Depends(get_current_user)):
    client = FacebookClient()
    return ResponseBuilder.success(data={"configured": client.is_configured(), "peak_hours": PEAK_HOURS})


@router.post("/auto-schedule/run")
def force_auto_schedule(current_user: User = Depends(get_current_user)):
    created = run_daily_auto_schedule()
    return ResponseBuilder.success(
        data={"created": created},
        message=f"{created} post(s) agendado(s) para os horarios de pico." if created else "Ja havia posts agendados para hoje ou nenhum produto disponivel.",
    )


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


@router.post("/video/generate")
def generate_video(payload: GenerateVideoRequest, current_user: User = Depends(get_current_user)):

    try:
        path = generate_product_video(
            image_url=payload.image_url,
            title=payload.title,
            price=payload.price,
            discount_rate=payload.discount_rate,
        )
    except VideoGenerationError as exc:
        return ResponseBuilder.error(message=str(exc), status_code=400)

    return ResponseBuilder.success(
        data={"file": path.name, "url": f"/media/videos/{path.name}"},
        message="Vídeo gerado com sucesso.",
    )


@router.post("/video/post")
def post_video(payload: PostVideoRequest, current_user: User = Depends(get_current_user)):

    file_path = MEDIA_DIR / payload.file

    if not file_path.exists():
        return ResponseBuilder.error(message="Arquivo de vídeo não encontrado.", status_code=404)

    client = FacebookClient()

    try:
        result = client.publish_video(str(file_path), description=payload.description)
    except FacebookConfigError as exc:
        return ResponseBuilder.error(message=str(exc), status_code=400)
    except FacebookAPIError as exc:
        return ResponseBuilder.error(message=str(exc), status_code=502)

    return ResponseBuilder.success(data=result, message="Vídeo publicado no Facebook com sucesso.")
