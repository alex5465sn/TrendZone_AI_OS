"""
Repository para Notification.
"""

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    model = Notification

    @classmethod
    def get_by_user(cls, db: Session, user_id: int, limit: int = 50) -> list[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())

    @classmethod
    def get_unread_count(cls, db: Session, user_id: int) -> int:
        stmt = select(func.count(Notification.id)).where(
            (Notification.user_id == user_id) & (Notification.read == False)
        )
        return db.execute(stmt).scalar() or 0

    @classmethod
    def mark_as_read(cls, db: Session, notification_id: int, user_id: int) -> bool:
        notification = db.query(Notification).filter(
            (Notification.id == notification_id) & (Notification.user_id == user_id)
        ).first()

        if notification:
            from datetime import datetime
            notification.read = True
            notification.read_at = datetime.utcnow()
            db.add(notification)
            db.commit()
            return True
        return False
