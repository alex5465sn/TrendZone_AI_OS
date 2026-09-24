"""
TrendZone AI OS
===============================

Schemas responsáveis pelos Produtos.

Representam o contrato entre:

Frontend
↓
API
↓
Services
↓
Database
"""

from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


# =====================================================
# CREATE
# =====================================================

class ProductCreate(BaseModel):
    """
    Cadastro de um novo produto.
    """

    item_id: int

    shop_id: int

    category: str = "geral"

    name: str = Field(
        min_length=3,
        max_length=255,
    )

    price: Decimal = Field(
        ge=0,
    )

    commission: Decimal = Field(
        default=0,
        ge=0,
    )

    image: str = ""

    offer_link: str = ""

    rating: float = Field(
        default=0.0,
        ge=0,
        le=5,
    )

    sales: int = Field(
        default=0,
        ge=0,
    )


# =====================================================
# UPDATE
# =====================================================

class ProductUpdate(BaseModel):
    """
    Atualização parcial do produto.
    """

    name: str | None = None

    category: str | None = None

    price: Decimal | None = None

    commission: Decimal | None = None

    image: str | None = None

    offer_link: str | None = None

    rating: float | None = None

    sales: int | None = None

    score: float | None = None

    confidence: float | None = None

    recommendation: str | None = None

    is_active: bool | None = None


# =====================================================
# RESPONSE
# =====================================================

class ProductResponse(BaseModel):
    """
    Produto retornado pela API.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    uuid: str

    item_id: int

    shop_id: int

    category: str

    name: str

    image: str

    offer_link: str

    price: Decimal

    commission: Decimal

    rating: float

    sales: int

    score: float

    confidence: float

    recommendation: str

    is_active: bool

    created_at: datetime

    updated_at: datetime

    deleted_at: datetime | None


# =====================================================
# LIST RESPONSE
# =====================================================

class ProductListResponse(BaseModel):
    """
    Retorno paginado de produtos.
    """

    items: list[ProductResponse]

    total: int

    page: int

    page_size: int