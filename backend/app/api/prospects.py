"""
TrendZone AI OS — Prospects API

Prospecção de nichos de oportunidade.
Inspirado na Máquina de Leads: descobre os melhores
nichos de produto com score + temperatura + dossiê.
"""

import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.prospect import Prospect
from app.models.schedule import Schedule
from app.repositories.product_repository import ProductRepository
from app.repositories.prospect_repository import ProspectRepository
from app.repositories.schedule_repository import ScheduleRepository
from app.services.prospect_engine import ProspectEngine
from app.api.response import ResponseBuilder

router = APIRouter(prefix="/prospects", tags=["Prospects"])


def _product_to_dict(p) -> dict:
    return {
        "id": p.id, "item_id": p.item_id, "name": p.name,
        "image": p.image, "offer_link": p.offer_link,
        "price": float(p.price), "commission": float(p.commission),
        "rating": p.rating, "sales": p.sales,
        "score": p.score, "confidence": p.confidence,
        "recommendation": p.recommendation,
    }


def _prospect_dict(p) -> dict:
    return {
        "id": p.id, "uuid": p.uuid, "nicho": p.nicho,
        "cidade": p.cidade, "busca": p.busca, "nome": p.nome,
        "score": p.score, "temperatura": p.temperatura,
        "abordagem": p.abordagem,
        "dossie": json.loads(p.dossie) if p.dossie else {},
        "canal_sugerido": p.canal_sugerido,
        "status": p.status, "produto_ids": p.produto_ids,
        "qtd_produtos": p.qtd_produtos,
        "preco_medio": p.preco_medio,
        "comissao_media": p.comissao_media,
        "vendas_total": p.vendas_total,
        "created_at": p.created_at.isoformat() if p.created_at else "",
    }


@router.get("/scan")
def scan_prospects(
    nicho: str = Query("", description="Filtrar por nicho"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    products = ProductRepository.get_all(db)
    products_dict = [_product_to_dict(p) for p in products]

    results = ProspectEngine.prospect(products_dict, nicho=nicho)

    for r in results:
        prospect = Prospect(
            nicho=r["nicho"], cidade=r["cidade"], busca=r["busca"],
            nome=r["nome"], score=r["score"], temperatura=r["temperatura"],
            abordagem=r["abordagem"], dossie=r["dossie"],
            canal_sugerido=r["canal_sugerido"], status=r["status"],
            produto_ids=r["produto_ids"], qtd_produtos=r["qtd_produtos"],
            preco_medio=r["preco_medio"], comissao_media=r["comissao_media"],
            vendas_total=r["vendas_total"],
        )
        ProspectRepository.create(db, prospect)

    return ResponseBuilder.success(data=results)


@router.get("")
def list_prospects(
    temperatura: str = Query("", description="quente, morno ou frio"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if temperatura:
        prospects = ProspectRepository.get_by_temperatura(db, temperatura)
    else:
        prospects = ProspectRepository.get_all(db)

    prospects.sort(key=lambda p: p.score, reverse=True)

    return ResponseBuilder.success(
        data=[_prospect_dict(p) for p in prospects],
    )


@router.patch("/{prospect_id}/status")
def update_prospect_status(
    prospect_id: int,
    status: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prospect = ProspectRepository.get_by_id(db, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect não encontrado.")
    prospect.status = status
    prospect.updated_at = datetime.utcnow()
    ProspectRepository.update(db, prospect)
    return ResponseBuilder.success(
        data={"id": prospect.id, "status": prospect.status},
        message="Status atualizado.",
    )


@router.delete("/{prospect_id}")
def delete_prospect(
    prospect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prospect = ProspectRepository.get_by_id(db, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect não encontrado.")
    ProspectRepository.soft_delete(db, prospect)
    return ResponseBuilder.success(message="Prospect removido.")


class ScheduleCreate(BaseModel):
    nicho: str
    cidade: str = ""
    hora: str = "09:00"
    dias: str = "todos"
    quantos: int = 5


@router.post("/schedules")
def create_schedule(
    payload: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    schedule = Schedule(
        nicho=payload.nicho, cidade=payload.cidade,
        hora=payload.hora, dias=payload.dias,
        quantos=payload.quantos, status="ativo",
    )
    schedule = ScheduleRepository.create(db, schedule)
    return ResponseBuilder.success(
        data={"id": schedule.id, "status": schedule.status},
        message="Agendamento criado.",
    )


@router.get("/schedules")
def list_schedules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    schedules = ScheduleRepository.get_active(db)
    return ResponseBuilder.success(
        data=[
            {
                "id": s.id, "nicho": s.nicho, "cidade": s.cidade,
                "hora": s.hora, "dias": s.dias, "quantos": s.quantos,
                "ultimo_run": s.ultimo_run, "status": s.status,
                "created_at": s.created_at.isoformat() if s.created_at else "",
            }
            for s in schedules
        ],
    )


@router.delete("/schedules/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    schedule = ScheduleRepository.get_by_id(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    ScheduleRepository.soft_delete(db, schedule)
    return ResponseBuilder.success(message="Agendamento removido.")
