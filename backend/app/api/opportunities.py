"""
TrendZone AI OS
================================

Opportunities API

Endpoints do Motor de Oportunidades de Venda.

Gera sugestões de produtos + conteúdo de
divulgação pronto. A publicação/envio é
sempre uma ação manual do usuário.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.campaign import Campaign
from app.repositories.product_repository import ProductRepository
from app.repositories.campaign_repository import CampaignRepository
from app.services.opportunity_engine import OpportunityEngine
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/opportunities",
    tags=["Opportunities"],
)


# =====================================================
# SCHEMAS
# =====================================================

class SaveCampaignRequest(BaseModel):

    product_id: int
    title: str
    caption: str = ""
    hashtags: str = ""
    target_audience: str = ""
    channel: str = ""


# =====================================================
# HELPERS
# =====================================================

def _product_to_dict(product) -> dict:

    return {
        "id": product.id,
        "item_id": product.item_id,
        "name": product.name,
        "image": product.image,
        "offer_link": product.offer_link,
        "price": float(product.price),
        "commission": float(product.commission),
        "rating": product.rating,
        "sales": product.sales,
        "score": product.score,
        "confidence": product.confidence,
        "recommendation": product.recommendation,
    }


# =====================================================
# OPORTUNIDADES
# =====================================================

@router.get("")
def get_opportunities(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retorna as melhores oportunidades de venda com conteúdo gerado pela IA."""

    products = ProductRepository.get_all(db)
    products_dict = [_product_to_dict(p) for p in products]

    opportunities = OpportunityEngine.find(products_dict, limit=limit)

    return ResponseBuilder.success(
        data=opportunities,
    )


# =====================================================
# CAMPANHAS (HISTÓRICO)
# =====================================================

@router.post("/campaigns")
def save_campaign(
    payload: SaveCampaignRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Salva uma campanha gerada como rascunho."""

    product = ProductRepository.get_by_id(db, payload.product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    campaign = Campaign(
        product_id=product.id,
        title=payload.title,
        caption=payload.caption,
        hashtags=payload.hashtags,
        target_audience=payload.target_audience,
        channel=payload.channel,
        status="DRAFT",
    )

    campaign = CampaignRepository.create(db, campaign)

    return ResponseBuilder.success(
        data={"id": campaign.id, "uuid": campaign.uuid, "status": campaign.status},
        message="Campanha salva como rascunho.",
    )


@router.get("/campaigns")
def list_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lista o histórico de campanhas geradas."""

    campaigns = CampaignRepository.get_all(db)

    return ResponseBuilder.success(
        data=[
            {
                "id": c.id,
                "product_id": c.product_id,
                "title": c.title,
                "caption": c.caption,
                "hashtags": c.hashtags,
                "target_audience": c.target_audience,
                "channel": c.channel,
                "status": c.status,
                "created_at": c.created_at.isoformat(),
            }
            for c in campaigns
        ],
    )


@router.patch("/campaigns/{campaign_id}/publish")
def publish_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Marca uma campanha como publicada (ação manual confirmada pelo usuário)."""

    campaign = CampaignRepository.get_by_id(db, campaign_id)

    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada.")

    campaign = CampaignRepository.mark_published(db, campaign)

    return ResponseBuilder.success(
        data={"id": campaign.id, "status": campaign.status},
        message="Campanha marcada como publicada.",
    )


@router.delete("/campaigns/{campaign_id}")
def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove uma campanha do histórico."""

    campaign = CampaignRepository.get_by_id(db, campaign_id)

    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada.")

    CampaignRepository.soft_delete(db, campaign)

    return ResponseBuilder.success(message="Campanha removida.")
