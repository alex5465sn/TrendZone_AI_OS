from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.security.jwt import SECRET_KEY, ALGORITHM

security = HTTPBearer(
    auto_error=True,
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido.",
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido.",
        )

    user = UserRepository.get_by_email(
        db,
        email,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado.",
        )

    return user