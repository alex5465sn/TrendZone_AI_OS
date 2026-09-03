from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.repositories.base_repository import BaseRepository


class SaleRepository(BaseRepository[Sale]):
    model = Sale

    @classmethod
    def get_by_conversion_id(cls, db: Session, conversion_id: str):
        stmt = select(Sale).where(Sale.conversion_id == conversion_id)
        return db.execute(stmt).scalar_one_or_none()

    @classmethod
    def get_by_status(cls, db: Session, status: str) -> list[Sale]:
        stmt = (
            select(Sale)
            .where(Sale.status == status, Sale.is_active.is_(True))
            .order_by(Sale.created_at.desc())
        )
        return list(db.execute(stmt).scalars().all())

    @classmethod
    def financial_summary(cls, db: Session) -> dict:
        stmt = (
            select(
                func.count(Sale.id).label("total_sales"),
                func.coalesce(func.sum(Sale.total_commission), 0).label("total_commission"),
                func.coalesce(func.sum(Sale.net_commission), 0).label("net_commission"),
                func.coalesce(func.sum(Sale.seller_commission), 0).label("seller_commission"),
                func.coalesce(func.sum(Sale.shopee_commission), 0).label("shopee_commission"),
            )
            .where(Sale.is_active.is_(True))
        )
        row = db.execute(stmt).one()
        return {
            "total_sales": row.total_sales,
            "total_commission": float(row.total_commission),
            "net_commission": float(row.net_commission),
            "seller_commission": float(row.seller_commission),
            "shopee_commission": float(row.shopee_commission),
        }

    @classmethod
    def pending_summary(cls, db: Session) -> dict:
        stmt = (
            select(
                func.count(Sale.id).label("count"),
                func.coalesce(func.sum(Sale.net_commission), 0).label("pending"),
            )
            .where(Sale.status == "pendente", Sale.is_active.is_(True))
        )
        row = db.execute(stmt).one()
        return {"pending_count": row.count, "pending_amount": float(row.pending)}

    @classmethod
    def confirmed_summary(cls, db: Session) -> dict:
        stmt = (
            select(
                func.count(Sale.id).label("count"),
                func.coalesce(func.sum(Sale.net_commission), 0).label("confirmed"),
            )
            .where(Sale.status == "confirmada", Sale.is_active.is_(True))
        )
        row = db.execute(stmt).one()
        return {"confirmed_count": row.count, "confirmed_amount": float(row.confirmed)}
