import json
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.audit_log import AuditLog
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Log"],
)


def record_audit(
    db: Session,
    user_id: int,
    entity_type: str,
    action: str,
    entity_id: Optional[int] = None,
    description: str = "",
    metadata: Optional[dict] = None,
) -> None:
    log = AuditLog(
        user_id=user_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        description=description,
        metadata_json=json.dumps(metadata or {}, ensure_ascii=False),
    )
    db.add(log)
    db.commit()


@router.get("")
def list_audit_logs(
    entity_type: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(AuditLog).filter(AuditLog.user_id == current_user.id)

    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)

    items = query.order_by(AuditLog.created_at.desc()).limit(limit).all()

    result = [
        {
            "id": log.id,
            "entity_type": log.entity_type,
            "entity_id": log.entity_id,
            "action": log.action,
            "description": log.description,
            "metadata": json.loads(log.metadata_json) if log.metadata_json else {},
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in items
    ]

    return ResponseBuilder.success(data=result)


@router.get("/entity-types")
def list_entity_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(AuditLog.entity_type)
        .filter(AuditLog.user_id == current_user.id)
        .distinct()
        .all()
    )
    return ResponseBuilder.success(data=[r[0] for r in rows])
