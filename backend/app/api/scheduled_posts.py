"""
TrendZone AI OS
================================

Agendamento de posts — permite agendar a publicação
(texto/imagem ou vídeo) de um produto para uma data/hora futura.
"""

from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.scheduled_post import ScheduledPost
from app.repositories.scheduled_post_repository import ScheduledPostRepository
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/scheduled-posts",
    tags=["Agendamento de Posts"],
)


class ScheduledPostRequest(BaseModel):
    product_item_id: int
    message: str
    link: str | None = None
    image_url: str | None = None
    video_file: str | None = None
    scheduled_at: datetime


@router.get("")
def list_scheduled(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    posts = ScheduledPostRepository.get_all_ordered(db)
    return ResponseBuilder.success(data=[
        {
            "id": p.id,
            "product_item_id": p.product_item_id,
            "message": p.message,
            "link": p.link,
            "image_url": p.image_url,
            "video_path": p.video_path,
            "scheduled_at": p.scheduled_at.isoformat(),
            "status": p.status,
            "error_message": p.error_message,
        }
        for p in posts
    ])


@router.post("")
def create_scheduled(
    payload: ScheduledPostRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = ScheduledPost(
        product_item_id=payload.product_item_id,
        message=payload.message,
        link=payload.link or "",
        image_url=payload.image_url or "",
        video_path=payload.video_file or "",
        scheduled_at=payload.scheduled_at,
        status="pendente",
    )
    ScheduledPostRepository.create(db, post)
    return ResponseBuilder.success(data={"id": post.id}, message="Post agendado com sucesso.")


@router.delete("/{post_id}")
def cancel_scheduled(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = ScheduledPostRepository.get_by_id(db, post_id)
    if not post:
        return ResponseBuilder.error(message="Agendamento não encontrado.", status_code=404)

    ScheduledPostRepository.soft_delete(db, post)
    return ResponseBuilder.success(message="Agendamento cancelado.")
