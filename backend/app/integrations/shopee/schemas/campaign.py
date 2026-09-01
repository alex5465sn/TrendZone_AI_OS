from pydantic import BaseModel


class CampaignFilters(BaseModel):

    keyword: str | None = None

    page: int = 1

    limit: int = 20

    sortType: int = 1

    shopId: int | None = None

    shopType: list[int] | None = None

    sellerCommCoveRatio: str | None = None

    isKeySeller: bool | None = None