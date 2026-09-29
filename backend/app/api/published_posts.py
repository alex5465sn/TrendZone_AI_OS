"""
TrendZone AI OS
================================

Tracking de Cliques (TCIE - Fase 2)

Gera links rastreáveis para cada post publicado e registra
os cliques reais recebidos, formando a base de dados de
aprendizado para o Commercial Intelligence Engine.
"""

import html
import secrets

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
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


# Redes sociais fazem um "preview scraping" da URL compartilhada antes de
# exibir o card de compartilhamento. Se deixarmos esse robô seguir o
# redirect até a Shopee, ele recebe 403 (a Shopee bloqueia esses user-agents)
# e a rede social exibe "página indisponível" / fica em loop.
CRAWLER_USER_AGENTS = (
    "facebookexternalhit",
    "facebot",
    "whatsapp",
    "twitterbot",
    "linkedinbot",
    "slackbot",
    "telegrambot",
    "discordbot",
    "pinterest",
    "skypeuripreview",
)


def _is_social_crawler(user_agent: str) -> bool:
    ua = (user_agent or "").lower()
    return any(marker in ua for marker in CRAWLER_USER_AGENTS)


def _crawler_preview_html(post: PublishedPost, tracking_url: str) -> str:
    title = html.escape(post.product_name or "Oferta TrendZone")
    description = html.escape("Confira essa oferta imperdível antes que acabe! 🔥")
    image = html.escape(post.product_image or "")
    url = html.escape(tracking_url)
    destination = html.escape(post.destination_url)

    image_tag = f'<meta property="og:image" content="{image}" />' if image else ""

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8" />
<title>{title}</title>
<meta property="og:type" content="product" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="{url}" />
{image_tag}
<meta http-equiv="refresh" content="0; url={destination}" />
</head>
<body>
<p>{title}</p>
<p><a href="{destination}">Ver oferta</a></p>
</body>
</html>"""


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


@public_router.api_route("/go/{tracking_code}", methods=["GET", "HEAD"])
def redirect_tracking(tracking_code: str, request: Request, db: Session = Depends(get_db)):
    post = PublishedPostRepository.get_by_tracking_code(db, tracking_code)

    if not post:
        return ResponseBuilder.error(message="Link não encontrado.", status_code=404)

    user_agent = request.headers.get("user-agent", "")

    if _is_social_crawler(user_agent):
        from app.core.settings import settings

        tracking_url = _build_tracking_url(settings.APP_BASE_URL, tracking_code)
        return HTMLResponse(content=_crawler_preview_html(post, tracking_url))

    PublishedPostRepository.register_click(db, post)

    return RedirectResponse(url=post.destination_url, status_code=302)
