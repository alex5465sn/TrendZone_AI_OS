"""
TrendZone AI OS
================================

Shopee Report DTO
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ReportDTO:

    clicks: int = 0

    orders: int = 0

    sales: float = 0.0

    commission: float = 0.0

    conversion_rate: float = 0.0