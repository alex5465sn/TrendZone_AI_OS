"""
TrendZone AI OS

Product Snapshot Repository.

Acesso a dados da tabela product_snapshots.
Sem regra de negócio (fica no MomentumService).
"""

from datetime import datetime, timedelta

from sqlalchemy import delete, select

from sqlalchemy.orm import Session

from app.models.product_snapshot import ProductSnapshot

RETENTION_DAYS = 30


class ProductSnapshotRepository:

    @staticmethod
    def get_latest(
        db: Session,
        marketplace: str,
        item_id: int,
    ) -> ProductSnapshot | None:

        stmt = (
            select(ProductSnapshot)
            .where(
                ProductSnapshot.marketplace == marketplace,
                ProductSnapshot.item_id == item_id,
            )
            .order_by(ProductSnapshot.captured_at.desc())
            .limit(1)
        )

        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_baseline(
        db: Session,
        marketplace: str,
        item_id: int,
        max_age_days: int = 7,
        min_age_hours: int = 6,
    ) -> ProductSnapshot | None:
        """
        Snapshot de referência para cálculo de momentum:
        o mais antigo dentro da janela de `max_age_days`,
        desde que seja pelo menos `min_age_hours` mais
        antigo que agora (baseline mínimo para medir
        crescimento).
        """

        now = datetime.utcnow()

        upper = now - timedelta(hours=min_age_hours)

        lower = now - timedelta(days=max_age_days)

        stmt = (
            select(ProductSnapshot)
            .where(
                ProductSnapshot.marketplace == marketplace,
                ProductSnapshot.item_id == item_id,
                ProductSnapshot.captured_at >= lower,
                ProductSnapshot.captured_at <= upper,
            )
            .order_by(ProductSnapshot.captured_at.asc())
            .limit(1)
        )

        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def create(
        db: Session,
        snapshot: ProductSnapshot,
    ) -> ProductSnapshot:

        db.add(snapshot)

        db.commit()

        db.refresh(snapshot)

        return snapshot

    @staticmethod
    def purge_old(db: Session) -> int:
        """
        Remove snapshots mais antigos que RETENTION_DAYS.
        Retorna quantas linhas foram removidas.
        """

        cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)

        result = db.execute(
            delete(ProductSnapshot).where(
                ProductSnapshot.captured_at < cutoff
            )
        )

        db.commit()

        return result.rowcount or 0
