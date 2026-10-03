"""
TrendZone AI OS
================================

Serviço de OAuth do Mercado Livre.

Implementa o fluxo oficial do Mercado Livre
(Authorization Code Grant Type — Server Side):

1. build authorize URL  ->  usuário abre, loga com a
   conta PRINCIPAL (admin) e autoriza o app.
2. ML redireciona para o redirect_uri EXATAMENTE
   igual ao cadastrado no DevCenter, acrescentando
   ?code=...&state=...
3. exchange code -> access_token (6h) + refresh_token
   (uso único — cada refresh devolve um novo).
4. Auto-refresh: quando o access_token expira,
   usamos o refresh_token e persistimos o NOVO par.

Credenciais vêm da conta conectada do usuário
(MarketplaceAccount, criptografadas) com fallback
para as configurações globais (settings).
"""

from __future__ import annotations

import json
import secrets
import time

from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models.user import User
from app.schemas.marketplace_account import MarketplaceAccountUpdate
from app.services.marketplace_account_service import (
    MarketplaceAccountService,
    decrypt_secret,
    encrypt_secret,
)
from app.integrations.mercadolivre.client import (
    MercadoLivreClient,
    MercadoLivreException,
)

MARKETPLACE = "mercado_livre"

# Chaves do campo 'extra' da conta
EXTRA_APP_ID = "app_id"
EXTRA_CLIENT_SECRET_ENC = "client_secret_enc"
EXTRA_REDIRECT_URI = "redirect_uri"
EXTRA_USE_PKCE = "use_pkce"
EXTRA_EXPIRES_AT = "expires_at"
EXTRA_ML_USER_ID = "ml_user_id"
EXTRA_NICKNAME = "nickname"
EXTRA_PENDING_STATE = "pending_state"
EXTRA_PENDING_VERIFIER = "pending_code_verifier"

# Margem de segurança: renovar 60s antes de expirar
REFRESH_MARGIN_SECONDS = 60


class MercadoLivreAuthError(Exception):
    """Erro de negócio no fluxo OAuth do Mercado Livre."""


