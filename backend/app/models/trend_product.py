"""
TrendZone AI OS
================================

Trend Product

Modelo interno utilizado por todo
o TrendZone AI OS.

Nenhum módulo do sistema deve depender
dos objetos retornados pela Shopee.

Todo marketplace deve ser convertido
para este modelo.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class TrendProduct:

    item_id: int

    shop_id: int

    name: str

    image: Optional[str]

    price: float

    commission: float

    rating: float

    sales: int

    stock: int

    currency: str

    offer_link: Optional[str]

    category: Optional[str]

    marketplace: str

    score: float = 0.0

    decision: str = ""

    ranking: int = 0