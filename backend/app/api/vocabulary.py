from fastapi import APIRouter, Depends
from pydantic import BaseModel as Schema
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.niche_vocabulary import NicheVocabulary
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/vocabulary",
    tags=["Niche Vocabulary"],
)

PRESETS = {
    "ecommerce": {"niche_name": "E-commerce", "term_lead": "Lead", "term_prospect": "Prospect", "term_customer": "Cliente", "term_deal": "Oportunidade", "term_hot": "Quente", "term_cold": "Frio"},
    "saude": {"niche_name": "Saúde/Clínicas", "term_lead": "Paciente Potencial", "term_prospect": "Paciente", "term_customer": "Paciente Ativo", "term_deal": "Consulta", "term_hot": "Urgente", "term_cold": "Inativo"},
    "imoveis": {"niche_name": "Imóveis", "term_lead": "Interessado", "term_prospect": "Comprador", "term_customer": "Cliente Fechado", "term_deal": "Negociação", "term_hot": "Decidido", "term_cold": "Frio"},
    "afiliados": {"niche_name": "Marketing de Afiliados", "term_lead": "Seguidor", "term_prospect": "Comprador Potencial", "term_customer": "Comprador", "term_deal": "Venda", "term_hot": "Quente", "term_cold": "Frio"},
}


class VocabularyUpdate(Schema):
    niche_name: str = "E-commerce"
    term_lead: str = "Lead"
    term_prospect: str = "Prospect"
    term_customer: str = "Cliente"
    term_deal: str = "Oportunidade"
    term_hot: str = "Quente"
    term_cold: str = "Frio"


@router.get("/presets")
def get_presets(
    current_user: User = Depends(get_current_user),
):
    return ResponseBuilder.success(data=PRESETS)


@router.get("/")
def get_vocabulary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vocab = db.query(NicheVocabulary).filter(NicheVocabulary.user_id == current_user.id).first()

    if not vocab:
        vocab = NicheVocabulary(user_id=current_user.id)
        db.add(vocab)
        db.commit()
        db.refresh(vocab)

    return ResponseBuilder.success(data={
        "niche_name": vocab.niche_name,
        "term_lead": vocab.term_lead,
        "term_prospect": vocab.term_prospect,
        "term_customer": vocab.term_customer,
        "term_deal": vocab.term_deal,
        "term_hot": vocab.term_hot,
        "term_cold": vocab.term_cold,
    })


@router.put("/")
def update_vocabulary(
    payload: VocabularyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vocab = db.query(NicheVocabulary).filter(NicheVocabulary.user_id == current_user.id).first()

    if not vocab:
        vocab = NicheVocabulary(user_id=current_user.id)
        db.add(vocab)

    vocab.niche_name = payload.niche_name
    vocab.term_lead = payload.term_lead
    vocab.term_prospect = payload.term_prospect
    vocab.term_customer = payload.term_customer
    vocab.term_deal = payload.term_deal
    vocab.term_hot = payload.term_hot
    vocab.term_cold = payload.term_cold

    db.commit()

    return ResponseBuilder.success(message="Vocabulário atualizado.")
