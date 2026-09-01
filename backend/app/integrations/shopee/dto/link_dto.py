"""
TrendZone AI OS
================================

Shopee Link DTO
"""

from dataclasses import dataclass


@dataclass(slots=True)
class LinkDTO:

    original_url: str

    short_url: str