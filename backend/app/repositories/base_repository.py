"""
TrendZone AI OS
================================

Base Repository.

Centraliza todas as operações CRUD.

Todos os Repositories da aplicação
devem herdar desta classe.
"""

from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):

    model = None

    # =====================================================
    # CREATE
    # =====================================================

    @classmethod
    def create(
        cls,
        db: Session,
        obj: ModelType,
    ) -> ModelType:

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    # =====================================================
    # UPDATE
    # =====================================================

    @classmethod
    def update(
        cls,
        db: Session,
        obj: ModelType,
    ) -> ModelType:

        db.commit()
        db.refresh(obj)

        return obj

    # =====================================================
    # DELETE
    # =====================================================

    @classmethod
    def delete(
        cls,
        db: Session,
        obj: ModelType,
    ) -> None:

        db.delete(obj)
        db.commit()

    # =====================================================
    # SOFT DELETE
    # =====================================================

    @classmethod
    def soft_delete(
        cls,
        db: Session,
        obj: ModelType,
    ) -> None:

        obj.is_active = False

        db.commit()
        db.refresh(obj)

    # =====================================================
    # RESTORE
    # =====================================================

    @classmethod
    def restore(
        cls,
        db: Session,
        obj: ModelType,
    ) -> None:

        obj.is_active = True

        db.commit()
        db.refresh(obj)

    # =====================================================
    # GET ID
    # =====================================================

    @classmethod
    def get_by_id(
        cls,
        db: Session,
        id: int,
    ) -> ModelType | None:

        stmt = (
            select(cls.model)
            .where(
                cls.model.id == id,
                cls.model.is_active.is_(True),
            )
        )

        return db.execute(stmt).scalar_one_or_none()

    # =====================================================
    # GET UUID
    # =====================================================

    @classmethod
    def get_by_uuid(
        cls,
        db: Session,
        uuid: str,
    ) -> ModelType | None:

        stmt = (
            select(cls.model)
            .where(
                cls.model.uuid == uuid,
                cls.model.is_active.is_(True),
            )
        )

        return db.execute(stmt).scalar_one_or_none()

    # =====================================================
    # GET ALL
    # =====================================================

    @classmethod
    def get_all(
        cls,
        db: Session,
    ) -> list[ModelType]:

        stmt = (
            select(cls.model)
            .where(
                cls.model.is_active.is_(True)
            )
        )

        return list(db.execute(stmt).scalars().all())

    # =====================================================
    # GET MULTI
    # =====================================================

    @classmethod
    def get_multi(
        cls,
        db: Session,
        **filters: Any,
    ) -> list[ModelType]:

        stmt = select(cls.model)

        for field, value in filters.items():

            if hasattr(cls.model, field):

                stmt = stmt.where(
                    getattr(cls.model, field) == value
                )

        stmt = stmt.where(
            cls.model.is_active.is_(True)
        )

        return list(
            db.execute(stmt).scalars().all()
        )

    # =====================================================
    # EXISTS
    # =====================================================

    @classmethod
    def exists(
        cls,
        db: Session,
        **filters: Any,
    ) -> bool:

        stmt = select(cls.model)

        for field, value in filters.items():

            if hasattr(cls.model, field):

                stmt = stmt.where(
                    getattr(cls.model, field) == value
                )

        stmt = stmt.limit(1)

        return db.execute(stmt).scalar_one_or_none() is not None

    # =====================================================
    # PAGINATION
    # =====================================================

    @classmethod
    def paginate(
        cls,
        db: Session,
        page: int = 1,
        page_size: int = 20,
    ) -> list[ModelType]:

        stmt = (
            select(cls.model)
            .where(
                cls.model.is_active.is_(True)
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        return list(
            db.execute(stmt).scalars().all()
        )

    # =====================================================
    # COUNT
    # =====================================================

    @classmethod
    def count(
        cls,
        db: Session,
    ) -> int:

        stmt = (
            select(
                func.count(cls.model.id)
            )
            .where(
                cls.model.is_active.is_(True)
            )
        )

        return db.scalar(stmt) or 0