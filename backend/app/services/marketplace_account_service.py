"""
TrendZone AI OS
================================

Serviço de Contas de Marketplace por usuário.

Criptografia: tokens de acesso são segredos de terceiros
(clientes/afiliados) — nunca podem ficar em texto puro no
banco. Usamos Fernet (cryptography) com chave derivada do
SECRET_KEY da aplicação via SHA-256.

Regras:
- Um usuário pode conectar 1 conta por marketplace.
- Nunca expor tokens (nem ciphertext) em respostas de API.
- get_credentials() descriptografa apenas em memória,
  para uso interno (ex.: sync de vendas do usuário).
"""

import hashlib
import base64
import json
from datetime import datetime, timezone

from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models import User
from app.models.marketplace_account import MarketplaceAccount
from app.schemas.marketplace_account import (
    MarketplaceAccountCreate,
    MarketplaceAccountUpdate,
)

SUPPORTED_MARKETPLACES = [
    "shopee",
    "mercado_livre",
    "amazon",
    "aliexpress",
    "magalu",
    "tiktok",
]


def _fernet() -> Fernet:
    key = hashlib.sha256(settings.SECRET_KEY.encode("utf-8")).digest()
    return Fernet(base64.urlsafe_b64encode(key))


def _encrypt(plain: str) -> str:
    if not plain:
        return ""
    return _fernet().encrypt(plain.encode("utf-8")).decode("utf-8")


def _decrypt(cipher: str) -> str:
    if not cipher:
        return ""
    try:
        return _fernet().decrypt(cipher.encode("utf-8")).decode("utf-8")
    except (InvalidToken, ValueError):
        return ""


class MarketplaceAccountService:

    # =====================================================
    # Leitura (somente do próprio usuário)
    # =====================================================

    @staticmethod
    def list_for_user(db: Session, user_id: int) -> list[MarketplaceAccount]:
        stmt = (
            select(MarketplaceAccount)
            .where(
                MarketplaceAccount.user_id == user_id,
                MarketplaceAccount.is_active.is_(True),
            )
            .order_by(MarketplaceAccount.marketplace)
        )
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def get_by_user_and_marketplace(
        db: Session,
        user_id: int,
        marketplace: str,
    ) -> MarketplaceAccount | None:
        stmt = select(MarketplaceAccount).where(
            MarketplaceAccount.user_id == user_id,
            MarketplaceAccount.marketplace == marketplace,
            MarketplaceAccount.is_active.is_(True),
        )
        return db.execute(stmt).scalars().first()

    # =====================================================
    # Conexão / Desconexão
    # =====================================================

    @staticmethod
    def connect(
        db: Session,
        user: User,
        data: MarketplaceAccountCreate,
    ) -> MarketplaceAccount:
        marketplace = data.marketplace.strip().lower()
        if marketplace not in SUPPORTED_MARKETPLACES:
            raise ValueError(
                f"Marketplace '{marketplace}' não suportado. "
                f"Suportados: {', '.join(SUPPORTED_MARKETPLACES)}."
            )

        existing = MarketplaceAccountService.get_by_user_and_marketplace(
            db, user.id, marketplace
        )
        if existing is not None:
            raise ValueError(
                f"Conta do marketplace '{marketplace}' já está conectada. "
                "Use PATCH para atualizar os tokens."
            )

        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        account = MarketplaceAccount(
            user_id=user.id,
            marketplace=marketplace,
            access_token=_encrypt(data.access_token.strip()),
            refresh_token=_encrypt((data.refresh_token or "").strip()),
            extra=json.dumps(
                json.loads(data.extra) if data.extra else {},
                ensure_ascii=False,
            ),
            status="conectada",
            last_validated_at=now,
        )
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def update_tokens(
        db: Session,
        user: User,
        marketplace: str,
        data: MarketplaceAccountUpdate,
    ) -> MarketplaceAccount:
        account = MarketplaceAccountService.get_by_user_and_marketplace(
            db, user.id, marketplace.strip().lower()
        )
        if account is None:
            raise ValueError("Conta não encontrada para este usuário.")

        if data.access_token is not None:
            account.access_token = _encrypt(data.access_token.strip())
        if data.refresh_token is not None:
            account.refresh_token = _encrypt(data.refresh_token.strip())
        if data.extra is not None:
            account.extra = json.dumps(
                json.loads(data.extra) if data.extra else {},
                ensure_ascii=False,
            )
        if data.status is not None:
            account.status = data.status
        if data.status in ("conectada", "erro") and data.access_token:
            account.last_validated_at = (
                datetime.now(timezone.utc).isoformat(timespec="seconds")
            )

        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def disconnect(
        db: Session,
        user: User,
        marketplace: str,
    ) -> None:
        account = MarketplaceAccountService.get_by_user_and_marketplace(
            db, user.id, marketplace.strip().lower()
        )
        if account is None:
            raise ValueError("Conta não encontrada para este usuário.")

        account.is_active = False
        account.status = "desconectada"
        db.commit()

    # =====================================================
    # Uso interno (tokens descriptografados em memória)
    # =====================================================

    @staticmethod
    def get_credentials(
        db: Session,
        user_id: int,
        marketplace: str,
    ) -> dict | None:
        """Devolve credenciais descriptografadas para operações internas."""
        account = MarketplaceAccountService.get_by_user_and_marketplace(
            db, user_id, marketplace
        )
        if account is None:
            return None
        return {
            "access_token": _decrypt(account.access_token),
            "refresh_token": _decrypt(account.refresh_token),
            "extra": json.loads(account.extra or "{}"),
        }
