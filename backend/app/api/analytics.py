"""
TrendZone AI OS
================================

Analytics API

Endpoints para análises e métricas.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.repositories.product_repository import ProductRepository
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


# =====================================================
# PRODUCT ANALYTICS
# =====================================================

@router.get("/products/summary")
def get_products_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retorna resumo de produtos."""

    products = ProductRepository.get_all(db)

    total = len(products)
    avg_score = sum(p.score for p in products) / total if total > 0 else 0
    avg_commission = sum(float(p.commission) for p in products) / total if total > 0 else 0
    avg_rating = sum(float(p.rating) for p in products) / total if total > 0 else 0
    total_sales = sum(p.sales for p in products)

    return ResponseBuilder.success(
        data={
            "total_products": total,
            "average_score": round(avg_score, 2),
            "average_commission": round(avg_commission, 2),
            "average_rating": round(avg_rating, 2),
            "total_sales": total_sales,
        },
    )


@router.get("/products/by-score")
def get_products_by_score(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retorna produtos agrupados por score."""

    products = ProductRepository.get_all(db)

    # Agrupar por faixas de score
    ranges = {
        "80-100": [],
        "60-79": [],
        "40-59": [],
        "0-39": [],
    }

    for p in products:
        score = p.score or 0
        if score >= 80:
            ranges["80-100"].append(p)
        elif score >= 60:
            ranges["60-79"].append(p)
        elif score >= 40:
            ranges["40-59"].append(p)
        else:
            ranges["0-39"].append(p)

    return ResponseBuilder.success(
        data={
            "80-100": len(ranges["80-100"]),
            "60-79": len(ranges["60-79"]),
            "40-59": len(ranges["40-59"]),
            "0-39": len(ranges["0-39"]),
        },
    )


@router.get("/products/by-commission")
def get_products_by_commission(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retorna produtos agrupados por comissão."""

    products = ProductRepository.get_all(db)

    # Agrupar por faixas de comissão
    ranges = {
        "0-5%": 0,
        "5-10%": 0,
        "10-15%": 0,
        "15-20%": 0,
        "20%+": 0,
    }

    for p in products:
        commission = float(p.commission) if p.commission else 0
        if commission < 5:
            ranges["0-5%"] += 1
        elif commission < 10:
            ranges["5-10%"] += 1
        elif commission < 15:
            ranges["10-15%"] += 1
        elif commission < 20:
            ranges["15-20%"] += 1
        else:
            ranges["20%+"] += 1

    return ResponseBuilder.success(
        data=ranges,
    )


@router.get("/products/top-10")
def get_top_10_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retorna top 10 produtos por score."""

    products = ProductRepository.get_all(db)
    sorted_products = sorted(products, key=lambda p: p.score or 0, reverse=True)[:10]

    return ResponseBuilder.success(
        data=[
            {
                "id": p.id,
                "name": p.name,
                "score": p.score,
                "commission": float(p.commission),
                "sales": p.sales,
                "rating": p.rating,
            }
            for p in sorted_products
        ],
    )


# =====================================================
# COMMISSION ANALYTICS
# =====================================================

@router.get("/commission/summary")
def get_commission_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retorna resumo de comissões."""

    products = ProductRepository.get_all(db)

    total_commission = sum(float(p.commission) * p.sales for p in products)
    avg_commission_per_product = sum(float(p.commission) for p in products) / len(products) if products else 0

    return ResponseBuilder.success(
        data={
            "total_commission": round(total_commission, 2),
            "average_commission_per_product": round(avg_commission_per_product, 2),
            "total_products": len(products),
        },
    )


# =====================================================
# SALES ANALYTICS
# =====================================================

@router.get("/sales/summary")
def get_sales_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retorna resumo de vendas."""

    products = ProductRepository.get_all(db)

    total_sales = sum(p.sales for p in products)
    avg_sales = total_sales / len(products) if products else 0

    return ResponseBuilder.success(
        data={
            "total_sales": total_sales,
            "average_sales_per_product": round(avg_sales, 2),
            "total_products": len(products),
        },
    )


@router.get("/sales/by-rating")
def get_sales_by_rating(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retorna vendas agrupadas por avaliação."""

    products = ProductRepository.get_all(db)

    # Agrupar por faixas de rating
    ranges = {
        "4.5-5.0": 0,
        "4.0-4.4": 0,
        "3.5-3.9": 0,
        "3.0-3.4": 0,
        "0-2.9": 0,
    }

    for p in products:
        rating = float(p.rating) if p.rating else 0
        if rating >= 4.5:
            ranges["4.5-5.0"] += p.sales
        elif rating >= 4.0:
            ranges["4.0-4.4"] += p.sales
        elif rating >= 3.5:
            ranges["3.5-3.9"] += p.sales
        elif rating >= 3.0:
            ranges["3.0-3.4"] += p.sales
        else:
            ranges["0-2.9"] += p.sales

    return ResponseBuilder.success(
        data=ranges,
    )
