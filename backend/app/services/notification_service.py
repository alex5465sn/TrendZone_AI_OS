"""
TrendZone AI OS

Serviço de Notificações.

Centraliza o envio de notificações via WhatsApp, Push, Email.
Integra com WAHA (WhatsApp), Firebase (Push), etc.
"""

import json
from datetime import datetime
from sqlalchemy.orm import Session
import requests

from app.core.logger import logger
from app.core.settings import settings
from app.models.notification import Notification
from app.models.user import User
from app.services.base_service import BaseService


def send_push_notification(title: str, message: str, tags: str = "info") -> None:
    """
    Notificação push simples e best-effort (usada pelo FacebookSchedulerService
    para avisos rápidos de publicação/erro que não exigem usuário/DB).
    """
    logger.info(f"[PUSH][{tags}] {title}: {message}")


class NotificationService(BaseService):
    """Serviço centralizado de notificações."""

    SERVICE_NAME = "NOTIFICATION_SERVICE"

    @classmethod
    def send_post_published_notification(
        cls,
        db: Session,
        user_id: int,
        product_name: str,
        channel: str,
        post_id: int,
    ) -> bool:
        """
        Envia notificação quando um post é publicado automaticamente.

        Tenta enviar via WhatsApp primeiro, depois Push.
        """

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            cls.log_error(f"Usuário {user_id} não encontrado")
            return False

        title = "📱 Post Publicado!"
        message = f"Seu post sobre '{product_name}' foi publicado em {channel.upper()}"

        # Tenta WhatsApp
        whatsapp_sent = False
        if user.whatsapp_number:
            whatsapp_sent = cls._send_whatsapp(
                user.whatsapp_number,
                title,
                message,
                product_name,
                channel,
            )

        # Registra notificação no banco
        notification = Notification(
            user_id=user_id,
            notification_type="whatsapp" if whatsapp_sent else "push",
            title=title,
            message=message,
            data=json.dumps(
                {
                    "product_name": product_name,
                    "channel": channel,
                    "post_id": post_id,
                }
            ),
            sent=whatsapp_sent,
            sent_at=datetime.utcnow() if whatsapp_sent else None,
            related_entity_type="published_post",
            related_entity_id=post_id,
        )
        db.add(notification)
        db.commit()

        if whatsapp_sent:
            cls.log_success(f"Notificação WhatsApp enviada para {user.whatsapp_number}")
        else:
            cls.log_warning(f"Falha ao enviar WhatsApp para {user_id}")

        return whatsapp_sent

    @classmethod
    def send_first_sale_notification(
        cls,
        db: Session,
        user_id: int,
        product_name: str,
        channel: str,
        commission: float,
    ) -> bool:
        """Envia notificação quando primeira venda é alcançada."""

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        title = "🎉 Primeira Venda!"
        message = f"Parabéns! Você fez sua primeira venda: {product_name} via {channel.upper()} (Comissão: R${commission:.2f})"

        whatsapp_sent = False
        if user.whatsapp_number:
            whatsapp_sent = cls._send_whatsapp(
                user.whatsapp_number,
                title,
                message,
                product_name,
                channel,
            )

        notification = Notification(
            user_id=user_id,
            notification_type="whatsapp" if whatsapp_sent else "push",
            title=title,
            message=message,
            data=json.dumps(
                {
                    "product_name": product_name,
                    "channel": channel,
                    "commission": commission,
                }
            ),
            sent=whatsapp_sent,
            sent_at=datetime.utcnow() if whatsapp_sent else None,
        )
        db.add(notification)
        db.commit()

        return whatsapp_sent

    @classmethod
    def _send_whatsapp(
        cls,
        phone_number: str,
        title: str,
        message: str,
        product_name: str,
        channel: str,
    ) -> bool:
        """Envia mensagem via WAHA (WhatsApp)."""

        try:
            # Formata número (remove caracteres especiais, adiciona código país se necessário)
            phone = phone_number.replace("+", "").replace("-", "").replace(" ", "")
            if not phone.startswith("55"):  # Brasil
                phone = f"55{phone}"

            # Monta mensagem formatada
            formatted_message = f"""
{title}

📦 Produto: {product_name}
📱 Canal: {channel.upper()}
⏰ Horário: {datetime.utcnow().strftime('%H:%M:%S')}

Acompanhe em tempo real em: https://app.trendzone.app/first-sale-plan
            """.strip()

            # Envia via WAHA
            waha_url = settings.WAHA_URL or "http://localhost:3000"
            response = requests.post(
                f"{waha_url}/api/sendText",
                json={
                    "chatId": f"{phone}@c.us",
                    "text": formatted_message,
                },
                timeout=10,
            )

            if response.status_code in [200, 201]:
                cls.log_success(f"WhatsApp enviado para {phone}")
                return True
            else:
                cls.log_error(f"Erro ao enviar WhatsApp: {response.status_code}")
                return False

        except Exception as e:
            cls.log_error(f"Exceção ao enviar WhatsApp: {str(e)}")
            return False

    @classmethod
    def get_user_notifications(
        cls,
        db: Session,
        user_id: int,
        limit: int = 50,
    ) -> list[Notification]:
        """Retorna notificações recentes do usuário."""

        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
            .all()
        )

    @classmethod
    def mark_as_read(cls, db: Session, notification_id: int) -> bool:
        """Marca notificação como lida."""

        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if notification:
            notification.read = True
            notification.read_at = datetime.utcnow()
            db.add(notification)
            db.commit()
            return True
        return False
