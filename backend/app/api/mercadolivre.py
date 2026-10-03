"""
TrendZone AI OS
================================

Mercado Livre API

Rotas para OAuth, busca de produtos e
gerenciamento da conta conectada.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.mercadolivre_auth_service import (
    MercadoLivreAuthService,
    MercadoLivreAuthError,
)
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/mercadolivre",
    tags=["Mercado Livre"],
)


@router.get("/authorize-url")
def authorize_url(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Monta a URL de autorização do Mercado Livre.

    O usuário abre essa URL, faz login com a conta
    PRINCIPAL (administrador, não colaborador) e
    autoriza o aplicativo. O ML redireciona para
    /mercadolivre/callback com ?code=...&state=...
    """

    try:

        result = MercadoLivreAuthService.build_authorize_url(
            db,
            current_user,
        )

        return ResponseBuilder.success(
            data=result,
            message="URL de autorização gerada. Abra no navegador.",
        )

    except MercadoLivreAuthError as e:

        return ResponseBuilder.error(
            message=str(e),
        )


@router.get("/callback")
def callback(
    code: str = Query(...),
    state: str = Query(default=""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Callback do Mercado Livre (OAuth).

    O ML redireciona aqui com ?code=...&state=...
    após o usuário autorizar. Trocamos o code pelo
    par access_token + refresh_token.
    """

    try:

        result = MercadoLivreAuthService.handle_callback(
            db,
            current_user,
            code,
            state or None,
        )

        return ResponseBuilder.success(
            data=result,
            message="Conta do Mercado Livre conectada com sucesso!",
        )

    except MercadoLivreAuthError as e:

        return ResponseBuilder.error(
            message=str(e),
        )


@router.get("/status")
def status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Status da conexão com o Mercado Livre.
    """

    result = MercadoLivreAuthService.status(
        db,
        current_user,
    )

    return ResponseBuilder.success(
        data=result,
    )


@router.post("/refresh")
def refresh(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Renova manualmente o access_token do Mercado Livre.

    (Normalmente a renovação é automática quando
    necessário, mas você pode forçar aqui.)
    """

    try:

        result = MercadoLivreAuthService.refresh(
            db,
            current_user,
        )

        return ResponseBuilder.success(
            data=result,
            message="Token renovado com sucesso.",
        )

    except MercadoLivreAuthError as e:

        return ResponseBuilder.error(
            message=str(e),
        )
