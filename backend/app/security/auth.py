from app.repositories.user_repository import UserRepository
from app.security.hash import verify_password


def authenticate_user(db, email: str, password: str):

    user = UserRepository.get_by_email(
        db,
        email,
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user