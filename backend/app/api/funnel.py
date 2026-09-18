from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel as Schema
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.funnel import FunnelStage, FunnelCard
from app.api.response import ResponseBuilder
from app.api.audit_log import record_audit

router = APIRouter(
    prefix="/funnel",
    tags=["Sales Funnel"],
)

DEFAULT_STAGES = [
    {"name": "Descoberto", "color": "#64748B", "position": 0},
    {"name": "Analisando", "color": "#F59E0B", "position": 1},
    {"name": "Testando", "color": "#3B82F6", "position": 2},
    {"name": "Escalando", "color": "#10B981", "position": 3},
    {"name": "Maduro", "color": "#8B5CF6", "position": 4},
    {"name": "Descartado", "color": "#EF4444", "position": 5},
]


class StageCreate(Schema):
    name: str
    color: str = "#2563EB"
    position: int = 0


class CardCreate(Schema):
    stage_id: int
    title: str
    description: str = ""
    product_id: Optional[int] = None
    priority: str = "MEDIUM"
    estimated_revenue: float = 0.0
    channel: str = ""
    notes: str = ""


class CardMove(Schema):
    stage_id: int
    position: int = 0


@router.get("/stages")
def list_stages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stages = (
        db.query(FunnelStage)
        .filter(FunnelStage.user_id == current_user.id, FunnelStage.is_active == True)
        .order_by(FunnelStage.position)
        .all()
    )

    if not stages:
        for s in DEFAULT_STAGES:
            stage = FunnelStage(
                name=s["name"],
                color=s["color"],
                position=s["position"],
                user_id=current_user.id,
            )
            db.add(stage)
        db.commit()
        stages = (
            db.query(FunnelStage)
            .filter(FunnelStage.user_id == current_user.id, FunnelStage.is_active == True)
            .order_by(FunnelStage.position)
            .all()
        )

    result = []
    for stage in stages:
        cards = (
            db.query(FunnelCard)
            .filter(FunnelCard.stage_id == stage.id, FunnelCard.is_active == True)
            .order_by(FunnelCard.position)
            .all()
        )
        result.append({
            "id": stage.id,
            "name": stage.name,
            "color": stage.color,
            "position": stage.position,
            "cards": [
                {
                    "id": c.id,
                    "title": c.title,
                    "description": c.description,
                    "product_id": c.product_id,
                    "priority": c.priority,
                    "position": c.position,
                    "estimated_revenue": c.estimated_revenue,
                    "channel": c.channel,
                    "notes": c.notes,
                    "created_at": c.created_at.isoformat() if c.created_at else None,
                }
                for c in cards
            ],
        })

    return ResponseBuilder.success(data=result)


@router.post("/stages")
def create_stage(
    payload: StageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stage = FunnelStage(
        name=payload.name,
        color=payload.color,
        position=payload.position,
        user_id=current_user.id,
    )
    db.add(stage)
    db.commit()
    db.refresh(stage)

    return ResponseBuilder.success(
        data={"id": stage.id, "name": stage.name},
        message="Etapa criada.",
        status_code=201,
    )


@router.delete("/stages/{stage_id}")
def delete_stage(
    stage_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stage = (
        db.query(FunnelStage)
        .filter(FunnelStage.id == stage_id, FunnelStage.user_id == current_user.id)
        .first()
    )
    if not stage:
        raise HTTPException(status_code=404, detail="Etapa não encontrada.")

    db.query(FunnelCard).filter(FunnelCard.stage_id == stage_id).update({"is_active": False})
    stage.is_active = False
    db.commit()

    return ResponseBuilder.success(message="Etapa removida.")


@router.post("/cards")
def create_card(
    payload: CardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stage = db.query(FunnelStage).filter(FunnelStage.id == payload.stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Etapa não encontrada.")

    card = FunnelCard(
        stage_id=payload.stage_id,
        product_id=payload.product_id,
        user_id=current_user.id,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        position=payload.position,
        estimated_revenue=payload.estimated_revenue,
        channel=payload.channel,
        notes=payload.notes,
    )
    db.add(card)
    db.commit()
    db.refresh(card)

    return ResponseBuilder.success(
        data={"id": card.id, "title": card.title},
        message="Card criado.",
        status_code=201,
    )


@router.put("/cards/{card_id}/move")
def move_card(
    card_id: int,
    payload: CardMove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = (
        db.query(FunnelCard)
        .filter(FunnelCard.id == card_id, FunnelCard.user_id == current_user.id)
        .first()
    )
    if not card:
        raise HTTPException(status_code=404, detail="Card não encontrado.")

    old_stage_id = card.stage_id
    card.stage_id = payload.stage_id
    card.position = payload.position
    db.commit()

    record_audit(
        db, current_user.id, "funnel_card", "MOVE", card.id,
        f"Card '{card.title}' movido do estágio {old_stage_id} para {payload.stage_id}",
    )

    return ResponseBuilder.success(message="Card movido.")


@router.delete("/cards/{card_id}")
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = (
        db.query(FunnelCard)
        .filter(FunnelCard.id == card_id, FunnelCard.user_id == current_user.id)
        .first()
    )
    if not card:
        raise HTTPException(status_code=404, detail="Card não encontrado.")

    card.is_active = False
    db.commit()

    return ResponseBuilder.success(message="Card removido.")


@router.get("/radar")
def lead_radar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from datetime import datetime, timedelta

    threshold = datetime.utcnow() - timedelta(days=3)

    stale_cards = (
        db.query(FunnelCard)
        .filter(
            FunnelCard.user_id == current_user.id,
            FunnelCard.is_active == True,
            FunnelCard.updated_at < threshold,
        )
        .all()
    )

    result = [
        {
            "id": c.id,
            "title": c.title,
            "stage_id": c.stage_id,
            "days_stale": (datetime.utcnow() - c.updated_at).days,
            "priority": c.priority,
            "estimated_revenue": c.estimated_revenue,
        }
        for c in stale_cards
    ]

    return ResponseBuilder.success(data=result)
