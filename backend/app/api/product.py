from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

from app.services.product_service import ProductService


router = APIRouter(

    prefix="/products",

    tags=["Products"],

)


# =====================================================
# LISTAR
# =====================================================

@router.get(
    "/",
    response_model=list[ProductResponse],
)
def get_products(
    db: Session = Depends(get_db),
):

    return ProductService.get_all(db)


# =====================================================
# BUSCAR POR ID
# =====================================================

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):

    product = ProductService.get_by_id(
        db,
        product_id,
    )

    if not product:

        raise HTTPException(

            status_code=404,

            detail="Produto não encontrado.",

        )

    return product


# =====================================================
# CADASTRAR
# =====================================================

@router.post(
    "/",
    response_model=ProductResponse,
)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
):

    try:

        return ProductService.create(
            db,
            data,
        )

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e),

        )


# =====================================================
# ATUALIZAR
# =====================================================

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
):

    product = ProductService.get_by_id(
        db,
        product_id,
    )

    if not product:

        raise HTTPException(

            status_code=404,

            detail="Produto não encontrado.",

        )

    return ProductService.update(
        db,
        product,
        data,
    )


# =====================================================
# DESATIVAR
# =====================================================

@router.delete(
    "/{product_id}",
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):

    product = ProductService.get_by_id(
        db,
        product_id,
    )

    if not product:

        raise HTTPException(

            status_code=404,

            detail="Produto não encontrado.",

        )

    ProductService.soft_delete(
        db,
        product,
    )

    return {

        "message": "Produto desativado com sucesso."

    }


# =====================================================
# RESTAURAR
# =====================================================

@router.patch(
    "/{product_id}/restore",
)
def restore_product(
    product_id: int,
    db: Session = Depends(get_db),
):

    product = ProductService.get_by_id(
        db,
        product_id,
    )

    if not product:

        raise HTTPException(

            status_code=404,

            detail="Produto não encontrado.",

        )

    ProductService.restore(
        db,
        product,
    )

    return {

        "message": "Produto restaurado."

    }


# =====================================================
# TOP SCORE
# =====================================================

@router.get(
    "/ranking/top-score",
)
def top_score(
    limit: int = 10,
    db: Session = Depends(get_db),
):

    return ProductService.top_score(
        db,
        limit,
    )


# =====================================================
# TOP VENDAS
# =====================================================

@router.get(
    "/ranking/top-sales",
)
def top_sales(
    limit: int = 10,
    db: Session = Depends(get_db),
):

    return ProductService.top_sales(
        db,
        limit,
    )


# =====================================================
# PESQUISA
# =====================================================

@router.get(
    "/search/{text}",
)
def search_products(
    text: str,
    db: Session = Depends(get_db),
):

    return ProductService.search(
        db,
        text,
    )


# =====================================================
# ESTATÍSTICAS
# =====================================================

@router.get(
    "/statistics",
)
def statistics(
    db: Session = Depends(get_db),
):

    return ProductService.statistics(
        db,
    )