class MercadoLivreAuthService:

    client = MercadoLivreClient()

    # =====================================================
    # Credenciais
    # =====================================================

    @staticmethod
    def _load_account(
        db: Session,
        user: User,
    ):
        account = MarketplaceAccountService.get_by_user_and_marketplace(
            db,
            user.id,
            MARKETPLACE,
        )

        if account is None:
            raise MercadoLivreAuthError(
                "Conta do Mercado Livre não encontrada. Conecte o app "
                "(app_id + client_secret) antes de autorizar."
            )

        return account

    @staticmethod
    def _resolve_credentials(
        extra: dict,
    ) -> tuple[str, str, str, bool]:
        """
        (app_id, client_secret, redirect_uri, use_pkce)

        Prioriza a conta do usuário; fallback para settings.
        """

        app_id = str(extra.get(EXTRA_APP_ID) or "").strip() \
            or settings.MERCADOLIVRE_CLIENT_ID

        client_secret = decrypt_secret(
            str(extra.get(EXTRA_CLIENT_SECRET_ENC) or ""),
        ) or settings.MERCADOLIVRE_CLIENT_SECRET

        redirect_uri = str(extra.get(EXTRA_REDIRECT_URI) or "").strip() \
            or settings.MERCADOLIVRE_REDIRECT_URI

        use_pkce = bool(
            extra.get(EXTRA_USE_PKCE, False),
        )

        return app_id, client_secret, redirect_uri, use_pkce

    # =====================================================
    # 1. Authorize URL
    # =====================================================

    @classmethod
    def build_authorize_url(
        cls,
        db: Session,
        user: User,
        redirect_uri: str | None = None,
    ) -> dict:
        """
        Monta a URL de autorização e registra o 'state'
        (e o code_verifier, quando PKCE) na conta do usuário
        para validação no callback.
        """

        account = cls._load_account(db, user)

        extra = json.loads(account.extra or "{}")

        app_id, client_secret, configured_uri, use_pkce = (
            cls._resolve_credentials(extra)
        )

        if not app_id or not client_secret:
            raise MercadoLivreAuthError(
                "App ID / Client Secret do Mercado Livre não configurados. "
                "Reconecte a conta informando app_id e client_secret."
            )

        # redirect_uri passado na requisição precisa ser o mesmo
        # cadastrado no DevCenter — não pode ser qualquer URL.
        redirect_uri = (redirect_uri or "").strip() or configured_uri

        state = secrets.token_urlsafe(16)

        verifier = None

        if use_pkce:
            verifier = MercadoLivreClient.generate_code_verifier()

        url = cls.client.build_authorize_url(
            app_id=app_id,
            redirect_uri=redirect_uri,
            state=state,
            code_verifier=verifier,
        )

        # Persiste state/verifier para o callback validar.
        extra[EXTRA_PENDING_STATE] = state
        extra[EXTRA_PENDING_VERIFIER] = verifier or ""
        extra[EXTRA_REDIRECT_URI] = redirect_uri

        MarketplaceAccountService.update_tokens(
            db,
            user,
            MARKETPLACE,
            MarketplaceAccountUpdate(
                extra=json.dumps(extra, ensure_ascii=False),
            ),
        )

        return {
            "authorize_url": url,
            "state": state,
            "redirect_uri": redirect_uri,
        }

    # =====================================================
    # 2. Callback (code -> token)
    # =====================================================

    @classmethod
    def handle_callback(
        cls,
        db: Session,
        user: User,
        code: str,
        state: str | None = None,
    ) -> dict:
        """
        Troca o authorization code pelo par de tokens,
        valida contra /users/me e persiste tudo
        criptografado na conta do usuário.
        """

        account = cls._load_account(db, user)

        extra = json.loads(account.extra or "{}")

        pending_state = str(extra.get(EXTRA_PENDING_STATE) or "")

        if pending_state and state and state != pending_state:
            raise MercadoLivreAuthError(
                "State inválido — a resposta não pertence à solicitação "
                "iniciada por você. Gere a URL de autorização novamente."
            )

        app_id, client_secret, redirect_uri, _ = (
            cls._resolve_credentials(extra)
        )

        verifier = str(extra.get(EXTRA_PENDING_VERIFIER) or "") or None

        try:

            tokens = cls.client.exchange_code(
                app_id=app_id,
                client_secret=client_secret,
                code=code.strip(),
                redirect_uri=redirect_uri,
                code_verifier=verifier,
            )

        except MercadoLivreException as e:

            raise MercadoLivreAuthError(
                f"Falha ao trocar o código por token: {e.message}",
            ) from e

        profile = {}

        try:

            profile = cls.client.get_user_me(
                tokens["access_token"],
            )

        except MercadoLivreException:
            # Token válido mesmo sem conseguir ler o perfil
            # (pode ser scope de leitura restrito).
            profile = {}

        cls._persist_tokens(
            db,
            user,
            account,
            extra,
            tokens,
            profile,
        )

        return cls.status(db, user)

    # =====================================================
    # 3. Refresh automático
    # =====================================================

    @classmethod
    def get_valid_access_token(
        cls,
        db: Session,
        user: User,
    ) -> str | None:
        """
        Devolve um access_token válido, renovando
        automaticamente quando estiver expirado
        (o refresh_token do ML é de uso único e cada
        renovação devolve um novo par de tokens).
        """

        account = MarketplaceAccountService.get_by_user_and_marketplace(
            db,
            user.id,
            MARKETPLACE,
        )

        if account is None:
            return None

        extra = json.loads(account.extra or "{}")

        access_token = decrypt_secret(account.access_token or "")

        if not access_token:
            return None

        expires_at = float(extra.get(EXTRA_EXPIRES_AT) or 0)

        if expires_at - REFRESH_MARGIN_SECONDS > time.time():
            return access_token

        # Expirado (ou vencendo) -> renovar
        try:

            return cls._do_refresh(
                db,
                user,
                account,
            )

        except MercadoLivreAuthError:
            return None

    @classmethod
    def refresh(
        cls,
        db: Session,
        user: User,
    ) -> dict:
        """
        Renova manualmente os tokens do Mercado Livre
        e devolve o status da conexão.
        """

        account = cls._load_account(db, user)

        cls._do_refresh(
            db,
            user,
            account,
        )

        return cls.status(db, user)

    @classmethod
    def _do_refresh(
        cls,
        db: Session,
        user: User,
        account,
    ) -> str:
        """
        Renova os tokens via refresh_token (uso único)
        e devolve o NOVO access_token.
        """

        extra = json.loads(account.extra or "{}")

        app_id, client_secret, _, _ = cls._resolve_credentials(extra)

        refresh_token = decrypt_secret(
            account.refresh_token or "",
        )

        if not refresh_token:
            raise MercadoLivreAuthError(
                "Nenhum refresh_token armazenado. Faça o fluxo de "
                "autorização novamente."
            )

        try:

            tokens = cls.client.refresh_access_token(
                app_id=app_id,
                client_secret=client_secret,
                refresh_token=refresh_token,
            )

        except MercadoLivreException as e:

            raise MercadoLivreAuthError(
                f"Falha ao renovar o token do Mercado Livre: {e.message}",
            ) from e

        cls._persist_tokens(
            db,
            user,
            account,
            extra,
            tokens,
            {},
        )

        return tokens["access_token"]

    # =====================================================
    # Persistência
    # =====================================================

    @classmethod
    def _persist_tokens(
        cls,
        db: Session,
        user: User,
        account,
        extra: dict,
        tokens: dict,
        profile: dict,
    ) -> None:
        """
        Persiste tokens (criptografados), expiração e
        dados do perfil na conta do usuário.
        """

        expires_in = int(tokens.get("expires_in") or 21600)

        extra[EXTRA_EXPIRES_AT] = time.time() + expires_in

        extra[EXTRA_ML_USER_ID] = tokens.get("user_id") \
            or profile.get("id") \
            or extra.get(EXTRA_ML_USER_ID)

        extra[EXTRA_NICKNAME] = profile.get("nickname") \
            or extra.get(EXTRA_NICKNAME) \
            or ""

        # Limpa o estado pendente (code já consumido)
        extra.pop(EXTRA_PENDING_STATE, None)
        extra.pop(EXTRA_PENDING_VERIFIER, None)

        MarketplaceAccountService.update_tokens(
            db,
            user,
            MARKETPLACE,
            MarketplaceAccountUpdate(
                access_token=tokens["access_token"],
                refresh_token=tokens.get("refresh_token") or "",
                extra=json.dumps(extra, ensure_ascii=False),
                status="conectada",
            ),
        )

    # =====================================================
    # Status
    # =====================================================

    @classmethod
    def status(
        cls,
        db: Session,
        user: User,
    ) -> dict:

        account = MarketplaceAccountService.get_by_user_and_marketplace(
            db,
            user.id,
            MARKETPLACE,
        )

        if account is None:
            return {
                "connected": False,
                "marketplace": MARKETPLACE,
            }

        extra = json.loads(account.extra or "{}")

        expires_at = float(extra.get(EXTRA_EXPIRES_AT) or 0)

        has_tokens = bool(
            decrypt_secret(account.access_token or ""),
        )

        expires_at_iso = time.strftime(
            "%Y-%m-%dT%H:%M:%SZ",
            time.gmtime(expires_at),
        ) if expires_at else ""

        return {
            "connected": has_tokens,
            "marketplace": MARKETPLACE,
            "status": account.status,
            "app_id": extra.get(EXTRA_APP_ID) or "",
            "nickname": extra.get(EXTRA_NICKNAME) or "",
            "ml_user_id": extra.get(EXTRA_ML_USER_ID) or "",
            "expires_at": expires_at_iso,
            "expired": bool(
                expires_at and expires_at <= time.time()
            ),
        }
