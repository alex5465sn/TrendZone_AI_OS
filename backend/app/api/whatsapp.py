from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel as Schema
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.whatsapp import WhatsAppConnection, WhatsAppMessage
from app.models.funnel import FunnelStage, FunnelCard
from app.models.ai_agent_config import AIAgentConfig
from app.api.response import ResponseBuilder
from app.api.audit_log import record_audit
from app.services.waha_client import waha_client
from app.services import ai_agent_service

router = APIRouter(
    prefix="/whatsapp",
    tags=["WhatsApp"],
)


class SendMessageRequest(Schema):
    phone: str
    text: str


def _get_or_create_connection(db: Session, user_id: int) -> WhatsAppConnection:
    conn = db.query(WhatsAppConnection).filter(WhatsAppConnection.user_id == user_id).first()
    if not conn:
        conn = WhatsAppConnection(user_id=user_id)
        db.add(conn)
        db.commit()
        db.refresh(conn)
    return conn


@router.post("/session/start")
def start_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conn = _get_or_create_connection(db, current_user.id)
    result = waha_client.start_session()

    if not result.get("ok"):
        conn.status = "error"
        conn.last_error = result.get("error", "Falha ao iniciar sessão no servidor WAHA.")
        db.commit()
        return ResponseBuilder.error(
            message="Não foi possível conectar ao servidor WAHA. Verifique se ele está rodando (docker-compose).",
            errors={"detail": conn.last_error},
        )

    conn.status = "starting"
    conn.last_error = ""
    db.commit()

    return ResponseBuilder.success(message="Sessão iniciada. Busque o QR Code em seguida.")


