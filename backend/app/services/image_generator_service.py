"""
TrendZone AI OS — Gerador de imagem de capa com IA

Gera uma imagem de capa "viral" para o produto usando a API de
imagens da OpenAI, a partir do nome do produto, em vez de usar a
foto crua da Shopee. Se a geração falhar por qualquer motivo (sem
chave configurada, erro de rede, cota excedida etc.), retorna None
— quem chamar esta função deve cair de volta pra foto original do
produto. Nunca deve derrubar o fluxo de agendamento automático.
"""

import base64
import uuid
from pathlib import Path

import requests

from app.core.logger import logger
from app.core.settings import settings

MEDIA_DIR = Path(__file__).resolve().parents[2] / "media" / "covers"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

OPENAI_IMAGES_URL = "https://api.openai.com/v1/images/generations"
TIMEOUT = 60


def generate_cover_image(product_name: str) -> str | None:
    """
    Gera uma imagem de capa para divulgação do produto e salva em
    backend/media/covers, retornando a URL pública (servida em
    /media/covers/...). Retorna None se a geração não estiver
    disponível ou falhar por qualquer motivo.
    """
    if not settings.OPENAI_API_KEY:
        return None

    prompt = (
        f"Capa publicitária de e-commerce para redes sociais, chamativa e "
        f"vibrante, anunciando o produto '{product_name}'. Sem texto, sem "
        f"logotipos, fundo limpo, iluminação de estúdio, foco no produto, "
        f"estilo comercial moderno e profissional."
    )

    try:
        response = requests.post(
            OPENAI_IMAGES_URL,
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-image-1",
                "prompt": prompt,
                "size": "1024x1024",
                "n": 1,
            },
            timeout=TIMEOUT,
        )
        if not response.ok:
            logger.warning(
                f"[IMAGE_GENERATOR] OpenAI retornou {response.status_code}: {response.text[:300]}"
            )
            return None

        item = response.json()["data"][0]

        image_bytes = None
        if item.get("b64_json"):
            image_bytes = base64.b64decode(item["b64_json"])
        elif item.get("url"):
            img_resp = requests.get(item["url"], timeout=TIMEOUT)
            img_resp.raise_for_status()
            image_bytes = img_resp.content

        if not image_bytes:
            return None

        filename = f"{uuid.uuid4().hex}.png"
        (MEDIA_DIR / filename).write_bytes(image_bytes)

        base_url = settings.APP_BASE_URL.rstrip("/")
        return f"{base_url}/media/covers/{filename}"

    except Exception as exc:
        logger.warning(f"[IMAGE_GENERATOR] Falha ao gerar imagem de capa: {exc}")
        return None
