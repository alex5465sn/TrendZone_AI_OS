"""
TrendZone AI OS
================================

Admin API

Endpoints administrativos para gerenciar usuários e produtos.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_admin_user
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


# =====================================================
# USERS
# =====================================================

@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Lista todos os usuários (apenas admin)."""

    users = UserRepository.get_all(db)

    return ResponseBuilder.success(
        data=[
            {
                "id": u.id,
                "uuid": u.uuid,
                "name": u.name,
                "email": u.email,
                "role": u.role,
                "plan": u.plan,
                "company": u.company,
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat(),
            }
            for u in users
        ],
    )


@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Obtém detalhes de um usuário (apenas admin)."""

    user = UserRepository.get_by_id(db, user_id)

    if not user:
        return ResponseBuilder.error(
            message="Usuário não encontrado.",
            status_code=404,
        )

    return ResponseBuilder.success(
        data={
            "id": user.id,
            "uuid": user.uuid,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "plan": user.plan,
            "company": user.company,
            "avatar": user.avatar,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
        },
    )


@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Atualiza o role de um usuário (apenas admin)."""

    user = UserRepository.get_by_id(db, user_id)

    if not user:
        return ResponseBuilder.error(
            message="Usuário não encontrado.",
            status_code=404,
        )

    if "role" not in data:
        return ResponseBuilder.error(
            message="Campo 'role' é obrigatório.",
            status_code=400,
        )

    valid_roles = ["ADMIN", "USER", "VIEWER"]
    if data["role"] not in valid_roles:
        return ResponseBuilder.error(
            message=f"Role inválido. Valores válidos: {', '.join(valid_roles)}",
            status_code=400,
        )

    user.role = data["role"]
    user = UserRepository.update(db, user)

    return ResponseBuilder.success(
        data={
            "id": user.id,
            "email": user.email,
            "role": user.role,
        },
        message="Role atualizado com sucesso.",
    )


@router.put("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Ativa ou desativa um usuário (apenas admin)."""

    user = UserRepository.get_by_id(db, user_id)

    if not user:
        return ResponseBuilder.error(
            message="Usuário não encontrado.",
            status_code=404,
        )

    if "is_active" not in data:
        return ResponseBuilder.error(
            message="Campo 'is_active' é obrigatório.",
            status_code=400,
        )

    if data["is_active"]:
        UserRepository.restore(db, user)
    else:
        UserRepository.soft_delete(db, user)

    return ResponseBuilder.success(
        data={
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
        },
        message="Status do usuário atualizado com sucesso.",
    )


# =====================================================
# PRODUCTS
# =====================================================

@router.get("/products")
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Lista todos os produtos (apenas admin)."""

    products = ProductRepository.get_all(db)

    return ResponseBuilder.success(
        data=[
            {
                "id": p.id,
                "uuid": p.uuid,
                "item_id": p.item_id,
                "name": p.name,
                "price": float(p.price),
                "commission": float(p.commission),
                "score": p.score,
                "recommendation": p.recommendation,
                "sales": p.sales,
                "rating": p.rating,
                "created_at": p.created_at.isoformat(),
            }
            for p in products
        ],
    )


@router.get("/products/stats")
def get_products_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Retorna estatísticas de produtos (apenas admin)."""

    products = ProductRepository.get_all(db)

    total = len(products)
    avg_score = sum(p.score for p in products) / total if total > 0 else 0
    avg_commission = sum(float(p.commission) for p in products) / total if total > 0 else 0
    total_sales = sum(p.sales for p in products)

    return ResponseBuilder.success(
        data={
            "total_products": total,
            "average_score": round(avg_score, 2),
            "average_commission": round(avg_commission, 2),
            "total_sales": total_sales,
        },
    )


# =====================================================
# SYSTEM
# =====================================================

@router.get("/stats")
def get_system_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Retorna estatísticas do sistema (apenas admin)."""

    total_users = UserRepository.count(db)
    total_products = ProductRepository.count(db)
    admins = UserRepository.get_admins(db)

    return ResponseBuilder.success(
        data={
            "total_users": total_users,
            "total_products": total_products,
            "total_admins": len(admins),
            "system_status": "online",
        },
    )
