"""
TrendZone AI OS

API para Plano de Primeira Venda.

Endpoints para gerenciar o checklist, rastrear progresso,
e obter recomendações automáticas baseadas em dados reais.
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.first_sale_plan import FirstSalePlan
from app.models.published_post import PublishedPost
from app.models.channel_tracking import ChannelTracking
from app.repositories.first_sale_plan_repository import FirstSalePlanRepository
from app.api.response import ResponseBuilder

router = APIRouter(prefix="/first-sale-plan", tags=["Plano de Primeira Venda"])


class FirstSalePlanUpdate(BaseModel):
    selected_niche: str | None = None
    selected_niche_keywords: str | None = None
    niche_validated: bool | None = None
    champion_products_identified: int | None = None
    whatsapp_groups_count: int | None = None
    facebook_groups_count: int | None = None
    groups_registered: bool | None = None
    current_phase: str | None = None
    notes: str | None = None


@router.get("")
def get_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtém o plano de primeira venda do usuário."""
    plan = FirstSalePlanRepository.get_or_create(db, current_user.id)

    # Calcula métricas em tempo real
    posts = db.query(PublishedPost).filter(
        PublishedPost.user_id == current_user.id
    ).all()
    total_posts = len(posts)
    total_clicks = sum(p.click_count or 0 for p in posts)

    trackings = db.query(ChannelTracking).filter(
        ChannelTracking.user_id == current_user.id
    ).all()
    total_conversions = sum(t.conversions or 0 for t in trackings)
    total_revenue = sum(t.revenue or 0.0 for t in trackings)

    # Atualiza métricas
    plan = FirstSalePlanRepository.update_metrics(
        db, plan, total_clicks, total_conversions, total_posts
    )

    return ResponseBuilder.success(
        data={
            "id": plan.id,
            "selected_niche": plan.selected_niche,
            "current_phase": plan.current_phase,
            "checklist": {
                "niche_validated": plan.niche_validated,
                "champion_products_identified": plan.champion_products_identified,
                "whatsapp_groups_count": plan.whatsapp_groups_count,
                "facebook_groups_count": plan.facebook_groups_count,
                "groups_registered": plan.groups_registered,
            },
            "metrics": {
                "posts_published": plan.posts_published,
                "total_clicks": plan.total_clicks,
                "total_conversions": plan.total_conversions,
                "conversion_rate": plan.conversion_rate,
                "estimated_commission": total_revenue,
                "first_sale_achieved": plan.first_sale_achieved,
                "first_sale_date": plan.first_sale_date.isoformat() if plan.first_sale_date else None,
            },
            "recommendations": _get_recommendations(plan, total_clicks, total_conversions),
            "notes": plan.notes,
        }
    )


@router.put("")
def update_plan(
    payload: FirstSalePlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Atualiza o plano de primeira venda."""
    plan = FirstSalePlanRepository.get_or_create(db, current_user.id)

    if payload.selected_niche is not None:
        plan.selected_niche = payload.selected_niche
    if payload.selected_niche_keywords is not None:
        plan.selected_niche_keywords = payload.selected_niche_keywords
    if payload.niche_validated is not None:
        plan.niche_validated = payload.niche_validated
    if payload.champion_products_identified is not None:
        plan.champion_products_identified = payload.champion_products_identified
    if payload.whatsapp_groups_count is not None:
        plan.whatsapp_groups_count = payload.whatsapp_groups_count
    if payload.facebook_groups_count is not None:
        plan.facebook_groups_count = payload.facebook_groups_count
    if payload.groups_registered is not None:
        plan.groups_registered = payload.groups_registered
    if payload.current_phase is not None:
        plan.current_phase = payload.current_phase
        plan.phase_started_at = datetime.utcnow()
    if payload.notes is not None:
        plan.notes = payload.notes

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return ResponseBuilder.success(
        data={"id": plan.id, "current_phase": plan.current_phase},
        message="Plano atualizado com sucesso.",
    )


@router.post("/mark-first-sale")
def mark_first_sale(
    product_name: str,
    channel: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Marca a primeira venda alcançada."""
    plan = FirstSalePlanRepository.get_or_create(db, current_user.id)

    plan.first_sale_achieved = True
    plan.first_sale_date = datetime.utcnow()
    plan.first_sale_product = product_name
    plan.first_sale_channel = channel
    plan.current_phase = "optimization"

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return ResponseBuilder.success(
        data={"first_sale_achieved": True, "date": plan.first_sale_date.isoformat()},
        message="🎉 Primeira venda registrada! Parabéns!",
    )


def _get_recommendations(plan: FirstSalePlan, total_clicks: int, total_conversions: int) -> list:
    """Gera recomendações automáticas baseadas no progresso."""
    recommendations = []

    if plan.current_phase == "preparation":
        if not plan.niche_validated:
            recommendations.append(
                {
                    "priority": "high",
                    "message": "Valide o nicho escolhido no Scout (procure por produtos com score ≥70).",
                }
            )
        if plan.champion_products_identified < 5:
            recommendations.append(
                {
                    "priority": "high",
                    "message": f"Identifique pelo menos 5 produtos campeões (você tem {plan.champion_products_identified}).",
                }
            )
        if plan.whatsapp_groups_count + plan.facebook_groups_count < 6:
            recommendations.append(
                {
                    "priority": "high",
                    "message": f"Cadastre pelo menos 6 grupos (você tem {plan.whatsapp_groups_count + plan.facebook_groups_count}).",
                }
            )

    elif plan.current_phase == "execution":
        if total_clicks < 10:
            recommendations.append(
                {
                    "priority": "high",
                    "message": f"Aumente frequência de posts (você tem {total_clicks} cliques). Meta: 50+ cliques/semana.",
                }
            )
        if total_clicks > 0 and total_conversions == 0:
            recommendations.append(
                {
                    "priority": "medium",
                    "message": "Nenhuma conversão ainda. Teste diferentes horários e produtos.",
                }
            )
        if total_clicks > 20 and total_conversions > 0:
            recommendations.append(
                {
                    "priority": "low",
                    "message": "🎯 Você está no caminho certo! Continue com a frequência atual.",
                }
            )

    elif plan.current_phase == "optimization":
        recommendations.append(
            {
                "priority": "low",
                "message": "Primeira venda alcançada! Agora duplique o que funciona.",
            }
        )

    return recommendations
