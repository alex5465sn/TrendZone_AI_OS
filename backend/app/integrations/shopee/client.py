from typing import Optional

import requests

from app.integrations.shopee.endpoints import BASE_URL


class ShopeeClient:

    def __init__(
        self,
        access_token: Optional[str] = None,
    ):
        self.access_token = access_token

    def get_headers(self):

        headers = {
            "Content-Type": "application/json",
        }

        if self.access_token:

            headers["Authorization"] = (
                f"Bearer {self.access_token}"
            )

        return headers

    def execute(
        self,
        query: str,
        variables: dict | None = None,
    ):

        payload = {
            "query": query,
            "variables": variables or {},
        }

        response = requests.post(
            BASE_URL,
            json=payload,
            headers=self.get_headers(),
            timeout=30,
        )

        response.raise_for_status()

        return response.json()