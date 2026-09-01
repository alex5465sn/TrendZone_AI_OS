"""
TrendZone AI OS
================================

Marketplace Types

Enum oficial dos marketplaces.
"""

from enum import Enum


class Marketplace(str, Enum):

    SHOPEE = "shopee"

    AMAZON = "amazon"

    MERCADO_LIVRE = "mercado_livre"

    TIKTOK = "tiktok"

    ALIEXPRESS = "aliexpress"