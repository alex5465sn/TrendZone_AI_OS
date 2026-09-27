"""
TrendZone AI OS

API de Notificações.

Endpoints para gerenciar notificações do usuário.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.repositories.notification_repository import NotificationRepository
from app.api.response import ResponseBuilder

router = APIRouter(prefix="/notifications", tags=["Notificações"])


@router.get("")
def get_notifications(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retorna notificações recentes do usuário."""
    notifications = NotificationRepository.get_by_user(db, current_user.id, limit)

    return ResponseBuilder.success(
        data=[
            {
                "id": n.id,
                "type": n.notification_type,
                "title": n.title,
                "message": n.message,
                "sent": n.sent,
                "read": n.read,
                "created_at": n.created_at.isoformat(),
                "sent_at": n.sent_at.isoformat() if n.sent_at else None,
            }
            for n in notifications
        ]
    )


@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Marca notificação como lida."""
    success = NotificationRepository.mark_as_read(db, notification_id, current_user.id)

    if success:
        return ResponseBuilder.success(message="Notificação marcada como lida.")
    else:
        return ResponseBuilder.error("Notificação não encontrada.", status_code=404)


@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retorna quantidade de notificações não lidas."""
    count = NotificationRepository.get_unread_count(db, current_user.id)

    return ResponseBuilder.success(data={"unread_count": count})
