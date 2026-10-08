from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel as Schema
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.seasonal_event import SeasonalEvent
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/seasonal",
    tags=["Seasonal Planner"],
)

PRESET_EVENTS = [
    {"name": "Ano Novo", "month": 1, "day": 1, "category": "comemorativa", "niches": "decoração, eletrônicos, fitness, organização"},
    {"name": "Carnaval", "month": 2, "day": 20, "category": "sazonal", "niches": "fantasia, maquiagem, acessórios, bebidas"},
    {"name": "Dia da Mulher", "month": 3, "day": 8, "category": "comemorativa", "niches": "beleza, moda, joias, perfumes"},
    {"name": "Páscoa", "month": 4, "day": 10, "category": "comemorativa", "niches": "chocolates, decoração, presentes"},
    {"name": "Dia das Mães", "month": 5, "day": 11, "category": "comemorativa", "niches": "beleza, joias, eletrodomésticos, roupas"},
    {"name": "Dia dos Namorados", "month": 6, "day": 12, "category": "comemorativa", "niches": "perfumes, joias, lingerie, eletrônicos"},
    {"name": "Festa Junina", "month": 6, "day": 24, "category": "sazonal", "niches": "decoração, roupas típicas, doces"},
    {"name": "Dia dos Pais", "month": 8, "day": 10, "category": "comemorativa", "niches": "eletrônicos, ferramentas, roupas, relógios"},
    {"name": "Shopee 8.8", "month": 8, "day": 8, "category": "marketplace", "niches": "todos — mega promoção Shopee"},
    {"name": "Dia das Crianças", "month": 10, "day": 12, "category": "comemorativa", "niches": "brinquedos, jogos, roupas infantis"},
    {"name": "Shopee 11.11", "month": 11, "day": 11, "category": "marketplace", "niches": "todos — mega promoção Shopee"},
    {"name": "Black Friday", "month": 11, "day": 28, "category": "marketplace", "niches": "eletrônicos, moda, casa, beleza — tudo"},
    {"name": "Natal", "month": 12, "day": 25, "category": "comemorativa", "niches": "presentes, decoração, eletrônicos, brinquedos"},
    {"name": "Shopee 12.12", "month": 12, "day": 12, "category": "marketplace", "niches": "todos — mega promoção Shopee"},
]


class EventCreate(Schema):
    name: str
    event_date: str
    prep_start: Optional[str] = None
    category: str = ""
    niches: str = ""
    strategy_notes: str = ""


class EventUpdate(Schema):
    status: Optional[str] = None
    strategy_notes: Optional[str] = None


@router.get("/presets")
def preset_events(
    current_user: User = Depends(get_current_user),
):
    return ResponseBuilder.success(data=PRESET_EVENTS)


@router.post("/seed")
def seed_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    year = datetime.utcnow().year
    created = 0

    for evt in PRESET_EVENTS:
        event_date = datetime(year, evt["month"], evt["day"])
        if event_date < datetime.utcnow():
            event_date = datetime(year + 1, evt["month"], evt["day"])

        prep_start = datetime(
            event_date.year,
            max(event_date.month - 2, 1),
            1,
        )

        existing = (
            db.query(SeasonalEvent)
            .filter(
                SeasonalEvent.user_id == current_user.id,
                SeasonalEvent.name == evt["name"],
                SeasonalEvent.is_active == True,
            )
            .first()
        )
        if existing:
            continue

        event = SeasonalEvent(
            user_id=current_user.id,
            name=evt["name"],
            event_date=event_date,
            prep_start=prep_start,
            category=evt["category"],
            niches=evt["niches"],
        )
        db.add(event)
        created += 1

    db.commit()

    return ResponseBuilder.success(
        data={"created": created},
        message=f"{created} eventos sazonais criados.",
        status_code=201,
    )


@router.get("")
def list_events(
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(SeasonalEvent).filter(
        SeasonalEvent.user_id == current_user.id,
        SeasonalEvent.is_active == True,
    )

    if category:
        query = query.filter(SeasonalEvent.category == category)
    if status:
        query = query.filter(SeasonalEvent.status == status)

    items = query.order_by(SeasonalEvent.event_date.asc()).all()

    now = datetime.utcnow()
    result = [
        {
            "id": e.id,
            "name": e.name,
            "event_date": e.event_date.isoformat() if e.event_date else None,
            "prep_start": e.prep_start.isoformat() if e.prep_start else None,
            "category": e.category,
            "niches": e.niches,
            "strategy_notes": e.strategy_notes,
            "status": e.status,
            "days_until": (e.event_date - now).days if e.event_date else None,
            "is_prep_phase": (
                e.prep_start is not None
                and e.prep_start <= now <= e.event_date
            ) if e.event_date else False,
        }
        for e in items
    ]

    return ResponseBuilder.success(data=result)


@router.post("")
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        event_date = datetime.fromisoformat(payload.event_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido.")

    prep = None
    if payload.prep_start:
        try:
            prep = datetime.fromisoformat(payload.prep_start)
        except ValueError:
            pass

    event = SeasonalEvent(
        user_id=current_user.id,
        name=payload.name,
        event_date=event_date,
        prep_start=prep,
        category=payload.category,
        niches=payload.niches,
        strategy_notes=payload.strategy_notes,
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    return ResponseBuilder.success(
        data={"id": event.id, "name": event.name},
        message="Evento sazonal criado.",
        status_code=201,
    )


@router.patch("/{event_id}")
def update_event(
    event_id: int,
    payload: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(SeasonalEvent)
        .filter(SeasonalEvent.id == event_id, SeasonalEvent.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")

    if payload.status is not None:
        item.status = payload.status
    if payload.strategy_notes is not None:
        item.strategy_notes = payload.strategy_notes
    db.commit()

    return ResponseBuilder.success(message="Evento atualizado.")


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(SeasonalEvent)
        .filter(SeasonalEvent.id == event_id, SeasonalEvent.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")

    item.is_active = False
    db.commit()

    return ResponseBuilder.success(message="Evento removido.")


@router.get("/upcoming")
def upcoming_events(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from datetime import timedelta
    now = datetime.utcnow()
    limit = now + timedelta(days=days)

    items = (
        db.query(SeasonalEvent)
        .filter(
            SeasonalEvent.user_id == current_user.id,
            SeasonalEvent.is_active == True,
            SeasonalEvent.event_date >= now,
            SeasonalEvent.event_date <= limit,
        )
        .order_by(SeasonalEvent.event_date.asc())
        .all()
    )

    result = [
        {
            "id": e.id,
            "name": e.name,
            "event_date": e.event_date.isoformat(),
            "category": e.category,
            "niches": e.niches,
            "days_until": (e.event_date - now).days,
        }
        for e in items
    ]

    return ResponseBuilder.success(data=result)
