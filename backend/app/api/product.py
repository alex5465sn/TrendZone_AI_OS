"""
TrendZone AI OS
================================

Products API

Endpoints oficiais da entidade Product.
"""

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

from app.services.product_service import ProductService

from app.api.response import ResponseBuilder

router = APIRouter(

    prefix="/products",

    tags=["Products"],

)


@router.get("/")

def get_products(

    category: Optional[str] = None,

    db: Session = Depends(get_db),

):

    products = ProductService.get_all(db, category=category)

    return ResponseBuilder.success(

        data=[

            ProductResponse.model_validate(product).model_dump(mode="json")

            for product in products

        ]

    )


@router.get("/{product_id}")

def get_product(

    product_id: int,

    db: Session = Depends(get_db),

):

    product = ProductService.get_by_id(

        db,

        product_id,

    )

    if product is None:

        raise ValueError(

            "Produto não encontrado."

        )

    return ResponseBuilder.success(

        data=ProductResponse.model_validate(product).model_dump(mode="json")

    )


@router.post("/")

def create_product(

    data: ProductCreate,

    db: Session = Depends(get_db),

):

    product = ProductService.create(

        db,

        data,

    )

    return ResponseBuilder.success(

        data=ProductResponse.model_validate(product).model_dump(mode="json"),

        message="Produto criado.",

        status_code=201,

    )


@router.put("/{product_id}")

def update_product(

    product_id: int,

    data: ProductUpdate,

    db: Session = Depends(get_db),

):

    product = ProductService.get_by_id(

        db,

        product_id,

    )

    if product is None:

        raise ValueError(

            "Produto não encontrado."

        )

    updated = ProductService.update(

        db,

        product,

        data,

    )

    return ResponseBuilder.success(

        data=ProductResponse.model_validate(updated).model_dump(mode="json"),

        message="Produto atualizado.",

    )


@router.delete("/{product_id}")

def delete_product(

    product_id: int,

    db: Session = Depends(get_db),

):

    product = ProductService.get_by_id(

        db,

        product_id,

    )

    if product is None:

        raise ValueError(

            "Produto não encontrado."

        )

    ProductService.soft_delete(

        db,

        product,

    )

    return ResponseBuilder.success(

        message="Produto removido."

    )