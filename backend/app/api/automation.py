import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel as Schema
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.automation_rule import AutomationRule
from app.models.funnel import FunnelCard
from app.models.follow_up import FollowUp
from app.models.prospect import Prospect
from app.api.response import ResponseBuilder
from app.api.audit_log import record_audit
from app.models.ai_agent_config import AIAgentConfig
from app.services import ai_agent_service

router = APIRouter(
    prefix="/automation",
    tags=["Automation Rules"],
)

TRIGGER_TYPES = [
    {"id": "card_stale", "name": "Card parado no funil (X dias sem mover)", "config": ["days"]},
    {"id": "follow_up_overdue", "name": "Follow-up atrasado", "config": []},
    {"id": "prospect_cold", "name": "Prospect esfriando (sem contato há X dias)", "config": ["days"]},
]

ACTION_TYPES = [
    {"id": "create_follow_up", "name": "Criar follow-up automático", "config": ["message", "priority"]},
    {"id": "change_prospect_status", "name": "Mudar status do prospect", "config": ["status"]},
    {"id": "change_prospect_temperature", "name": "Mudar temperatura do prospect", "config": ["temperatura"]},
    {"id": "notify", "name": "Registrar notificação no log", "config": ["message"]},
]


class RuleCreate(Schema):
    name: str
    trigger_type: str
    trigger_config: dict = {}
    action_type: str
    action_config: dict = {}
    is_enabled: bool = True


class RuleUpdate(Schema):
    name: Optional[str] = None
    trigger_config: Optional[dict] = None
    action_config: Optional[dict] = None
    is_enabled: Optional[bool] = None


@router.get("/definitions")
def get_definitions(
    current_user: User = Depends(get_current_user),
):
    return ResponseBuilder.success(data={"triggers": TRIGGER_TYPES, "actions": ACTION_TYPES})


@router.get("/rules")
def list_rules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rules = (
        db.query(AutomationRule)
        .filter(AutomationRule.user_id == current_user.id, AutomationRule.is_active == True)
        .order_by(AutomationRule.created_at.desc())
        .all()
    )

    result = [
        {
            "id": r.id,
            "name": r.name,
            "trigger_type": r.trigger_type,
            "trigger_config": json.loads(r.trigger_config or "{}"),
            "action_type": r.action_type,
            "action_config": json.loads(r.action_config or "{}"),
            "is_enabled": r.is_enabled,
            "last_triggered_at": r.last_triggered_at.isoformat() if r.last_triggered_at else None,
            "trigger_count": r.trigger_count,
        }
        for r in rules
    ]

    return ResponseBuilder.success(data=result)


