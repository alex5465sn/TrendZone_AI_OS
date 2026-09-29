"""
TrendZone AI OS
================================

Marketplace API.
"""

import secrets
from urllib.parse import quote

from fastapi import APIRouter, Depends
from fastapi import Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.published_post import PublishedPost
from app.repositories.published_post_repository import PublishedPostRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate
from app.services.marketplace_service import MarketplaceBusiness
from app.services.product_service import ProductService
from app.services.product_score import ProductScore
from app.services.decision_engine import DecisionEngine
from app.services.content_generator_service import ContentGeneratorService
from app.core.exceptions import ProductAlreadyExists
from app.core.settings import settings

from app.api.response import ResponseBuilder
from app.api.marketplace_schemas import PromoteRequest

router = APIRouter(

    prefix="/marketplace",

    tags=["Marketplace"],

)

service = MarketplaceBusiness()


def _score_and_classify(node: dict) -> tuple[float, str]:

    score = ProductScore.calculate(
        commission=float(node.get("commissionRate") or 0) * 100,
        rating=float(node.get("ratingStar") or 0),
        sales=int(node.get("sales") or 0),
    )

    decision = DecisionEngine.classify({"score": score})

    return score, decision


def _auto_add_if_promoted(db: Session, node: dict, decision: str, score: float) -> bool:
    """Adiciona o produto ao banco automaticamente quando a IA decide PROMOVER.

    Retorna True se o produto já está (ou acabou de ficar) rastreado no banco.
    """

    existing = ProductRepository.get_by_item_id(db, node["itemId"])

    if existing:
        return True

    if decision != "PROMOVER":
        return False

    try:
        ProductService.create(
            db,
            ProductCreate(
                item_id=node["itemId"],
                shop_id=node["shopId"],
                category="geral",
                name=node["productName"],
                price=node["price"],
                commission=float(node.get("commissionRate") or 0) * 100,
                image=node.get("imageUrl", ""),
                offer_link=node.get("offerLink", ""),
                rating=float(node.get("ratingStar") or 0),
                sales=int(node.get("sales") or 0),
            ),
        )
        return True
    except ProductAlreadyExists:
        return True
    except Exception:
        return False


@router.get("/products")
def products(

    marketplace: str = Query(default="shopee"),
    keyword: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    sortType: int = Query(default=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),

):

    data = service.search_products(

        marketplace_name=marketplace,

        keyword=keyword,

        page=page,

        limit=limit,

        sortType=sortType,

    )

    for node in data.get("nodes", []):

        try:
            score, decision = _score_and_classify(node)
            node["score"] = score
            node["decision"] = decision
            node["alreadyTracked"] = _auto_add_if_promoted(db, node, decision, score)
        except Exception:
            node["score"] = None
            node["decision"] = None
            node["alreadyTracked"] = False

    return ResponseBuilder.success(
        data=data,
    )


@router.post("/promote")
def promote(
    payload: PromoteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Gera o conteúdo de divulgação (com IA) e um link de rastreamento
    para um produto, com várias formas prontas de divulgar (copiar texto,
    WhatsApp, Facebook)."""

    tracking_code = secrets.token_urlsafe(6).replace("-", "").replace("_", "")[:8]

    post = PublishedPost(
        tracking_code=tracking_code,
        product_item_id=payload.item_id,
        product_name=payload.product_name,
        destination_url=payload.offer_link,
        channel="marketplace",
        post_format="texto",
        message="",
    )
    PublishedPostRepository.create(db, post)

    tracking_url = f"{settings.APP_BASE_URL.rstrip('/')}/go/{tracking_code}"

    content = ContentGeneratorService.generate_smart(
        {
            "name": payload.product_name,
            "price": payload.price,
            "commission": payload.commission_rate * 100,
            "rating": payload.rating_star,
            "sales": payload.sales,
        },
        tone=payload.tone,
    )
    content["link"] = tracking_url

    full_text = f"{content.get('title', '')}\n\n{content.get('caption', '')}\n\n{tracking_url}\n\n{content.get('hashtags', '')}".strip()

    return ResponseBuilder.success(
        data={
            "content": content,
            "tracking_code": tracking_code,
            "tracking_url": tracking_url,
            "full_text": full_text,
            "whatsapp_share_url": f"https://wa.me/?text={quote(full_text)}",
            "facebook_share_url": f"https://www.facebook.com/sharer/sharer.php?u={quote(tracking_url)}",
        },
        message="Conteúdo de divulgação gerado com sucesso.",
    )


@router.get("/shops")
def shops(

    marketplace: str = Query(default="shopee"),
    keyword: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    sortType: int = Query(default=1),

):

    data = service.search_shops(

        marketplace_name=marketplace,

        keyword=keyword,

        page=page,

        limit=limit,

        sortType=sortType,

    )

    return ResponseBuilder.success(
        data=data,
    )


@router.get("/offers")
def offers(

    marketplace: str = Query(default="shopee"),
    keyword: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    sortType: int = Query(default=1),

):

    data = service.search_offers(

        marketplace_name=marketplace,

        keyword=keyword,

        page=page,

        limit=limit,

        sortType=sortType,

    )

    return ResponseBuilder.success(
        data=data,
    )
