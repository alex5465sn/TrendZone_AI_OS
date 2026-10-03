"""
TrendZone AI OS
================================

Mercado Livre HTTP Client

Responsável pela comunicação HTTP
com a API oficial do Mercado Livre
(https://api.mercadolibre.com).

Não contém regras de negócio.

Responsabilidades:

- OAuth 2.0 (authorization code + refresh)
- Busca pública de produtos (catálogo)
- Dados de item
- Dados do usuário autorizado (/users/me)

Documentação oficial de autenticação:
- Authorize: https://auth.mercadolivre.com.br/authorization
- Token:     https://api.mercadolibre.com/oauth/token
"""

from __future__ import annotations

import secrets
import hashlib
import base64
from typing import Any
from urllib.parse import urlencode

import requests

from app.core.settings import settings


class MercadoLivreException(Exception):
    """
    Erro de integração com o Mercado Livre.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        error_code: str | None = None,
    ):

        super().__init__(message)

        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class MercadoLivreClient:

    DEFAULT_TIMEOUT = 30

    API_BASE = "https://api.mercadolibre.com"

    AUTH_URL = "https://auth.mercadolivre.com.br/authorization"

    TOKEN_URL = "https://api.mercadolibre.com/oauth/token"

    def __init__(
        self,
        site_id: str | None = None,
    ) -> None:

        self.site_id = (
            site_id
            or settings.MERCADOLIVRE_SITE_ID
            or "MLB"
        )

    # =====================================================
    # OAuth 2.0 — Authorization Code
    # =====================================================

    def build_authorize_url(
        self,
        app_id: str,
        redirect_uri: str,
        state: str,
        code_verifier: str | None = None,
    ) -> str:
        """
        Monta a URL de autorização do Mercado Livre.

        O usuário abre essa URL, faz login com a conta
        PRINCIPAL (administrador, não colaborador) e
        autoriza o aplicativo. O ML redireciona para o
        redirect_uri EXATAMENTE igual ao cadastrado no
        DevCenter, acrescentando ?code=...&state=...
        """

        params = {
            "response_type": "code",
            "client_id": app_id,
            "redirect_uri": redirect_uri,
            "state": state,
        }

        if code_verifier:
            params["code_challenge"] = self.pkce_challenge(
                code_verifier,
            )
            params["code_challenge_method"] = "S256"

        return f"{self.AUTH_URL}?{urlencode(params)}"

    @staticmethod
    def pkce_challenge(
        verifier: str,
    ) -> str:
        """
        Gera o code_challenge S256 a partir do
        code_verifier (PKCE).
        """

        digest = hashlib.sha256(
            verifier.encode("ascii"),
        ).digest()

        return base64.urlsafe_b64encode(
            digest,
        ).rstrip(
            b"=",
        ).decode("ascii")

    @staticmethod
    def generate_code_verifier() -> str:
        """
        Gera um code_verifier aleatório seguro (PKCE).
        """

        return secrets.token_urlsafe(48)

    def exchange_code(
        self,
        app_id: str,
        client_secret: str,
        code: str,
        redirect_uri: str,
        code_verifier: str | None = None,
    ) -> dict[str, Any]:
        """
        Troca o authorization code pelo par
        access_token + refresh_token (válido por 6h).

        Resposta esperada:
        {
            "access_token": "APP_USR-...",
            "token_type": "bearer",
            "expires_in": 21600,
            "scope": "offline_access read write",
            "user_id": 1234567,
            "refresh_token": "TG-..."
        }
        """

        data = {
            "grant_type": "authorization_code",
            "client_id": app_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }

        if code_verifier:
            data["code_verifier"] = code_verifier

        return self._token_request(data)

    def refresh_access_token(
        self,
        app_id: str,
        client_secret: str,
        refresh_token: str,
    ) -> dict[str, Any]:
        """
        Renova o access_token a partir do refresh_token.

        IMPORTANTE: o refresh_token do Mercado Livre é
        de USO ÚNICO — cada renovação devolve um NOVO
        refresh_token que deve ser persistido no lugar
        do anterior.
        """

        data = {
            "grant_type": "refresh_token",
            "client_id": app_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        }

        return self._token_request(data)

    def _token_request(
        self,
        data: dict[str, str],
    ) -> dict[str, Any]:

        try:

            response = requests.post(

                self.TOKEN_URL,

                data=data,

                headers={
                    "accept": "application/json",
                    "content-type": "application/x-www-form-urlencoded",
                },

                timeout=self.DEFAULT_TIMEOUT,

            )

        except requests.RequestException as e:

            raise MercadoLivreException(
                f"Falha de conexão com o Mercado Livre: {e}",
            ) from e

        if response.status_code >= 400:

            raise self._error(
                response,
                "Erro ao obter token do Mercado Livre",
            )

        return response.json()

    # =====================================================
    # API — busca pública (não exige token)
    # =====================================================

    def search_site(
        self,
        q: str,
        offset: int = 0,
        limit: int = 20,
    ) -> dict[str, Any]:
        """
        GET /sites/{site}/search — busca pública
        no catálogo do Mercado Livre.

        Não exige autenticação. Limite máximo por
        página: 50 itens.
        """

        endpoint = f"{self.API_BASE}/sites/{self.site_id}/search"

        try:

            response = requests.get(

                endpoint,

                params={
                    "q": q,
                    "offset": max(0, int(offset)),
                    "limit": min(50, max(1, int(limit))),
                },

                timeout=self.DEFAULT_TIMEOUT,

            )

        except requests.RequestException as e:

            raise MercadoLivreException(
                f"Falha de conexão com o Mercado Livre: {e}",
            ) from e

        if response.status_code >= 400:

            raise self._error(
                response,
                "Erro na busca de produtos do Mercado Livre",
            )

        return response.json()

    def get_item(
        self,
        external_id: str,
    ) -> dict[str, Any]:
        """
        GET /items/{id} — detalhe público do item
        (ex.: MLB1234567890).
        """

        endpoint = f"{self.API_BASE}/items/{external_id}"

        try:

            response = requests.get(

                endpoint,

                timeout=self.DEFAULT_TIMEOUT,

            )

        except requests.RequestException as e:

            raise MercadoLivreException(
                f"Falha de conexão com o Mercado Livre: {e}",
            ) from e

        if response.status_code >= 400:

            raise self._error(
                response,
                "Erro ao consultar item do Mercado Livre",
            )

        return response.json()

    # =====================================================
    # API — recursos privados (exigem access_token)
    # =====================================================

    def get_user_me(
        self,
        access_token: str,
    ) -> dict[str, Any]:
        """
        GET /users/me — valida o token e devolve
        os dados da conta que autorizou o aplicativo.
        """

        try:

            response = requests.get(

                f"{self.API_BASE}/users/me",

                headers={
                    "Authorization": f"Bearer {access_token}",
                    "accept": "application/json",
                },

                timeout=self.DEFAULT_TIMEOUT,

            )

        except requests.RequestException as e:

            raise MercadoLivreException(
                f"Falha de conexão com o Mercado Livre: {e}",
            ) from e

        if response.status_code >= 400:

            raise self._error(
                response,
                "Não foi possível validar o token do Mercado Livre",
            )

        return response.json()

    # =====================================================
    # Errors
    # =====================================================

    @staticmethod
    def _error(
        response: requests.Response,
        fallback: str,
    ) -> MercadoLivreException:

        try:

            body = response.json()

            message = (
                body.get("message")
                or body.get("error_description")
                or body.get("error")
                or fallback
            )

            error_code = body.get("error")

        except Exception:

            message = fallback
            error_code = None

        return MercadoLivreException(
            f"{fallback}: {message}",
            status_code=response.status_code,
            error_code=error_code,
        )