@router.post("/rules")
def create_rule(
    payload: RuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.trigger_type not in [t["id"] for t in TRIGGER_TYPES]:
        raise HTTPException(status_code=400, detail="Tipo de gatilho inválido.")
    if payload.action_type not in [a["id"] for a in ACTION_TYPES]:
        raise HTTPException(status_code=400, detail="Tipo de ação inválido.")

    rule = AutomationRule(
        user_id=current_user.id,
        name=payload.name,
        trigger_type=payload.trigger_type,
        trigger_config=json.dumps(payload.trigger_config, ensure_ascii=False),
        action_type=payload.action_type,
        action_config=json.dumps(payload.action_config, ensure_ascii=False),
        is_enabled=payload.is_enabled,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)

    record_audit(db, current_user.id, "automation_rule", "CREATE", rule.id, f"Regra criada: {rule.name}")

    return ResponseBuilder.success(
        data={"id": rule.id, "name": rule.name},
        message="Regra de automação criada.",
        status_code=201,
    )


@router.patch("/rules/{rule_id}")
def update_rule(
    rule_id: int,
    payload: RuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rule = (
        db.query(AutomationRule)
        .filter(AutomationRule.id == rule_id, AutomationRule.user_id == current_user.id)
        .first()
    )
    if not rule:
        raise HTTPException(status_code=404, detail="Regra não encontrada.")

    if payload.name is not None:
        rule.name = payload.name
    if payload.trigger_config is not None:
        rule.trigger_config = json.dumps(payload.trigger_config, ensure_ascii=False)
    if payload.action_config is not None:
        rule.action_config = json.dumps(payload.action_config, ensure_ascii=False)
    if payload.is_enabled is not None:
        rule.is_enabled = payload.is_enabled

    db.commit()

    return ResponseBuilder.success(message="Regra atualizada.")


@router.delete("/rules/{rule_id}")
def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rule = (
        db.query(AutomationRule)
        .filter(AutomationRule.id == rule_id, AutomationRule.user_id == current_user.id)
        .first()
    )
    if not rule:
        raise HTTPException(status_code=404, detail="Regra não encontrada.")

    rule.is_active = False
    db.commit()

    return ResponseBuilder.success(message="Regra removida.")


def _execute_action(db: Session, rule: AutomationRule, user_id: int, context: dict) -> str:
    action_config = json.loads(rule.action_config or "{}")

    if rule.action_type == "create_follow_up":
        follow_up = FollowUp(
            card_id=context.get("card_id"),
            product_id=context.get("product_id"),
            user_id=user_id,
            message=action_config.get("message", "Follow-up automático gerado por regra."),
            priority=action_config.get("priority", "MEDIUM"),
        )
        db.add(follow_up)
        db.commit()
        return f"Follow-up criado para {context.get('label', 'item')}"

    if rule.action_type == "change_prospect_status" and context.get("prospect"):
        prospect = context["prospect"]
        prospect.status = action_config.get("status", prospect.status)
        db.commit()
        return f"Status do prospect '{prospect.nome}' alterado para {prospect.status}"

    if rule.action_type == "change_prospect_temperature" and context.get("prospect"):
        prospect = context["prospect"]
        prospect.temperatura = action_config.get("temperatura", prospect.temperatura)
        db.commit()
        return f"Temperatura do prospect '{prospect.nome}' alterada para {prospect.temperatura}"

    if rule.action_type == "notify":
        return action_config.get("message", "Notificação registrada.")

    return "Nenhuma ação executada."


@router.post("/run")
def run_automation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rules = (
        db.query(AutomationRule)
        .filter(
            AutomationRule.user_id == current_user.id,
            AutomationRule.is_active == True,
            AutomationRule.is_enabled == True,
        )
        .all()
    )

    executions = []
    now = datetime.utcnow()

    for rule in rules:
        trigger_config = json.loads(rule.trigger_config or "{}")
        matched_contexts = []

        if rule.trigger_type == "card_stale":
            days = int(trigger_config.get("days", 3))
            threshold = now - timedelta(days=days)
            cards = (
                db.query(FunnelCard)
                .filter(
                    FunnelCard.user_id == current_user.id,
                    FunnelCard.is_active == True,
                    FunnelCard.updated_at < threshold,
                )
                .all()
            )
            matched_contexts = [
                {"card_id": c.id, "product_id": c.product_id, "label": c.title}
                for c in cards
            ]

        elif rule.trigger_type == "follow_up_overdue":
            overdue = (
                db.query(FollowUp)
                .filter(
                    FollowUp.user_id == current_user.id,
                    FollowUp.is_active == True,
                    FollowUp.status == "PENDING",
                    FollowUp.due_at < now,
                )
                .all()
            )
            matched_contexts = [{"label": f.message[:50]} for f in overdue]

        elif rule.trigger_type == "prospect_cold":
            days = int(trigger_config.get("days", 7))
            threshold = now - timedelta(days=days)
            prospects = (
                db.query(Prospect)
                .filter(
                    Prospect.is_active == True,
                    Prospect.updated_at < threshold,
                    Prospect.temperatura != "frio",
                )
                .all()
            )
            matched_contexts = [{"prospect": p, "label": p.nome} for p in prospects]

        if matched_contexts:
            for ctx in matched_contexts:
                result_msg = _execute_action(db, rule, current_user.id, ctx)
                executions.append({"rule": rule.name, "result": result_msg})

            rule.last_triggered_at = now
            rule.trigger_count += len(matched_contexts)
            db.commit()

            record_audit(
                db, current_user.id, "automation_rule", "TRIGGER", rule.id,
                f"Regra '{rule.name}' disparada {len(matched_contexts)}x",
            )

    return ResponseBuilder.success(
        data={"executions": executions, "total": len(executions)},
        message=f"{len(executions)} ação(ões) executada(s).",
    )


AI_SYSTEM_PROMPT = (
    "Você é o motor de automação do TrendZone. Analise a situação atual do funil de vendas, "
    "follow-ups e prospects abaixo, e decida quais ações tomar agora. "
    "Responda APENAS com um JSON (array), sem texto fora do JSON, no formato: "
    '[{"action": "create_follow_up", "card_id": 12, "message": "...", "priority": "HIGH|MEDIUM|LOW"}, '
    '{"action": "change_prospect_status", "prospect_id": 5, "status": "contatado"}, '
    '{"action": "change_prospect_temperature", "prospect_id": 5, "temperatura": "quente"}, '
    '{"action": "notify", "message": "..."}]. '
    "Se nada precisar ser feito, responda com uma lista vazia []. "
    "Não invente IDs que não estejam na lista fornecida."
)


def _ai_execute(db: Session, user_id: int, decision: dict) -> str:
    action = decision.get("action")

    if action == "create_follow_up":
        follow_up = FollowUp(
            card_id=decision.get("card_id"),
            product_id=decision.get("product_id"),
            user_id=user_id,
            message=decision.get("message", "Follow-up sugerido pela IA."),
            priority=decision.get("priority", "MEDIUM"),
        )
        db.add(follow_up)
        db.commit()
        return f"Follow-up criado (card {decision.get('card_id')})"

    if action == "change_prospect_status":
        prospect = db.query(Prospect).filter(Prospect.id == decision.get("prospect_id")).first()
        if prospect:
            prospect.status = decision.get("status", prospect.status)
            db.commit()
            return f"Status do prospect '{prospect.nome}' alterado para {prospect.status}"
        return "Prospect não encontrado para alteração de status."

    if action == "change_prospect_temperature":
        prospect = db.query(Prospect).filter(Prospect.id == decision.get("prospect_id")).first()
        if prospect:
            prospect.temperatura = decision.get("temperatura", prospect.temperatura)
            db.commit()
            return f"Temperatura do prospect '{prospect.nome}' alterada para {prospect.temperatura}"
        return "Prospect não encontrado para alteração de temperatura."

    if action == "notify":
        return decision.get("message", "Notificação registrada.")

    return f"Ação desconhecida ignorada: {action}"


@router.post("/ai-run")
def ai_run_automation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    config = db.query(AIAgentConfig).filter(AIAgentConfig.user_id == current_user.id).first()
    if not config:
        config = AIAgentConfig(user_id=current_user.id)
        db.add(config)
        db.commit()
        db.refresh(config)

    if not ai_agent_service.is_provider_configured(config.provider):
        return ResponseBuilder.error(
            message=f"Provedor de IA '{config.provider}' sem chave de API configurada. Configure em Agente de IA."
        )

    now = datetime.utcnow()
    stale_threshold = now - timedelta(days=3)

    stale_cards = (
        db.query(FunnelCard)
        .filter(
            FunnelCard.user_id == current_user.id,
            FunnelCard.is_active == True,
            FunnelCard.updated_at < stale_threshold,
        )
        .limit(20)
        .all()
    )

    overdue_follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.user_id == current_user.id,
            FollowUp.is_active == True,
            FollowUp.status == "PENDING",
            FollowUp.due_at < now,
        )
        .limit(20)
        .all()
    )

    cold_prospects = (
        db.query(Prospect)
        .filter(
            Prospect.is_active == True,
            Prospect.updated_at < now - timedelta(days=7),
            Prospect.temperatura != "frio",
        )
        .limit(20)
        .all()
    )

    context_summary = {
        "cards_parados": [
            {"card_id": c.id, "titulo": c.title, "dias_parado": (now - c.updated_at).days}
            for c in stale_cards
        ],
        "follow_ups_atrasados": [
            {"follow_up_id": f.id, "card_id": f.card_id, "mensagem": f.message[:80]}
            for f in overdue_follow_ups
        ],
        "prospects_esfriando": [
            {"prospect_id": p.id, "nome": p.nome, "temperatura_atual": p.temperatura}
            for p in cold_prospects
        ],
    }

    if not any(context_summary.values()):
        return ResponseBuilder.success(
            data={"executions": [], "total": 0},
            message="Nada pendente no momento. A IA não encontrou ações necessárias.",
        )

    result = ai_agent_service.generate_reply(
        provider=config.provider,
        model_name=config.model_name,
        system_prompt=AI_SYSTEM_PROMPT,
        user_message=json.dumps(context_summary, ensure_ascii=False),
        history=[],
    )

    if not result.get("ok"):
        return ResponseBuilder.error(message=result.get("error", "Falha ao consultar a IA."))

    raw_reply = result.get("reply", "").strip()
    try:
        start = raw_reply.index("[")
        end = raw_reply.rindex("]") + 1
        decisions = json.loads(raw_reply[start:end])
    except (ValueError, json.JSONDecodeError):
        return ResponseBuilder.error(message="A IA não retornou uma decisão em formato válido. Tente novamente.")

    executions = []
    for decision in decisions:
        if not isinstance(decision, dict):
            continue
        msg = _ai_execute(db, current_user.id, decision)
        executions.append({"action": decision.get("action"), "result": msg})

    if executions:
        record_audit(
            db, current_user.id, "automation_ai", "RUN", None,
            f"Agente de IA executou {len(executions)} ação(ões) automaticamente",
        )

    return ResponseBuilder.success(
        data={"executions": executions, "total": len(executions)},
        message=f"Agente de IA analisou o cenário e executou {len(executions)} ação(ões).",
    )
