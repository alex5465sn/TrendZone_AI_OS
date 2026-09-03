"""
TrendZone AI OS
================================

Schemas das Contas de Marketplace dos usuários.

Tokens NUNCA são devolvidos na resposta — apenas
indicadores de presença (has_access_token).
"""

from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class MarketplaceAccountCreate(BaseModel):
    """
    Conexão de uma conta de marketplace.
    """

    marketplace: str = Field(
        min_length=2,
        max_length=30,
    )

    access_token: str = Field(
        min_length=10,
        max_length=2000,
    )

    refresh_token: str | None = Field(
        default=None,
        max_length=2000,
    )

    extra: str | None = Field(
        default=None,
        max_length=4000,
    )


class MarketplaceAccountUpdate(BaseModel):
    """
    Atualização (ex.: renovação de token).
    """

    access_token: str | None = Field(
        default=None,
        min_length=10,
        max_length=2000,
    )

    refresh_token: str | None = Field(
        default=None,
        max_length=2000,
    )

    extra: str | None = Field(
        default=None,
        max_length=4000,
    )

    status: str | None = Field(
        default=None,
        max_length=20,
    )


class MarketplaceAccountResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    uuid: str

    marketplace: str

    has_access_token: bool

    has_refresh_token: bool

    status: str

    last_validated_at: str

    is_active: bool

    created_at: datetime

    updated_at: datetime
