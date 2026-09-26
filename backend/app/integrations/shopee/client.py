"""
TrendZone AI OS
================================

Shopee HTTP Client

Responsável pela comunicação HTTP
com a Shopee Affiliate API.

Não contém regras de negócio.

Responsabilidades:

- REST
- GraphQL
- Headers
- HTTP
"""

from __future__ import annotations

import json
from typing import Any

import requests

from app.core.settings import settings
from app.integrations.shopee.signature import ShopeeSignature
from app.integrations.shopee.rate_limiter import RateLimiter


class ShopeeClient:

    DEFAULT_TIMEOUT = 60

    # Compartilhado entre todas as instancias do processo: o limite
    # e da API da Shopee como um todo, nao por instancia de client.
    _rate_limiter = RateLimiter()

    def __init__(
        self,
        access_token: str | None = None,
        app_id: str | None = None,
        secret: str | None = None,
    ):

        self.access_token = access_token
        self.app_id = app_id
        self.secret = secret

    # =====================================================
    # HEADERS
    # =====================================================

    def get_headers(
        self,
        payload: dict[str, Any],
    ) -> dict[str, str]:

        headers = {
            "Content-Type": "application/json",
        }

        headers.update(
            ShopeeSignature.authorization_header(
                payload,
                app_id=self.app_id,
                secret=self.secret,
            )
        )

        return headers

    # =====================================================
    # REST GET
    # =====================================================

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ) -> dict[str, Any]:

        payload = params or {}

        self._rate_limiter.acquire()

        response = requests.get(

            endpoint,

            headers=self.get_headers(payload),

            params=params,

            timeout=self.DEFAULT_TIMEOUT,

        )

        response.raise_for_status()

        return response.json()

    # =====================================================
    # REST POST
    # =====================================================

    def post(
        self,
        endpoint: str,
        payload: dict | None = None,
    ) -> dict[str, Any]:

        body = payload or {}

        self._rate_limiter.acquire()

        response = requests.post(

            endpoint,

            headers=self.get_headers(body),

            data=json.dumps(
                body,
                separators=(",", ":"),
                ensure_ascii=False,
            ),

            timeout=self.DEFAULT_TIMEOUT,

        )

        response.raise_for_status()

        return response.json()

    # =====================================================
    # GRAPHQL
    # =====================================================

    def execute(
        self,
        *,
        query: str,
        variables: dict | None = None,
    ) -> dict[str, Any]:

        payload = {

            "query": query,

            "variables": variables or {},

        }

        body = json.dumps(
            payload,
            separators=(",", ":"),
            ensure_ascii=False,
        )

        self._rate_limiter.acquire()

        response = requests.post(

            settings.SHOPEE_GRAPHQL_URL,

            headers=self.get_headers(payload),

            data=body,

            timeout=self.DEFAULT_TIMEOUT,

        )

        response.raise_for_status()

        return response.json()
