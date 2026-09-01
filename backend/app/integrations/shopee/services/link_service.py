"""
TrendZone AI OS
================================

Shopee Link Service.

Responsável pelas operações relacionadas
à geração de links de afiliado.
"""

from __future__ import annotations

from app.integrations.shopee.graphql.repository import (
    GraphQLRepository,
)


class LinkService:

    def __init__(
        self,
        access_token: str | None = None,
    ) -> None:

        self.repository = GraphQLRepository(
            access_token=access_token,
        )

    def generate_short_link(
        self,
        original_url: str,
    ):

        variables = {
            "originalUrl": original_url,
        }

        return self.repository.generate_short_link(
            variables
        )

    def generate_batch_short_link(
        self,
        urls: list[str],
    ):

        variables = {
            "urls": urls,
        }

        return self.repository.generate_batch_short_link(
            variables
        )
