from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel as Schema
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.channel_tracking import ChannelTracking
from app.services.product_performance_score import ProductPerformanceScore
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/channel-tracking",
    tags=["Channel Tracking"],
)

CHANNELS = [
    {"id": "shopee_video", "name": "Shopee Vídeo", "icon": "videocam"},
    {"id": "pinterest", "name": "Pinterest", "icon": "push_pin"},
    {"id": "whatsapp", "name": "WhatsApp", "icon": "chat"},
    {"id": "facebook", "name": "Facebook", "icon": "facebook"},
    {"id": "instagram", "name": "Instagram", "icon": "photo_camera"},
    {"id": "tiktok", "name": "TikTok", "icon": "music_note"},
    {"id": "blog", "name": "Blog/SEO", "icon": "article"},
    {"id": "telegram", "name": "Telegram", "icon": "send"},
]


class TrackingCreate(Schema):
    product_id: Optional[int] = None
    channel: str
    sub_id: str
    tracking_url: str = ""


class TrackingUpdate(Schema):
    clicks: Optional[int] = None
    conversions: Optional[int] = None
    revenue: Optional[float] = None


@router.get("/channels")
def available_channels(
    current_user: User = Depends(get_current_user),
):
    return ResponseBuilder.success(data=CHANNELS)


@router.get("/")
def list_trackings(
    channel: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(ChannelTracking).filter(
        ChannelTracking.user_id == current_user.id,
        ChannelTracking.is_active == True,
    )

    if channel:
        query = query.filter(ChannelTracking.channel == channel)

    items = query.order_by(ChannelTracking.created_at.desc()).all()

    result = [
        {
            "id": t.id,
            "product_id": t.product_id,
            "channel": t.channel,
            "sub_id": t.sub_id,
            "tracking_url": t.tracking_url,
            "clicks": t.clicks,
            "conversions": t.conversions,
            "revenue": t.revenue,
            "ctr": t.ctr,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        }
        for t in items
    ]

    return ResponseBuilder.success(data=result)


@router.get("/summary")
def channel_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(
            ChannelTracking.channel,
            func.sum(ChannelTracking.clicks).label("total_clicks"),
            func.sum(ChannelTracking.conversions).label("total_conversions"),
            func.sum(ChannelTracking.revenue).label("total_revenue"),
            func.count(ChannelTracking.id).label("total_links"),
        )
        .filter(
            ChannelTracking.user_id == current_user.id,
            ChannelTracking.is_active == True,
        )
        .group_by(ChannelTracking.channel)
        .all()
    )

    result = [
        {
            "channel": r.channel,
            "total_clicks": r.total_clicks or 0,
            "total_conversions": r.total_conversions or 0,
            "total_revenue": float(r.total_revenue or 0),
            "total_links": r.total_links,
            "avg_ctr": round(
                (r.total_conversions or 0) / max(r.total_clicks or 1, 1) * 100, 2
            ),
        }
        for r in rows
    ]

    return ResponseBuilder.success(data=result)


@router.post("/recalculate-score")
def recalculate_score(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Fecha o loop de dados: reponde o Score dos produtos com base no
    que realmente converteu em Canais & SubIDs (nao espera o ciclo
    automatico de ate 60 minutos do scheduler em segundo plano).
    """
    summary = ProductPerformanceScore.recalculate_all(db)
    return ResponseBuilder.success(
        data=summary,
        message="Score reponderado com base na performance real.",
    )


@router.post("/")
def create_tracking(
    payload: TrackingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tracking = ChannelTracking(
        user_id=current_user.id,
        product_id=payload.product_id,
        channel=payload.channel,
        sub_id=payload.sub_id,
        tracking_url=payload.tracking_url,
    )
    db.add(tracking)
    db.commit()
    db.refresh(tracking)

    return ResponseBuilder.success(
        data={"id": tracking.id, "sub_id": tracking.sub_id},
        message="Tracking criado.",
        status_code=201,
    )


@router.patch("/{tracking_id}")
def update_tracking(
    tracking_id: int,
    payload: TrackingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(ChannelTracking)
        .filter(ChannelTracking.id == tracking_id, ChannelTracking.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Tracking não encontrado.")

    if payload.clicks is not None:
        item.clicks = payload.clicks
    if payload.conversions is not None:
        item.conversions = payload.conversions
    if payload.revenue is not None:
        item.revenue = payload.revenue

    if item.clicks and item.clicks > 0:
        item.ctr = round((item.conversions or 0) / item.clicks * 100, 2)

    db.commit()

    return ResponseBuilder.success(message="Tracking atualizado.")


@router.delete("/{tracking_id}")
def delete_tracking(
    tracking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(ChannelTracking)
        .filter(ChannelTracking.id == tracking_id, ChannelTracking.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Tracking não encontrado.")

    item.is_active = False
    db.commit()

    return ResponseBuilder.success(message="Tracking removido.")
