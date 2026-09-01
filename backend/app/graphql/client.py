"""
TrendZone AI OS
================================

Shopee GraphQL Client

Cliente HTTP responsável por executar
requisições GraphQL.
"""

from typing import Any

import requests

from app.core.settings import settings


class GraphQLClient:

    def __init__(self):

        self.endpoint = settings.SHOPEE_GRAPHQL_URL

        self.timeout = 30

    # =====================================================

    def execute(

        self,

        query: str,

        variables: dict | None = None,

        headers: dict | None = None,

    ) -> dict[str, Any]:

        payload = {

            "query": query,

            "variables": variables or {},

        }

        response = requests.post(

            self.endpoint,

            json=payload,

            headers=headers,

            timeout=self.timeout,

        )

        response.raise_for_status()

        return response.json()