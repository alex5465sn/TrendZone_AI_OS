"""
GraphQL oficial da Shopee Affiliate API.

Todas as Queries e Mutations ficam centralizadas aqui.
"""

from .products import PRODUCT_OFFER_V2
from .campaigns import (
    SHOP_OFFER_V2,
    SHOPEE_OFFER_V2,
)
from .reports import (
    CONVERSION_REPORT,
    VALIDATED_REPORT,
)
from .links import (
    GENERATE_SHORT_LINK,
    GENERATE_BATCH_SHORT_LINK,
)
from .feeds import (
    LIST_ITEM_FEEDS,
    GET_ITEM_FEED_DATA,
)

__all__ = [
    "PRODUCT_OFFER_V2",
    "SHOP_OFFER_V2",
    "SHOPEE_OFFER_V2",
    "CONVERSION_REPORT",
    "VALIDATED_REPORT",
    "GENERATE_SHORT_LINK",
    "GENERATE_BATCH_SHORT_LINK",
    "LIST_ITEM_FEEDS",
    "GET_ITEM_FEED_DATA",
]