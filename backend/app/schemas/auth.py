"""
TrendZone AI OS
===============================

Schemas de autenticação.
"""

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class LoginRequest(BaseModel):
    """
    Dados enviados para login.
    """

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=255,
    )


class Token(BaseModel):
    """
    JWT retornado pela API.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    access_token: str

    token_type: str = "bearer"