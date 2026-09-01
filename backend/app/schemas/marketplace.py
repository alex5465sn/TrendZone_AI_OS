"""
TrendZone AI OS
================================

Marketplace Schemas.
"""

from pydantic import BaseModel


class MarketplaceSearch(BaseModel):

    keyword: str | None = None

    page: int = 1

    limit: int = 20

    sort_type: int = 1


class MarketplaceShortLink(BaseModel):

    url: str

    sub_ids: list[str] = []