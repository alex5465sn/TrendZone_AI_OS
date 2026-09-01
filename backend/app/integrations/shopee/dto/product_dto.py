"""
TrendZone AI OS
================================

Shopee Product DTO

Representa um produto padronizado
recebido da API da Shopee.

Todos os Parsers devem retornar
este objeto.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class ProductDTO:

    item_id: int

    shop_id: int

    name: str

    image: Optional[str] = None

    price: float = 0.0

    commission: float = 0.0

    rating: float = 0.0

    sales: int = 0

    stock: int = 0

    currency: str = "BRL"

    offer_link: Optional[str] = None

    category: Optional[str] = None

    marketplace: str = "Shopee"