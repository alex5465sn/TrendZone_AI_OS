"""
TrendZone AI OS
================================

Schemas do Marketplace (busca em tempo real na Shopee).
"""

from pydantic import BaseModel


class PromoteRequest(BaseModel):
    item_id: int
    product_name: str
    price: float = 0
    commission_rate: float = 0
    rating_star: float = 0
    sales: int = 0
    offer_link: str = ""
    image_url: str = ""
    tone: str = "oferta"
