"""
TrendZone AI OS
================================

Shopee Gateway

Camada responsável por centralizar
a comunicação com a Shopee Affiliate API.

Não contém regras de negócio.

Responsabilidades:

- REST
- GraphQL
- Interface única para os Services
"""

from __future__ import annotations

from typing import Any

from app.integrations.shopee.client import ShopeeClient


class ShopeeGateway:

    def __init__(
        self,
        access_token: str | None = None,
    ) -> None:

        self.client = ShopeeClient(
            access_token=access_token,
        )

    # =====================================================
    # REST GET
    # =====================================================

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ) -> dict[str, Any]:

        return self.client.get(

            endpoint=endpoint,

            params=params,

        )

    # =====================================================
    # REST POST
    # =====================================================

    def post(
        self,
        endpoint: str,
        payload: dict | None = None,
    ) -> dict[str, Any]:

        return self.client.post(

            endpoint=endpoint,

            payload=payload,

        )

    # =====================================================
    # GRAPHQL
    # =====================================================

    def execute(
        self,
        *,
        query: str,
        variables: dict | None = None,
    ) -> dict[str, Any]:

        return self.client.execute(

            query=query,

            variables=variables,

        )