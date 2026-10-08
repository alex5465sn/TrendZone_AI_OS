"""
TrendZone AI OS
================================

Marketplace Accounts API

Conexão de contas de afiliado por usuário
(Shopee hoje; Mercado Livre, Amazon etc. no futuro).
"""

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas.marketplace_account import (
    MarketplaceAccountCreate,
    MarketplaceAccountResponse,
    MarketplaceAccountUpdate,
)
from app.services.marketplace_account_service import (
    MarketplaceAccountService,
    SUPPORTED_MARKETPLACES,
)
from app.api.response import ResponseBuilder

router = APIRouter(
    prefix="/marketplace-accounts",
    tags=["Marketplace Accounts"],
)


def _mask(account) -> dict:
    return MarketplaceAccountResponse(
        id=account.id,
        uuid=account.uuid,
        marketplace=account.marketplace,
        has_access_token=bool(account.access_token),
        has_refresh_token=bool(account.refresh_token),
        status=account.status,
        last_validated_at=account.last_validated_at,
        is_active=account.is_active,
        created_at=account.created_at,
        updated_at=account.updated_at,
    ).model_dump(mode="json")


@router.get("/available")
def available_marketplaces():

    return ResponseBuilder.success(
        data={"marketplaces": SUPPORTED_MARKETPLACES},
    )


@router.get("")
def my_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    accounts = MarketplaceAccountService.list_for_user(
        db, current_user.id
    )

    return ResponseBuilder.success(
        data=[_mask(a) for a in accounts],
    )


@router.post("")
def connect_account(
    data: MarketplaceAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:
        account = MarketplaceAccountService.connect(
            db, current_user, data
        )
    except ValueError as e:
        return ResponseBuilder.error(
            message=str(e),
        )

    return ResponseBuilder.success(
        data=_mask(account),
        message="Conta conectada com sucesso.",
    )


@router.patch("/{marketplace}")
def update_account(
    marketplace: str,
    data: MarketplaceAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:
        account = MarketplaceAccountService.update_tokens(
            db, current_user, marketplace, data
        )
    except ValueError as e:
        return ResponseBuilder.error(
            message=str(e),
        )

    return ResponseBuilder.success(
        data=_mask(account),
        message="Conta atualizada com sucesso.",
    )


@router.delete("/{marketplace}")
def disconnect_account(
    marketplace: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:
        MarketplaceAccountService.disconnect(
            db, current_user, marketplace
        )
    except ValueError as e:
        return ResponseBuilder.error(
            message=str(e),
        )

    return ResponseBuilder.success(
        message="Conta desconectada.",
    )
