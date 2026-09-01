"""
TrendZone AI OS
================================

Domain Product

Representa um produto dentro do domínio
do TrendZone AI OS.

Este objeto não conhece banco de dados,
API externa ou GraphQL.

Toda regra de negócio trabalha
exclusivamente com esta classe.
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