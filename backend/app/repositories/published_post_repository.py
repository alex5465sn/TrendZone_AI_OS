from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.published_post import PublishedPost
from app.repositories.base_repository import BaseRepository


class PublishedPostRepository(BaseRepository[PublishedPost]):
    model = PublishedPost

    @classmethod
    def get_by_tracking_code(cls, db: Session, tracking_code: str) -> PublishedPost | None:
        stmt = select(PublishedPost).where(PublishedPost.tracking_code == tracking_code)
        return db.execute(stmt).scalars().first()

    @classmethod
    def get_all_ordered(cls, db: Session) -> list[PublishedPost]:
        stmt = (
            select(PublishedPost)
            .where(PublishedPost.is_active.is_(True))
            .order_by(PublishedPost.created_at.desc())
        )
        return list(db.execute(stmt).scalars().all())

    @classmethod
    def register_click(cls, db: Session, post: PublishedPost) -> PublishedPost:
        post.click_count = (post.click_count or 0) + 1
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
