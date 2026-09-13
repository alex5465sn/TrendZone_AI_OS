"""
TrendZone AI OS
================================

Tracking de Cliques (TCIE - Fase 2)

Gera links rastreáveis para cada post publicado e registra
os cliques reais recebidos, formando a base de dados de
aprendizado para o Commercial Intelligence Engine.
"""

import secrets

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.published_post import PublishedPost
from app.repositories.published_post_repository import PublishedPostRepository
from app.api.response import ResponseBuilder

router = APIRouter(prefix="/tracking", tags=["Tracking de Cliques"])
public_router = APIRouter(tags=["Tracking de Cliques"])


class CreateTrackingRequest(BaseModel):
    product_item_id: int
    product_name: str = ""
    destination_url: str
    channel: str = "facebook"
    post_format: str = "texto"
    message: str = ""


def _build_tracking_url(request_base_url: str, tracking_code: str) -> str:
    base = request_base_url.rstrip("/")
    return f"{base}/go/{tracking_code}"


@router.post("/create")
def create_tracking_link(
    payload: CreateTrackingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tracking_code = secrets.token_urlsafe(6).replace("-", "").replace("_", "")[:8]

    post = PublishedPost(
        tracking_code=tracking_code,
        product_item_id=payload.product_item_id,
        product_name=payload.product_name,
        destination_url=payload.destination_url,
        channel=payload.channel,
        post_format=payload.post_format,
        message=payload.message,
    )
    PublishedPostRepository.create(db, post)

    from app.core.settings import settings

    tracking_url = _build_tracking_url(settings.APP_BASE_URL, tracking_code)

    return ResponseBuilder.success(
        data={"tracking_code": tracking_code, "tracking_url": tracking_url},
        message="Link de rastreamento criado com sucesso.",
    )


@router.get("")
def list_tracking(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    posts = PublishedPostRepository.get_all_ordered(db)
    return ResponseBuilder.success(data=[
        {
            "id": p.id,
            "tracking_code": p.tracking_code,
            "product_item_id": p.product_item_id,
            "product_name": p.product_name,
            "destination_url": p.destination_url,
            "channel": p.channel,
            "post_format": p.post_format,
            "click_count": p.click_count,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in posts
    ])


@public_router.get("/go/{tracking_code}")
def redirect_tracking(tracking_code: str, db: Session = Depends(get_db)):
    post = PublishedPostRepository.get_by_tracking_code(db, tracking_code)

    if not post:
        return ResponseBuilder.error(message="Link não encontrado.", status_code=404)

    PublishedPostRepository.register_click(db, post)

    return RedirectResponse(url=post.destination_url, status_code=302)
