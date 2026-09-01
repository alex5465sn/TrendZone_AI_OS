"""
TrendZone AI OS
================================

Users API

Endpoints oficiais da entidade User.
"""

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse,
)

from app.services.user_service import UserService

from app.api.response import ResponseBuilder

router = APIRouter(

    prefix="/users",

    tags=["Users"],

)


@router.get("/")

def get_users(

    db: Session = Depends(get_db),

):

    users = UserService.get_all(db)

    return ResponseBuilder.success(

        data=[

            UserResponse.model_validate(user).model_dump(mode="json")

            for user in users

        ]

    )


@router.post("/")

def create_user(

    data: UserCreate,

    db: Session = Depends(get_db),

):

    user = UserService.create(

        db,

        data,

    )

    return ResponseBuilder.success(

        data=UserResponse.model_validate(user).model_dump(mode="json"),

        message="Usuário criado.",

        status_code=201,

    )