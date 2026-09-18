from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel as Schema
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.product import Product
from app.models.content_strategy import ContentStrategy
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/content-strategy",
    tags=["Content Strategy"],
)

PLATFORMS = ["shopee_video", "pinterest", "whatsapp", "facebook", "instagram", "tiktok", "blog"]
CONTENT_TYPES = ["video_curto", "video_review", "carrossel", "post_imagem", "artigo_blog", "live", "stories"]


class StrategyGenerate(Schema):
    product_id: int
    platforms: list[str] = ["shopee_video", "pinterest", "whatsapp"]


class StrategyCreate(Schema):
    product_id: Optional[int] = None
    content_type: str
    platform: str
    title: str
    script: str = ""
    hashtags: str = ""
    cta: str = ""
    best_time: str = ""


class StrategyUpdate(Schema):
    status: str


@router.post("/generate")
def generate_strategies(
    payload: StrategyGenerate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    strategies = []

    templates = {
        "shopee_video": {
            "content_type": "video_curto",
            "title": f"Review Rápido: {product.name[:60]}",
            "script": (
                f"1. Abertura impactante (3s) — mostre o produto em uso\n"
                f"2. Destaque o benefício principal\n"
                f"3. Mostre o preço e desconto: R$ {product.price}\n"
                f"4. CTA: 'Clique no carrinho para garantir!'\n"
                f"5. Música em alta — estilo clean sem narração pesada"
            ),
            "hashtags": "#shopee #oferta #achados #review #dica",
            "cta": "Clique no carrinho para garantir o seu!",
            "best_time": "9h, 12h, 15h, 20h",
        },
        "pinterest": {
            "content_type": "post_imagem",
            "title": f"Achado Shopee: {product.name[:60]}",
            "script": (
                f"Pin com imagem profissional do produto\n"
                f"Título: {product.name[:60]}\n"
                f"Descrição otimizada para SEO com palavras-chave do nicho\n"
                f"Link de afiliado com SubID 'Pin_{product.item_id}'\n"
                f"Cookie de 7 dias — qualquer compra na Shopee gera comissão"
            ),
            "hashtags": "#shopee #achados #oferta #dica #tendencia",
            "cta": "Veja o preço especial no link!",
            "best_time": "14h, 19h, 21h",
        },
        "whatsapp": {
            "content_type": "post_imagem",
            "title": f"Oferta Exclusiva: {product.name[:60]}",
            "script": (
                f"🔥 ACHADO DO DIA 🔥\n\n"
                f"{product.name}\n"
                f"💰 Por apenas R$ {product.price}\n"
                f"⭐ Avaliação: {product.rating}\n"
                f"🛒 Comissão: {product.commission}%\n\n"
                f"👉 Link de afiliado com SubID 'WA_{product.item_id}'"
            ),
            "hashtags": "",
            "cta": "Corre que é por tempo limitado!",
            "best_time": "8h, 12h, 18h",
        },
        "facebook": {
            "content_type": "video_review",
            "title": f"Vale a Pena? {product.name[:60]}",
            "script": (
                f"Post para feed ou grupo de ofertas:\n"
                f"Título chamativo + imagem do produto\n"
                f"Destaque: preço, avaliações, frete grátis (se aplicável)\n"
                f"Link com SubID 'FB_{product.item_id}'"
            ),
            "hashtags": "#shopee #oferta #desconto #achadinho",
            "cta": "Comenta 'EU QUERO' que mando o link!",
            "best_time": "12h, 19h, 21h",
        },
        "instagram": {
            "content_type": "carrossel",
            "title": f"Top Achado: {product.name[:60]}",
            "script": (
                f"Carrossel de 5 slides:\n"
                f"1. Capa impactante com o produto\n"
                f"2. Problema que resolve\n"
                f"3. Benefícios principais\n"
                f"4. Preço + desconto\n"
                f"5. CTA — link na bio"
            ),
            "hashtags": "#shopee #reels #achados #tendencia #oferta",
            "cta": "Link na bio! Corre antes que acabe!",
            "best_time": "11h, 17h, 20h",
        },
        "tiktok": {
            "content_type": "video_curto",
            "title": f"Achado que Viralizou: {product.name[:60]}",
            "script": (
                f"Vídeo de 15-30s:\n"
                f"Hook nos primeiros 3 segundos\n"
                f"Demonstração do produto em uso\n"
                f"Transição rápida para preço\n"
                f"Música viral em alta"
            ),
            "hashtags": "#shopee #achadinho #tiktokmademebuyit #viral",
            "cta": "Link na bio!",
            "best_time": "7h, 12h, 19h, 22h",
        },
        "blog": {
            "content_type": "artigo_blog",
            "title": f"Review Completo: {product.name[:60]}",
            "script": (
                f"Artigo SEO otimizado:\n"
                f"H1: Review {product.name}\n"
                f"Seções: Visão geral, prós/contras, fotos, comparação\n"
                f"CTA com link de afiliado + SubID 'Blog_{product.item_id}'\n"
                f"Palavras-chave de cauda longa para ranquear no Google"
            ),
            "hashtags": "",
            "cta": "Confira o preço atualizado clicando aqui!",
            "best_time": "Publicação: qualquer hora — tráfego orgânico",
        },
    }

    for platform in payload.platforms:
        if platform not in templates:
            continue

        tpl = templates[platform]
        strategy = ContentStrategy(
            product_id=product.id,
            user_id=current_user.id,
            content_type=tpl["content_type"],
            platform=platform,
            title=tpl["title"],
            script=tpl["script"],
            hashtags=tpl["hashtags"],
            cta=tpl["cta"],
            best_time=tpl["best_time"],
        )
        db.add(strategy)
        strategies.append(strategy)

    db.commit()

    result = [
        {
            "id": s.id,
            "content_type": s.content_type,
            "platform": s.platform,
            "title": s.title,
            "script": s.script,
            "hashtags": s.hashtags,
            "cta": s.cta,
            "best_time": s.best_time,
            "status": s.status,
        }
        for s in strategies
    ]

    return ResponseBuilder.success(
        data=result,
        message=f"{len(strategies)} estratégias geradas.",
        status_code=201,
    )


@router.get("/")
def list_strategies(
    platform: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(ContentStrategy).filter(
        ContentStrategy.user_id == current_user.id,
        ContentStrategy.is_active == True,
    )

    if platform:
        query = query.filter(ContentStrategy.platform == platform)
    if status:
        query = query.filter(ContentStrategy.status == status)

    items = query.order_by(ContentStrategy.created_at.desc()).all()

    result = [
        {
            "id": s.id,
            "product_id": s.product_id,
            "content_type": s.content_type,
            "platform": s.platform,
            "title": s.title,
            "script": s.script,
            "hashtags": s.hashtags,
            "cta": s.cta,
            "best_time": s.best_time,
            "status": s.status,
            "performance_score": s.performance_score,
            "created_at": s.created_at.isoformat() if s.created_at else None,
        }
        for s in items
    ]

    return ResponseBuilder.success(data=result)


@router.patch("/{strategy_id}")
def update_strategy_status(
    strategy_id: int,
    payload: StrategyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    strategy = (
        db.query(ContentStrategy)
        .filter(ContentStrategy.id == strategy_id, ContentStrategy.user_id == current_user.id)
        .first()
    )
    if not strategy:
        raise HTTPException(status_code=404, detail="Estratégia não encontrada.")

    strategy.status = payload.status
    db.commit()

    return ResponseBuilder.success(message="Status atualizado.")


@router.delete("/{strategy_id}")
def delete_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    strategy = (
        db.query(ContentStrategy)
        .filter(ContentStrategy.id == strategy_id, ContentStrategy.user_id == current_user.id)
        .first()
    )
    if not strategy:
        raise HTTPException(status_code=404, detail="Estratégia não encontrada.")

    strategy.is_active = False
    db.commit()

    return ResponseBuilder.success(message="Estratégia removida.")


@router.get("/platforms")
def available_platforms(
    current_user: User = Depends(get_current_user),
):
    return ResponseBuilder.success(data={
        "platforms": PLATFORMS,
        "content_types": CONTENT_TYPES,
    })
