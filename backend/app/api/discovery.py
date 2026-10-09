from fastapi import APIRouter, Depends
from pydantic import BaseModel as Schema
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.product import Product
from app.api.response import ResponseBuilder

from app.services.momentum_service import MomentumService

router = APIRouter(
    prefix="/discovery",
    tags=["Product Discovery"],
)


class DiscoveryFilter(Schema):
    min_commission: float = 10.0
    max_competition: int = 50
    min_rating: float = 4.0
    min_sales: int = 10
    sort_by: str = "emerging"


@router.get("/radar")
def product_radar(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Product Radar — prioriza produtos COMEÇANDO a vencer.

    radar_score (0–100) = 50% momentum (crescimento de
    vendas desde o baseline de até 7 dias) + 30% score
    interno + 20% aderência à faixa de preço R$20–100.
    """

    items = MomentumService.radar(db, limit=max(1, min(limit, 50)))

    return ResponseBuilder.success(data=items)


@router.get("/emerging")
def emerging_products(
    min_commission: float = 10.0,
    min_rating: float = 4.0,
    max_sales: int = 500,
    min_sales: int = 5,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Product.commission é salvo como fração (ex.: 0.13 = 13%), enquanto
    # min_commission chega da tela como percentual (ex.: 10 = 10%).
    products = (
        db.query(Product)
        .filter(
            Product.is_active == True,
            Product.commission >= min_commission / 100,
            Product.rating >= min_rating,
            Product.sales >= min_sales,
            Product.sales <= max_sales,
        )
        .order_by(Product.created_at.desc())
        .limit(limit)
        .all()
    )

    result = [
        {
            "id": p.id,
            "name": p.name,
            "image": p.image,
            "price": float(p.price),
            "commission": round(float(p.commission) * 100, 2),
            "rating": p.rating,
            "sales": p.sales,
            "score": p.score,
            "recommendation": p.recommendation,
            "offer_link": p.offer_link,
            "opportunity_index": round(
                (float(p.commission) * 100 * p.rating) / max(p.sales, 1) * 100, 2
            ),
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in products
    ]

    result.sort(key=lambda x: x["opportunity_index"], reverse=True)

    return ResponseBuilder.success(data=result)


@router.get("/high-commission")
def high_commission_products(
    min_commission: float = 10.0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    products = (
        db.query(Product)
        .filter(
            Product.is_active == True,
            Product.commission >= min_commission / 100,
        )
        .order_by(Product.commission.desc(), Product.score.desc())
        .limit(limit)
        .all()
    )

    result = [
        {
            "id": p.id,
            "name": p.name,
            "image": p.image,
            "price": float(p.price),
            "commission": round(float(p.commission) * 100, 2),
            "rating": p.rating,
            "sales": p.sales,
            "score": p.score,
            "offer_link": p.offer_link,
        }
        for p in products
    ]

    return ResponseBuilder.success(data=result)


@router.get("/trending")
def trending_products(
    min_sales: int = 10,
    min_rating: float = 3.5,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    products = (
        db.query(Product)
        .filter(
            Product.is_active == True,
            Product.sales > min_sales,
            Product.rating >= min_rating,
        )
        .order_by(Product.sales.desc(), Product.score.desc())
        .limit(limit)
        .all()
    )

    result = [
        {
            "id": p.id,
            "name": p.name,
            "image": p.image,
            "price": float(p.price),
            "commission": round(float(p.commission) * 100, 2),
            "rating": p.rating,
            "sales": p.sales,
            "score": p.score,
            "offer_link": p.offer_link,
            "heat_index": round(p.sales * p.rating * float(p.commission), 2),
        }
        for p in products
    ]

    return ResponseBuilder.success(data=result)


@router.get("/niche-gaps")
def niche_gap_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    niches = (
        db.query(
            Product.marketplace,
            func.count(Product.id).label("total"),
            func.avg(Product.commission).label("avg_commission"),
            func.avg(Product.rating).label("avg_rating"),
            func.avg(Product.sales).label("avg_sales"),
            func.avg(Product.score).label("avg_score"),
        )
        .filter(Product.is_active == True)
        .group_by(Product.marketplace)
        .all()
    )

    total_products = db.query(func.count(Product.id)).filter(Product.is_active == True).scalar() or 1

    result = [
        {
            "marketplace": n.marketplace,
            "total_products": n.total,
            "avg_commission": round(float(n.avg_commission or 0), 2),
            "avg_rating": round(float(n.avg_rating or 0), 2),
            "avg_sales": round(float(n.avg_sales or 0), 0),
            "avg_score": round(float(n.avg_score or 0), 2),
            "market_share": round(n.total / total_products * 100, 2),
        }
        for n in niches
    ]

    return ResponseBuilder.success(data=result)


@router.get("/recommendations")
def smart_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    emerging = (
        db.query(Product)
        .filter(
            Product.is_active == True,
            Product.commission >= 0.08,
            Product.rating >= 3.5,
            Product.sales <= 500,
            Product.sales >= 1,
        )
        .order_by(Product.created_at.desc())
        .limit(5)
        .all()
    )

    top_performers = (
        db.query(Product)
        .filter(
            Product.is_active == True,
            Product.score >= 40,
        )
        .order_by(Product.score.desc())
        .limit(5)
        .all()
    )

    high_profit = (
        db.query(Product)
        .filter(
            Product.is_active == True,
            Product.commission >= 0.10,
            Product.rating >= 3.5,
        )
        .order_by(Product.commission.desc())
        .limit(5)
        .all()
    )

    def serialize(p, tag):
        return {
            "id": p.id,
            "name": p.name,
            "image": p.image,
            "price": float(p.price),
            "commission": round(float(p.commission) * 100, 2),
            "rating": p.rating,
            "sales": p.sales,
            "score": p.score,
            "tag": tag,
        }

    result = {
        "emerging": [serialize(p, "EMERGENTE") for p in emerging],
        "top_performers": [serialize(p, "TOP PERFORMER") for p in top_performers],
        "high_profit": [serialize(p, "ALTA COMISSÃO") for p in high_profit],
    }

    return ResponseBuilder.success(data=result)
