"""
TrendZone AI OS
================================

GraphQL Executor

Executa consultas GraphQL
e padroniza o tratamento
das respostas.
"""

from __future__ import annotations

from typing import Any

from app.integrations.shopee.graphql_client import (
    ShopeeGraphQLClient,
)


class GraphQLExecutor:

    def __init__(
        self,
        access_token: str | None = None,
    ) -> None:

        self.client = ShopeeGraphQLClient(
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

        response = self.client.execute(

            query=query,

            variables=variables,

        )

        if response.get("errors"):

            messages = [

                error.get(
                    "message",
                    "Erro GraphQL"
                )

                for error in response["errors"]

            ]

            raise RuntimeError(

                " | ".join(messages)

            )

        return response.get(
            "data",
            {},
        )