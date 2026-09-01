from pydantic import BaseModel


class ProductFilters(BaseModel):

    keyword: str | None = None

    page: int = 1

    limit: int = 20

    sortType: int = 1

    listType: int = 0

    matchId: int | None = None

    shopId: int | None = None

    itemId: int | None = None

    categoryId: int | None = None

    isAMSOffer: bool | None = None

    isKeySeller: bool | None = None