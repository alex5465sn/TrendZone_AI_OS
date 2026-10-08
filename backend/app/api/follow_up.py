from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel as Schema
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.follow_up import FollowUp
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/follow-ups",
    tags=["Follow-ups"],
)


class FollowUpCreate(Schema):
    card_id: Optional[int] = None
    product_id: Optional[int] = None
    message: str
    due_at: Optional[str] = None
    priority: str = "MEDIUM"


class FollowUpUpdate(Schema):
    status: str


@router.get("")
def list_follow_ups(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(FollowUp).filter(
        FollowUp.user_id == current_user.id,
        FollowUp.is_active == True,
    )

    if status:
        query = query.filter(FollowUp.status == status)

    items = query.order_by(FollowUp.due_at.asc().nullslast()).all()

    result = [
        {
            "id": f.id,
            "card_id": f.card_id,
            "product_id": f.product_id,
            "message": f.message,
            "due_at": f.due_at.isoformat() if f.due_at else None,
            "status": f.status,
            "priority": f.priority,
            "created_at": f.created_at.isoformat() if f.created_at else None,
        }
        for f in items
    ]

    return ResponseBuilder.success(data=result)


@router.get("/overdue")
def overdue_follow_ups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = datetime.utcnow()

    items = (
        db.query(FollowUp)
        .filter(
            FollowUp.user_id == current_user.id,
            FollowUp.is_active == True,
            FollowUp.status == "PENDING",
            FollowUp.due_at < now,
        )
        .order_by(FollowUp.due_at.asc())
        .all()
    )

    result = [
        {
            "id": f.id,
            "card_id": f.card_id,
            "product_id": f.product_id,
            "message": f.message,
            "due_at": f.due_at.isoformat() if f.due_at else None,
            "priority": f.priority,
            "days_overdue": (now - f.due_at).days if f.due_at else 0,
        }
        for f in items
    ]

    return ResponseBuilder.success(data=result)


@router.post("")
def create_follow_up(
    payload: FollowUpCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    due = None
    if payload.due_at:
        try:
            due = datetime.fromisoformat(payload.due_at)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido. Use ISO 8601.")

    follow_up = FollowUp(
        card_id=payload.card_id,
        product_id=payload.product_id,
        user_id=current_user.id,
        message=payload.message,
        due_at=due,
        priority=payload.priority,
    )
    db.add(follow_up)
    db.commit()
    db.refresh(follow_up)

    return ResponseBuilder.success(
        data={"id": follow_up.id},
        message="Follow-up criado.",
        status_code=201,
    )


@router.patch("/{follow_up_id}")
def update_follow_up(
    follow_up_id: int,
    payload: FollowUpUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(FollowUp)
        .filter(FollowUp.id == follow_up_id, FollowUp.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Follow-up não encontrado.")

    item.status = payload.status
    db.commit()

    return ResponseBuilder.success(message="Follow-up atualizado.")


@router.delete("/{follow_up_id}")
def delete_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(FollowUp)
        .filter(FollowUp.id == follow_up_id, FollowUp.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Follow-up não encontrado.")

    item.is_active = False
    db.commit()

    return ResponseBuilder.success(message="Follow-up removido.")
