"""
TrendZone AI OS — Notification Service

Envia notificacoes push para o celular do usuario via ntfy.sh
(servico gratuito, sem necessidade de conta ou token).
Basta o usuario instalar o app ntfy e se inscrever no topico
configurado em NTFY_TOPIC.
"""

import requests

from app.core.logger import logger
from app.core.settings import settings

NTFY_TIMEOUT = 10


def send_push_notification(title: str, message: str, tags: str = "shopping_bags") -> None:
    topic = getattr(settings, "NTFY_TOPIC", "") or ""
    if not topic:
        return

    try:
        requests.post(
            f"https://ntfy.sh/{topic}",
            data=message.encode("utf-8"),
            headers={
                "Title": title.encode("utf-8"),
                "Tags": tags,
            },
            timeout=NTFY_TIMEOUT,
        )
    except Exception as e:
        logger.warning(f"[NOTIFICATION] Falha ao enviar notificacao push: {e}")
