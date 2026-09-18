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
