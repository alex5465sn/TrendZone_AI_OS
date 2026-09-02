"""
TrendZone AI OS
================================

Repository responsável pela entidade Campaign.
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.repositories.base_repository import BaseRepository


class CampaignRepository(BaseRepository[Campaign]):
    """
    Repository da entidade Campaign.
    """

    model = Campaign

    # =====================================================
    # BY STATUS
    # =====================================================

    @classmethod
    def get_by_status(
        cls,
        db: Session,
        status: str,
    ) -> list[Campaign]:

        stmt = (
            select(Campaign)
            .where(
                Campaign.status == status,
                Campaign.is_active.is_(True),
            )
            .order_by(Campaign.created_at.desc())
        )

        return list(db.execute(stmt).scalars().all())

    # =====================================================
    # PUBLISH
    # =====================================================

    @classmethod
    def mark_published(
        cls,
        db: Session,
        campaign: Campaign,
    ) -> Campaign:

        campaign.status = "PUBLISHED"
        campaign.updated_at = datetime.utcnow()

        return cls.update(db, campaign)
