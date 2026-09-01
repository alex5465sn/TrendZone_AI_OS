"""
TrendZone AI OS
================================

Marketplace API.
"""

from fastapi import APIRouter
from fastapi import Query

from app.services.marketplace_service import MarketplaceBusiness

from app.api.response import ResponseBuilder

router = APIRouter(

    prefix="/marketplace",

    tags=["Marketplace"],

)

service = MarketplaceBusiness()


@router.get("/products")
def products(

    keyword: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    sortType: int = Query(default=1),

):

    data = service.search_products(

        marketplace_name="shopee",

        keyword=keyword,

        page=page,

        limit=limit,

        sortType=sortType,

    )

    return ResponseBuilder.success(
        data=data,
    )


@router.get("/shops")
def shops(

    keyword: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    sortType: int = Query(default=1),

):

    data = service.search_shops(

        marketplace_name="shopee",

        keyword=keyword,

        page=page,

        limit=limit,

        sortType=sortType,

    )

    return ResponseBuilder.success(
        data=data,
    )


@router.get("/offers")
def offers(

    keyword: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    sortType: int = Query(default=1),

):

    data = service.search_offers(

        marketplace_name="shopee",

        keyword=keyword,

        page=page,

        limit=limit,

        sortType=sortType,

    )

    return ResponseBuilder.success(
        data=data,
    )
