"""
TrendZone AI OS
================================

Dependencies

Dependências para injeção em endpoints.
"""

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import decode_token
from app.services.auth_service import AuthService
from app.models.user import User


async def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
) -> User:
    """Obtém o usuário autenticado a partir do JWT."""

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Token não fornecido.",
        )

    token = authorization.replace("Bearer ", "")

    try:
        user = AuthService.get_current_user(db, token)
        return user
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado.",
        )


async def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Obtém o usuário autenticado e valida se é ADMIN."""

    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Acesso negado. Apenas administradores podem acessar este recurso.",
        )

    return current_user


async def get_user_or_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Obtém o usuário autenticado (USER ou ADMIN)."""

    if current_user.role not in ["USER", "ADMIN"]:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado.",
        )

    return current_user
