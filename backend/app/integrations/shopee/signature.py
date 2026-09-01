"""
TrendZone AI OS
================================

Shopee Affiliate Signature

Responsável por gerar a assinatura SHA256
exigida pela Shopee Affiliate Open API.

A autenticação da Affiliate API NÃO usa OAuth.
Cada requisição é assinada com:

    Authorization: SHA256 Credential={AppId}, Timestamp={Timestamp}, Signature={Signature}

Onde:

    Signature = SHA256(AppId + Timestamp + Payload + Secret)

- AppId     : ID da aplicação.
- Timestamp : Unix timestamp atual em segundos.
- Payload   : Corpo da requisição (JSON string completo).
- Secret    : Chave secreta da aplicação.

O Payload usado na assinatura DEVE ser idêntico
ao corpo enviado na requisição.
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

from app.core.settings import settings


class ShopeeSignature:
    """
    Gera o header Authorization assinado
    para a Shopee Affiliate Open API.
    """

    @staticmethod
    def _payload_string(
        payload: dict[str, Any],
    ) -> str:
        """
        Serializa o payload em JSON string
        sem espaços extras, garantindo que
        a assinatura bata com o corpo enviado.
        """

        return json.dumps(
            payload,
            separators=(",", ":"),
            ensure_ascii=False,
        )

    @classmethod
    def sign(
        cls,
        payload: dict[str, Any],
        timestamp: int | None = None,
    ) -> str:
        """
        Calcula a assinatura SHA256.

        Signature = SHA256(AppId + Timestamp + Payload + Secret)
        """

        app_id = settings.SHOPEE_APP_ID
        secret = settings.SHOPEE_SECRET

        if not app_id or not secret:

            raise ValueError(
                "SHOPEE_APP_ID e SHOPEE_SECRET devem estar configurados."
            )

        if timestamp is None:

            timestamp = int(time.time())

        payload_str = cls._payload_string(payload)

        base_string = (
            f"{app_id}{timestamp}{payload_str}{secret}"
        )

        return hashlib.sha256(
            base_string.encode("utf-8")
        ).hexdigest()

    @classmethod
    def authorization_header(
        cls,
        payload: dict[str, Any],
        timestamp: int | None = None,
    ) -> dict[str, str]:
        """
        Monta o header Authorization completo.

        Authorization: SHA256 Credential={AppId}, Timestamp={Timestamp}, Signature={Signature}
        """

        app_id = settings.SHOPEE_APP_ID

        if not app_id:

            raise ValueError(
                "SHOPEE_APP_ID deve estar configurado."
            )

        if timestamp is None:

            timestamp = int(time.time())

        signature = cls.sign(
            payload,
            timestamp,
        )

        return {
            "Authorization": (
                f"SHA256 Credential={app_id}, "
                f"Timestamp={timestamp}, "
                f"Signature={signature}"
            )
        }
