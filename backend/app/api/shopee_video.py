"""
TrendZone AI OS
================================

Shopee Vídeo — geração de vídeo promocional com identidade visual da
Shopee, pronto para baixar e publicar manualmente no app (a Shopee não
expõe API pública de upload de vídeo para afiliados).
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_current_user
from app.models.user import User
from app.api.response import ResponseBuilder
from app.services.video_generator import generate_product_video, VideoGenerationError

router = APIRouter(
    prefix="/shopee-video",
    tags=["Shopee Vídeo"],
)


class GenerateShopeeVideoRequest(BaseModel):
    image_url: str
    title: str
    price: str
    discount_rate: int | None = None
    commission_rate: float | None = None
    item_id: int | None = None


def _build_caption(title: str, price: str, discount_rate: int | None, commission_rate: float | None, item_id: int | None) -> str:
    lines = [
        "🛒 ACHADO SHOPEE",
        title,
        f"💰 Por apenas R$ {price}",
    ]
    if discount_rate:
        lines.append(f"🔻 {discount_rate}% OFF")
    if commission_rate:
        lines.append(f"⭐ Comissão: {commission_rate}%")
    lines.append("👉 Garanta já, link no carrinho/bio!")

    hashtags = "#shopee #achadinho #shopeevideo #promocao #oferta"
    if item_id:
        hashtags += f" #sub{item_id}"

    return "\n".join(lines) + "\n\n" + hashtags


@router.post("/generate")
def generate_shopee_video(payload: GenerateShopeeVideoRequest, current_user: User = Depends(get_current_user)):

    try:
        path = generate_product_video(
            image_url=payload.image_url,
            title=payload.title,
            price=payload.price,
            discount_rate=payload.discount_rate,
            cta="Garanta já na Shopee!",
            theme="shopee",
        )
    except VideoGenerationError as exc:
        return ResponseBuilder.error(message=str(exc), status_code=400)

    caption = _build_caption(
        payload.title, payload.price, payload.discount_rate, payload.commission_rate, payload.item_id
    )

    return ResponseBuilder.success(
        data={
            "file": path.name,
            "url": f"/media/videos/{path.name}",
            "caption": caption,
        },
        message="Vídeo Shopee gerado com sucesso.",
    )
