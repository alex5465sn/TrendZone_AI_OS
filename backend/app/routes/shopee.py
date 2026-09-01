from fastapi import APIRouter
from fastapi import Header
from fastapi import HTTPException

from app.controllers import ShopeeController

from app.integrations.shopee.schemas import (
    ProductFilters,
    CampaignFilters,
    ReportFilters,
)

router = APIRouter(
    prefix="/shopee",
    tags=["Shopee Affiliate"],
)


def get_controller(
    authorization: str | None,
) -> ShopeeController:

    if authorization is None:

        raise HTTPException(
            status_code=401,
            detail="Authorization Header não enviada.",
        )

    token = authorization.replace(
        "Bearer ",
        "",
    )

    return ShopeeController(
        token,
    )


@router.post(
    "/products"
)
def products(

    filters: ProductFilters,

    authorization: str | None = Header(
        default=None,
    ),

):

    controller = get_controller(
        authorization,
    )

    return controller.products.list(
        filters.model_dump(
            exclude_none=True,
        )
    )


@router.post(
    "/campaigns"
)
def campaigns(

    filters: CampaignFilters,

    authorization: str | None = Header(
        default=None,
    ),

):

    controller = get_controller(
        authorization,
    )

    return controller.campaigns.list(
        filters.model_dump(
            exclude_none=True,
        )
    )


@router.post(
    "/reports"
)
def reports(

    filters: ReportFilters,

    authorization: str | None = Header(
        default=None,
    ),

):

    controller = get_controller(
        authorization,
    )

    return controller.reports.list(
        filters.model_dump(
            exclude_none=True,
        )
    )


@router.get(
    "/status"
)
def status(

    authorization: str | None = Header(
        default=None,
    ),

):

    controller = get_controller(
        authorization,
    )

    return {

        "status": "online",

        "client": controller.__class__.__name__,

    }