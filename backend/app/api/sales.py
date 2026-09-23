"""
TrendZone AI OS — Sales & Commissions API

Rastreamento de vendas, comissoes e divulgacao.
- Sincroniza conversoes da Shopee Affiliate API
- Gera links curtos de rastreamento
- Painel financeiro (comissoes pendentes/confirmadas)
"""

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.sale import Sale
from app.repositories.sale_repository import SaleRepository
from app.repositories.campaign_repository import CampaignRepository
from app.services.sales_tracker_service import SalesTrackerService
from app.services.marketplace_account_service import MarketplaceAccountService
from app.api.response import ResponseBuilder

router = APIRouter(prefix="/sales", tags=["Sales & Commissions"])


class TrackingLinkRequest(BaseModel):
    origin_url: str
    campaign_id: int | None = None
    sub_ids: list[str] = []


def _shopee_credentials(db: Session, user: User) -> dict | None:
    """
    Credenciais da conta Shopee conectada pelo usuário.

    Retorna None quando o usuário não conectou conta própria —
    nesse caso os fluxos usam as credenciais globais (.env),
    preservando o comportamento do admin/dono.
    """
    try:
        creds = MarketplaceAccountService.get_credentials(
            db, user.id, "shopee"
        )
    except Exception:
        return None

    if not creds:
        return None

    extra = creds.get("extra") or {}
    app_id = str(extra.get("app_id") or "").strip()
    secret = str(extra.get("secret") or "").strip()

    if not app_id or not secret:
        return None

    return {"app_id": app_id, "secret": secret}


@router.post("/sync")
def sync_conversions(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    nodes = SalesTrackerService.fetch_conversions(
        days_back=days,
        credentials=_shopee_credentials(db, current_user),
    )

    new_count = 0
    updated_count = 0

    for node in nodes:
        parsed = SalesTrackerService.parse_conversion(node)
        existing = SaleRepository.get_by_conversion_id(db, parsed["conversion_id"])

        if existing:
            if existing.user_id is None:
                existing.user_id = current_user.id

            existing.order_status = parsed["order_status"]
            existing.total_commission = parsed["total_commission"]
            existing.net_commission = parsed["net_commission"]
            existing.seller_commission = parsed["seller_commission"]
            existing.shopee_commission = parsed["shopee_commission"]
            existing.updated_at = datetime.utcnow()

            if parsed["order_status"] in ("completed", "settled"):
                existing.status = "confirmada"
            elif parsed["order_status"] in ("cancelled", "refunded"):
                existing.status = "cancelada"

            SaleRepository.update(db, existing)
            updated_count += 1
        else:
            status = "pendente"
            if parsed["order_status"] in ("completed", "settled"):
                status = "confirmada"
            elif parsed["order_status"] in ("cancelled", "refunded"):
                status = "cancelada"

            sale = Sale(
                conversion_id=parsed["conversion_id"],
                user_id=current_user.id,
                order_id=parsed["order_id"],
                order_status=parsed["order_status"],
                shop_type=parsed["shop_type"],
                buyer_type=parsed["buyer_type"],
                device=parsed["device"],
                product_type=parsed["product_type"],
                click_time=parsed["click_time"],
                purchase_time=parsed["purchase_time"],
                total_commission=parsed["total_commission"],
                seller_commission=parsed["seller_commission"],
                shopee_commission=parsed["shopee_commission"],
                net_commission=parsed["net_commission"],
                utm_content=parsed["utm_content"],
                status=status,
            )
            SaleRepository.create(db, sale)
            new_count += 1

    return ResponseBuilder.success(
        data={
            "synced_from_shopee": len(nodes),
            "new_sales": new_count,
            "updated_sales": updated_count,
        },
        message=f"Sincronizado: {new_count} nova(s), {updated_count} atualizada(s).",
    )


@router.get("")
def list_sales(
    status: str = Query("", description="pendente, confirmada, cancelada"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if status:
        sales = SaleRepository.get_by_status(db, status)
    else:
        sales = SaleRepository.get_all(db)

    if current_user.role != "ADMIN":
        sales = [
            s for s in sales
            if s.user_id == current_user.id
        ]

    sales.sort(key=lambda s: s.created_at or datetime.min, reverse=True)

    return ResponseBuilder.success(
        data=[
            {
                "id": s.id,
                "conversion_id": s.conversion_id,
                "order_id": s.order_id,
                "order_status": s.order_status,
                "buyer_type": s.buyer_type,
                "device": s.device,
                "product_type": s.product_type,
                "click_time": s.click_time,
                "purchase_time": s.purchase_time,
                "total_commission": s.total_commission,
                "net_commission": s.net_commission,
                "seller_commission": s.seller_commission,
                "shopee_commission": s.shopee_commission,
                "utm_content": s.utm_content,
                "status": s.status,
                "created_at": s.created_at.isoformat() if s.created_at else "",
            }
            for s in sales
        ],
    )


@router.get("/financial")
def financial_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    owner_id = None if current_user.role == "ADMIN" else current_user.id
    total = SaleRepository.financial_summary(db, owner_id)
    pending = SaleRepository.pending_summary(db, owner_id)
    confirmed = SaleRepository.confirmed_summary(db, owner_id)

    return ResponseBuilder.success(
        data={
            **total,
            **pending,
            **confirmed,
            "available_to_withdraw": confirmed["confirmed_amount"],
        },
    )


@router.post("/tracking-link")
def generate_tracking_link(
    payload: TrackingLinkRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = SalesTrackerService.generate_tracking_link(
        origin_url=payload.origin_url,
        sub_ids=payload.sub_ids,
        credentials=_shopee_credentials(db, current_user),
    )

    if payload.campaign_id:
        campaign = CampaignRepository.get_by_id(db, payload.campaign_id)
        if campaign:
            campaign.tracking_link = result.get("short_link", "")
            campaign.updated_at = datetime.utcnow()
            CampaignRepository.update(db, campaign)

    return ResponseBuilder.success(
        data=result,
        message="Link de rastreamento gerado.",
    )


@router.get("/campaigns/tracking")
def campaigns_with_tracking(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaigns = CampaignRepository.get_all(db)

    return ResponseBuilder.success(
        data=[
            {
                "id": c.id,
                "title": c.title,
                "channel": c.channel,
                "status": c.status,
                "tracking_link": c.tracking_link,
                "clicks": c.clicks,
                "conversions": c.conversions,
                "revenue": c.revenue,
                "created_at": c.created_at.isoformat() if c.created_at else "",
            }
            for c in campaigns
        ],
    )
