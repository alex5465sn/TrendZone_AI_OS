"""
TrendZone AI OS
================================

Shopee Authentication

Responsável por validar e armazenar
o token de acesso da Shopee.

Não realiza chamadas HTTP.
"""

from __future__ import annotations

from app.integrations.shopee.storage import TokenStorage
from app.integrations.shopee.validator import ShopeeValidator


class ShopeeAuth:
    """
    Camada responsável apenas pela autenticação.

    Não conhece:

    - ShopeeClient
    - GraphQL
    - Gateway
    """

    def __init__(
        self,
        access_token: str,
    ) -> None:

        ShopeeValidator.validate_token(
            access_token
        )

        self.storage = TokenStorage(
            access_token=access_token
        )

    @property
    def token(self) -> str:
        return self.storage.access_token

    @property
    def authenticated(self) -> bool:
        return self.storage.authenticated

    @property
    def expired(self) -> bool:
        return self.storage.expired

    def get_authorization_header(self) -> dict[str, str]:

        return {
            "Authorization": f"Bearer {self.token}"
        }