@router.get("/session/qr")
def get_qr(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conn = _get_or_create_connection(db, current_user.id)
    result = waha_client.get_qr_code()

    if not result.get("ok"):
        return ResponseBuilder.error(
            message="QR Code indisponível. O servidor WAHA pode não estar rodando ou a sessão já está conectada.",
            errors={"detail": result.get("error", "")},
        )

    qr_data = result.get("data", {})
    qr_base64 = qr_data.get("qr") or qr_data.get("data") or ""
    conn.qr_code_base64 = qr_base64
    db.commit()

    return ResponseBuilder.success(data={"qr_code_base64": qr_base64})


@router.get("/session/status")
def get_session_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conn = _get_or_create_connection(db, current_user.id)
    result = waha_client.get_status()

    if result.get("ok"):
        remote_status = (result.get("data") or {}).get("status", conn.status)
        conn.status = remote_status
        db.commit()

    return ResponseBuilder.success(
        data={
            "status": conn.status,
            "phone_number": conn.phone_number,
            "last_error": conn.last_error,
            "waha_reachable": result.get("ok", False),
        }
    )


@router.post("/session/stop")
def stop_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conn = _get_or_create_connection(db, current_user.id)
    waha_client.stop_session()
    conn.status = "disconnected"
    db.commit()

    return ResponseBuilder.success(message="Sessão encerrada.")


@router.get("/messages")
def list_messages(
    phone: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(WhatsAppMessage).filter(WhatsAppMessage.user_id == current_user.id)
    if phone:
        query = query.filter(WhatsAppMessage.contact_phone == phone)

    messages = query.order_by(WhatsAppMessage.created_at.asc()).limit(500).all()

    return ResponseBuilder.success(
        data=[
            {
                "id": m.id,
                "contact_phone": m.contact_phone,
                "contact_name": m.contact_name,
                "direction": m.direction,
                "body": m.body,
                "is_from_agent": m.is_from_agent,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in messages
        ]
    )


@router.get("/conversations")
def list_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    messages = (
        db.query(WhatsAppMessage)
        .filter(WhatsAppMessage.user_id == current_user.id)
        .order_by(WhatsAppMessage.created_at.desc())
        .all()
    )

    seen = {}
    for m in messages:
        if m.contact_phone not in seen:
            seen[m.contact_phone] = {
                "contact_phone": m.contact_phone,
                "contact_name": m.contact_name,
                "last_message": m.body,
                "last_at": m.created_at.isoformat() if m.created_at else None,
            }

    return ResponseBuilder.success(data=list(seen.values()))


@router.post("/send")
def send_message(
    payload: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = waha_client.send_text(payload.phone, payload.text)
    if not result.get("ok"):
        return ResponseBuilder.error(
            message="Falha ao enviar mensagem via WAHA.",
            errors={"detail": result.get("error", "")},
        )

    msg = WhatsAppMessage(
        user_id=current_user.id,
        contact_phone=payload.phone,
        direction="out",
        body=payload.text,
        is_from_agent=False,
    )
    db.add(msg)
    db.commit()

    return ResponseBuilder.success(message="Mensagem enviada.")


@router.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Recebe eventos do WAHA (mensagens inbound). Rota pública pois o
    WAHA (servidor local/rede interna) não envia token de usuário —
    a segurança real vem de o webhook só ser alcançável pela rede
    interna do docker-compose.
    """
    payload = await request.json()

    event = payload.get("event", "")
    if event != "message":
        return ResponseBuilder.success(message="Evento ignorado.")

    data = payload.get("payload", {})
    from_number = (data.get("from") or "").replace("@c.us", "")
    body = data.get("body", "")
    contact_name = data.get("_data", {}).get("notifyName", "") if isinstance(data.get("_data"), dict) else ""

    if not from_number or not body:
        return ResponseBuilder.success(message="Payload sem remetente/texto.")

    admin_user = db.query(User).order_by(User.id.asc()).first()
    if not admin_user:
        return ResponseBuilder.error(message="Nenhum usuário cadastrado para receber a mensagem.")

    stage = (
        db.query(FunnelStage)
        .filter(FunnelStage.user_id == admin_user.id, FunnelStage.is_active == True)
        .order_by(FunnelStage.position.asc())
        .first()
    )

    card = None
    if stage:
        card = (
            db.query(FunnelCard)
            .filter(
                FunnelCard.user_id == admin_user.id,
                FunnelCard.channel == "whatsapp",
                FunnelCard.notes.like(f"%{from_number}%"),
                FunnelCard.is_active == True,
            )
            .first()
        )
        if not card:
            card = FunnelCard(
                stage_id=stage.id,
                user_id=admin_user.id,
                title=contact_name or from_number,
                description="Contato originado via WhatsApp.",
                channel="whatsapp",
                notes=f"phone:{from_number}",
            )
            db.add(card)
            db.commit()
            db.refresh(card)
            record_audit(
                db, admin_user.id, "funnel_card", "CREATE", card.id,
                f"Novo card criado automaticamente via WhatsApp ({from_number})",
            )

    inbound = WhatsAppMessage(
        user_id=admin_user.id,
        funnel_card_id=card.id if card else None,
        contact_phone=from_number,
        contact_name=contact_name,
        direction="in",
        body=body,
        is_from_agent=False,
    )
    db.add(inbound)
    db.commit()

    agent_config = (
        db.query(AIAgentConfig)
        .filter(AIAgentConfig.user_id == admin_user.id)
        .first()
    )

    if agent_config and agent_config.is_enabled and agent_config.auto_reply_whatsapp:
        history_rows = (
            db.query(WhatsAppMessage)
            .filter(
                WhatsAppMessage.user_id == admin_user.id,
                WhatsAppMessage.contact_phone == from_number,
            )
            .order_by(WhatsAppMessage.created_at.asc())
            .limit(10)
            .all()
        )
        history = [
            {"role": "assistant" if h.direction == "out" else "user", "content": h.body}
            for h in history_rows
        ]

        ai_result = ai_agent_service.generate_reply(
            provider=agent_config.provider,
            model_name=agent_config.model_name,
            system_prompt=agent_config.system_prompt,
            user_message=body,
            history=history,
        )

        if ai_result.get("ok"):
            reply_text = ai_result["reply"]
            send_result = waha_client.send_text(from_number, reply_text)
            if send_result.get("ok"):
                outbound = WhatsAppMessage(
                    user_id=admin_user.id,
                    funnel_card_id=card.id if card else None,
                    contact_phone=from_number,
                    direction="out",
                    body=reply_text,
                    is_from_agent=True,
                )
                db.add(outbound)
                db.commit()

    return ResponseBuilder.success(message="Mensagem processada.")
