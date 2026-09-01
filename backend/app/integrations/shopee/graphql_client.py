"""
TrendZone AI OS
================================

Shopee GraphQL Client

Camada responsável por executar
operações GraphQL utilizando
o ShopeeClient.

Não possui regras de negócio.

Responsabilidades:

- Executar Queries
- Executar Mutations
- Retornar resposta bruta
"""

from __future__ import annotations

from typing import Any

from app.integrations.shopee.client import ShopeeClient


class ShopeeGraphQLClient:

    def __init__(
        self,
        access_token: str | None = None,
    ) -> None:

        self.client = ShopeeClient(
            access_token=access_token,
        )

    # =====================================================
    # EXECUTE
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