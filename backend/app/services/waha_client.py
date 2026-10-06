"""
Cliente HTTP para o WAHA (WhatsApp HTTP API).

WAHA é um servidor self-hosted que expõe o WhatsApp Web via
QR Code como uma API REST simples. Precisa estar rodando
separadamente (container `waha` no docker-compose).

Documentação: https://waha.devlike.pro
"""

import requests

from app.core.settings import settings


class WahaClient:

    def __init__(self):
        self.base_url = settings.WAHA_URL.rstrip("/")
        self.session = "default"
        self.headers = {"Content-Type": "application/json"}
        if settings.WAHA_API_KEY:
            self.headers["X-Api-Key"] = settings.WAHA_API_KEY

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def start_session(self) -> dict:
        try:
            resp = requests.post(
                self._url("/api/sessions/start"),
                json={"name": self.session},
                headers=self.headers,
                timeout=15,
            )
            return {"ok": resp.ok, "status_code": resp.status_code, "data": self._safe_json(resp)}
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    def get_status(self) -> dict:
        try:
            resp = requests.get(
                self._url(f"/api/sessions/{self.session}"),
                headers=self.headers,
                timeout=10,
            )
            return {"ok": resp.ok, "status_code": resp.status_code, "data": self._safe_json(resp)}
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    def get_qr_code(self) -> dict:
        try:
            # Sem "Accept: application/json" o WAHA devolve o PNG puro
            # (binário) em vez do JSON com o base64 — o que quebrava o
            # parsing e deixava o QR Code em branco no frontend.
            resp = requests.get(
                self._url(f"/api/{self.session}/auth/qr"),
                headers={**self.headers, "Accept": "application/json"},
                timeout=10,
            )
            return {"ok": resp.ok, "status_code": resp.status_code, "data": self._safe_json(resp)}
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    def stop_session(self) -> dict:
        try:
            resp = requests.post(
                self._url("/api/sessions/stop"),
                json={"name": self.session},
                headers=self.headers,
                timeout=10,
            )
            return {"ok": resp.ok, "status_code": resp.status_code, "data": self._safe_json(resp)}
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    def send_text(self, phone: str, text: str) -> dict:
        chat_id = phone if "@c.us" in phone else f"{phone}@c.us"
        try:
            resp = requests.post(
                self._url("/api/sendText"),
                json={"session": self.session, "chatId": chat_id, "text": text},
                headers=self.headers,
                timeout=15,
            )
            return {"ok": resp.ok, "status_code": resp.status_code, "data": self._safe_json(resp)}
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def _safe_json(resp) -> dict:
        try:
            return resp.json()
        except ValueError:
            return {"raw": resp.text[:500]}


waha_client = WahaClient()
