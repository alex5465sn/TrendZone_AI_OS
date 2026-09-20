from fastapi import APIRouter, Depends
from pydantic import BaseModel as Schema
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.ai_agent_config import AIAgentConfig
from app.api.response import ResponseBuilder
from app.services import ai_agent_service

router = APIRouter(
    prefix="/ai-agent",
    tags=["AI Agent"],
)

PROVIDERS = ["openrouter", "openai", "anthropic"]


class AIAgentConfigUpdate(Schema):
    is_enabled: bool = False
    auto_reply_whatsapp: bool = False
    provider: str = "openrouter"
    model_name: str = "openai/gpt-4o-mini"
    system_prompt: str = "Você é um assistente de vendas do TrendZone. Responda de forma curta, simpática e objetiva, ajudando o cliente a decidir a compra do produto anunciado."


class AIAgentTestRequest(Schema):
    message: str


def _serialize(config: AIAgentConfig) -> dict:
    return {
        "is_enabled": config.is_enabled,
        "auto_reply_whatsapp": config.auto_reply_whatsapp,
        "provider": config.provider,
        "model_name": config.model_name,
        "system_prompt": config.system_prompt,
        "provider_configured": ai_agent_service.is_provider_configured(config.provider),
        "providers_disponiveis": PROVIDERS,
    }


@router.get("/config")
def get_config(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    config = db.query(AIAgentConfig).filter(AIAgentConfig.user_id == current_user.id).first()

    if not config:
        config = AIAgentConfig(user_id=current_user.id)
        db.add(config)
        db.commit()
        db.refresh(config)

    return ResponseBuilder.success(data=_serialize(config))


@router.put("/config")
def update_config(
    payload: AIAgentConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    config = db.query(AIAgentConfig).filter(AIAgentConfig.user_id == current_user.id).first()

    if not config:
        config = AIAgentConfig(user_id=current_user.id)
        db.add(config)

    config.is_enabled = payload.is_enabled
    config.auto_reply_whatsapp = payload.auto_reply_whatsapp
    config.provider = payload.provider
    config.model_name = payload.model_name
    config.system_prompt = payload.system_prompt

    db.commit()
    db.refresh(config)

    return ResponseBuilder.success(message="Configuração do agente de IA atualizada.", data=_serialize(config))


@router.post("/test")
def test_agent(
    payload: AIAgentTestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    config = db.query(AIAgentConfig).filter(AIAgentConfig.user_id == current_user.id).first()

    if not config:
        config = AIAgentConfig(user_id=current_user.id)
        db.add(config)
        db.commit()
        db.refresh(config)

    result = ai_agent_service.generate_reply(
        provider=config.provider,
        model_name=config.model_name,
        system_prompt=config.system_prompt,
        user_message=payload.message,
        history=[],
    )

    if not result.get("ok"):
        return ResponseBuilder.error(message=result.get("error", "Falha ao gerar resposta."))

    return ResponseBuilder.success(data={"reply": result["reply"]})
