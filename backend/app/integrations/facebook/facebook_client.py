"""
TrendZone AI OS
================================

Cliente para publicação de posts na página do Facebook via Graph API.
"""

import requests

from app.core.settings import settings


GRAPH_API_VERSION = "v19.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

TIMEOUT = 15
VIDEO_TIMEOUT = 180


class FacebookConfigError(Exception):
    pass


class FacebookAPIError(Exception):
    pass


class FacebookClient:

    def __init__(self):
        self.page_id = settings.FACEBOOK_PAGE_ID
        self.page_token = settings.FACEBOOK_PAGE_TOKEN

    def is_configured(self) -> bool:
        return bool(self.page_id and self.page_token)

    def publish_post(self, message: str, link: str | None = None, image_url: str | None = None) -> dict:

        if not self.is_configured():
            raise FacebookConfigError(
                "Integração com Facebook não configurada. Defina FACEBOOK_PAGE_ID e FACEBOOK_PAGE_TOKEN no .env."
            )

        if image_url:
            url = f"{GRAPH_API_BASE}/{self.page_id}/photos"
            payload = {
                "url": image_url,
                "caption": message,
                "access_token": self.page_token,
            }
        else:
            url = f"{GRAPH_API_BASE}/{self.page_id}/feed"
            payload = {
                "message": message,
                "access_token": self.page_token,
            }
            if link:
                payload["link"] = link

        try:
            response = requests.post(url, data=payload, timeout=TIMEOUT)
        except requests.RequestException as exc:
            raise FacebookAPIError(f"Falha ao conectar com o Facebook: {exc}") from exc

        if response.status_code >= 400:
            detail = response.text
            raise FacebookAPIError(f"Facebook recusou a publicação: {detail}")

        return response.json()

    def publish_video(self, file_path: str, description: str = "") -> dict:

        if not self.is_configured():
            raise FacebookConfigError(
                "Integração com Facebook não configurada. Defina FACEBOOK_PAGE_ID e FACEBOOK_PAGE_TOKEN no .env."
            )

        url = f"{GRAPH_API_BASE}/{self.page_id}/videos"

        try:
            with open(file_path, "rb") as video_file:
                files = {"source": video_file}
                data = {
                    "description": description,
                    "access_token": self.page_token,
                }
                response = requests.post(url, data=data, files=files, timeout=VIDEO_TIMEOUT)
        except OSError as exc:
            raise FacebookAPIError(f"Não foi possível ler o arquivo de vídeo: {exc}") from exc
        except requests.RequestException as exc:
            raise FacebookAPIError(f"Falha ao conectar com o Facebook: {exc}") from exc

        if response.status_code >= 400:
            raise FacebookAPIError(f"Facebook recusou a publicação do vídeo: {response.text}")

        return response.json()
