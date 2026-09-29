"""
TrendZone AI OS
================================

Grupos de Divulgação — Robô Divulgador

Fluxo semi-automático inspirado em ferramentas do mercado:
1. Gera um texto de divulgação com IA (por tom) para um produto.
2. Lista os grupos de WhatsApp/Facebook cadastrados pelo usuário.
3. O usuário copia o texto e publica manualmente no grupo.

Não publica automaticamente em grupos de WhatsApp/Facebook —
isso exige integrações (Baileys/WAHA para WhatsApp, permissões
especiais de administrador de grupo no Facebook) que não estão
disponíveis nesta versão. Este módulo cobre geração de texto +
organização dos grupos, o "copiar e colar" fica com o usuário.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.divulgation_group import DivulgationGroup
from app.repositories.divulgation_group_repository import DivulgationGroupRepository
from app.repositories.product_repository import ProductRepository
from app.services.content_generator_service import ContentGeneratorService
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/divulgation-groups",
    tags=["Grupos de Divulgação"],
)


class DivulgationGroupRequest(BaseModel):
    name: str
    platform: str = "facebook"
    category: str = "geral"
    description: str | None = None
    link: str | None = None
    best_time: str | None = None
    member_count: int = 0

    @field_validator("member_count", mode="before")
    @classmethod
    def _coerce_member_count(cls, v):
        if v is None or v == "":
            return 0
        if isinstance(v, str):
            v = v.replace(".", "").replace(",", "")
            if v == "":
                return 0
        return int(float(v))


class DivulgationGroupUpdateRequest(BaseModel):
    name: str | None = None
    platform: str | None = None
    category: str | None = None
    description: str | None = None
    link: str | None = None
    best_time: str | None = None
    member_count: int | None = None

    @field_validator("member_count", mode="before")
    @classmethod
    def _coerce_member_count(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str):
            v = v.replace(".", "").replace(",", "")
            if v == "":
                return None
        return int(float(v))


class GenerateTextRequest(BaseModel):
    product_id: int
    tone: str = "oferta"


def _serialize(g: DivulgationGroup) -> dict:
    return {
        "id": g.id,
        "name": g.name,
        "platform": g.platform,
        "category": g.category,
        "description": g.description,
        "link": g.link,
        "best_time": g.best_time,
        "member_count": g.member_count,
        "status": g.status,
    }


@router.get("")
def list_groups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    groups = DivulgationGroupRepository.get_all_active(db)
    return ResponseBuilder.success(data=[_serialize(g) for g in groups])


@router.post("")
def create_group(
    payload: DivulgationGroupRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group = DivulgationGroup(
        name=payload.name,
        platform=payload.platform,
        category=payload.category,
        description=payload.description or "",
        link=payload.link or "",
        best_time=payload.best_time or "",
        member_count=payload.member_count,
        status="ativo",
    )
    DivulgationGroupRepository.create(db, group)
    return ResponseBuilder.success(data={"id": group.id}, message="Grupo cadastrado com sucesso.")


@router.put("/{group_id}")
def update_group(
    group_id: int,
    payload: DivulgationGroupUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group = DivulgationGroupRepository.get_by_id(db, group_id)
    if not group:
        return ResponseBuilder.error(message="Grupo não encontrado.", status_code=404)

    if payload.name is not None:
        group.name = payload.name
    if payload.platform is not None:
        group.platform = payload.platform
    if payload.category is not None:
        group.category = payload.category
    if payload.description is not None:
        group.description = payload.description
    if payload.link is not None:
        group.link = payload.link
    if payload.best_time is not None:
        group.best_time = payload.best_time
    if payload.member_count is not None:
        group.member_count = payload.member_count

    DivulgationGroupRepository.update(db, group)
    return ResponseBuilder.success(data=_serialize(group), message="Grupo atualizado com sucesso.")


@router.delete("/{group_id}")
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group = DivulgationGroupRepository.get_by_id(db, group_id)
    if not group:
        return ResponseBuilder.error(message="Grupo não encontrado.", status_code=404)

    DivulgationGroupRepository.soft_delete(db, group)
    return ResponseBuilder.success(message="Grupo removido.")


@router.post("/generate-text")
def generate_text(
    payload: GenerateTextRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = ProductRepository.get_by_id(db, payload.product_id)
    if not product:
        return ResponseBuilder.error(message="Produto não encontrado.", status_code=404)

    content = ContentGeneratorService.generate_smart(
        {
            "name": product.name,
            "price": float(product.price or 0),
            "commission": float(product.commission or 0),
            "rating": float(product.rating or 0),
            "sales": int(product.sales or 0),
        },
        tone=payload.tone,
    )
    content["link"] = product.offer_link or ""
    return ResponseBuilder.success(data=content)
