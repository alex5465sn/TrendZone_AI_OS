"""
TrendZone AI OS
================================

Authentication API

Responsável pela autenticação
dos usuários.
"""

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.auth import (
    LoginRequest,
    Token,
)

from app.security.auth import authenticate_user
from app.security.jwt import create_access_token

from app.api.response import ResponseBuilder

router = APIRouter(

    prefix="/auth",

    tags=["Authentication"],

)


@router.post(

    "/login",

    response_model=Token,

)

def login(

    credentials: LoginRequest,

    db: Session = Depends(get_db),

):

    user = authenticate_user(

        db,

        credentials.email,

        credentials.password,

    )

    token = create_access_token(

        {

            "sub": user.email,

        }

    )

    return Token(

        access_token=token,

        token_type="bearer",

    )


@router.get("/validate")

def validate():

    return ResponseBuilder.success(

        message="Token válido.",

    )