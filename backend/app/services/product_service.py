"""
TrendZone AI OS
================================

Product Service.

Responsável pelas regras de negócio
da entidade Product.

Nunca acessa o banco diretamente.

Toda operação passa pelo Repository.
"""

from sqlalchemy.orm import Session

from app.models.product import Product

from app.repositories.product_repository import ProductRepository

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
)

from app.services.base_service import BaseService

from app.services.product_score import ProductScore

from app.core.exceptions import (
    ProductAlreadyExists,
    ProductNotFound,
)


class ProductService(BaseService):

    SERVICE_NAME = "PRODUCT_SERVICE"

    # =====================================================
    # CREATE
    # =====================================================

    @classmethod
    def create(
        cls,
        db: Session,
        data: ProductCreate,
    ) -> Product:

        cls.log_info(
            "Criando produto..."
        )

        existing = ProductRepository.get_by_item_id(
            db,
            data.item_id,
        )

        if existing:

            cls.log_warning(
                "Produto já existe."
            )

            raise ProductAlreadyExists()

        score = ProductScore.calculate(
            commission=float(data.commission),
            rating=data.rating,
            sales=data.sales,
        )

        product = Product(

            item_id=data.item_id,

            shop_id=data.shop_id,

            category=data.category or "geral",

            name=data.name,

            image=data.image,

            offer_link=data.offer_link,

            price=data.price,

            commission=data.commission,

            rating=data.rating,

            sales=data.sales,

            score=score,

        )

        product = ProductRepository.create(
            db,
            product,
        )

        cls.log_success(
            "Produto criado."
        )

        return product

    # =====================================================
    # UPDATE
    # =====================================================

    @classmethod
    def update(
        cls,
        db: Session,
        product: Product,
        data: ProductUpdate,
    ) -> Product:

        cls.log_info(
            "Atualizando produto..."
        )

        values = data.model_dump(
            exclude_unset=True
        )

        for key, value in values.items():

            setattr(
                product,
                key,
                value,
            )

        product = ProductRepository.update(
            db,
            product,
        )

        cls.log_success(
            "Produto atualizado."
        )

        return product

    # =====================================================
    # GET
    # =====================================================

    @classmethod
    def get_all(
        cls,
        db: Session,
        category: str | None = None,
    ):

        if category:
            return ProductRepository.get_by_category(db, category)

        return ProductRepository.get_all(db)

    @classmethod
    def get_by_id(
        cls,
        db: Session,
        product_id: int,
    ) -> Product:

        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if not product:

            raise ProductNotFound()

        return product

    @classmethod
    def get_by_uuid(
        cls,
        db: Session,
        uuid: str,
    ) -> Product:

        product = ProductRepository.get_by_uuid(
            db,
            uuid,
        )

        if not product:

            raise ProductNotFound()

        return product

    @classmethod
    def search(
        cls,
        db: Session,
        text: str,
    ):

        return ProductRepository.search(
            db,
            text,
        )

    # =====================================================
    # RANKINGS
    # =====================================================

    @classmethod
    def top_score(
        cls,
        db: Session,
        limit: int = 10,
    ):

        return ProductRepository.get_top_score(
            db,
            limit,
        )

    @classmethod
    def top_sales(
        cls,
        db: Session,
        limit: int = 10,
    ):

        return ProductRepository.get_top_sales(
            db,
            limit,
        )

    # =====================================================
    # DASHBOARD
    # =====================================================

    @classmethod
    def statistics(
        cls,
        db: Session,
    ) -> dict:

        return {

            "total_products":

                ProductRepository.count(db),

        }

    # =====================================================
    # SOFT DELETE
    # =====================================================

    @classmethod
    def soft_delete(
        cls,
        db: Session,
        product: Product,
    ):

        cls.log_warning(
            "Desativando produto..."
        )

        ProductRepository.soft_delete(
            db,
            product,
        )

    @classmethod
    def restore(
        cls,
        db: Session,
        product: Product,
    ):

        cls.log_info(
            "Restaurando produto..."
        )

        ProductRepository.restore(
            db,
            product,
        )

    @classmethod
    def delete(
        cls,
        db: Session,
        product: Product,
    ):

        cls.log_warning(
            "Removendo produto..."
        )

        ProductRepository.delete(
            db,
            product,
        )
