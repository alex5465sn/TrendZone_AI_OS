from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.api.response import ResponseBuilder

router = APIRouter(prefix="/admin", tags=["Admin Seed"])


@router.post("/seed")
def seed_admin(db: Session = Depends(get_db)):
    user = UserRepository.get_by_email(db, "admin@trendzone.com")

    if not user:
        return ResponseBuilder.error(
            message="Usuário admin@trendzone.com não encontrado. Registre-se primeiro.",
            status_code=404,
        )

    if user.role == "ADMIN":
        return ResponseBuilder.success(
            message="Usuário já é ADMIN.",
            data={"email": user.email, "role": user.role},
        )

    user.role = "ADMIN"
    UserRepository.update(db, user)

    return ResponseBuilder.success(
        message="Usuário promovido a ADMIN com sucesso.",
        data={"email": user.email, "role": user.role},
    )
