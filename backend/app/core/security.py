"""
TrendZone AI OS
================================

Security Module

Responsável por:
- Hash de senhas (bcrypt)
- Geração de JWT
- Validação de tokens
- Permissões e roles
"""

from datetime import datetime, timedelta, timezone


import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.settings import settings

# =====================================================
# PASSWORD HASHING
# =====================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Hash uma senha usando bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)


# =====================================================
# JWT TOKENS
# =====================================================

class TokenPayload(BaseModel):
    """Payload do JWT."""
    sub: str
    exp: datetime
    iat: datetime
    type: str
    role: str | None = None


def create_access_token(
    subject: str,
    role: str = "USER",
    expires_delta: timedelta | None = None,
) -> str:
    """Cria um access token JWT."""

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": now,
        "type": "access",
        "role": role,
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def create_refresh_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Cria um refresh token JWT."""

    if expires_delta is None:
        expires_delta = timedelta(days=7)

    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": now,
        "type": "refresh",
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def decode_token(token: str) -> TokenPayload | None:
    """Decodifica e valida um JWT."""

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        return TokenPayload(**payload)

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None


# =====================================================
# ROLES & PERMISSIONS
# =====================================================

ROLES = {
    "ADMIN": ["read", "write", "delete", "manage_users"],
    "USER": ["read", "write"],
    "VIEWER": ["read"],
}


def has_permission(role: str, permission: str) -> bool:
    """Verifica se um role tem uma permissão."""
    return permission in ROLES.get(role, [])


def has_role(user_role: str, required_role: str) -> bool:
    """Verifica se o usuário tem o role necessário."""

    role_hierarchy = {
        "ADMIN": 3,
        "USER": 2,
        "VIEWER": 1,
    }

    user_level = role_hierarchy.get(user_role, 0)
    required_level = role_hierarchy.get(required_role, 0)

    return user_level >= required_level
