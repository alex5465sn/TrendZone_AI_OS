from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenStorage:

    access_token: str | None = None
    refresh_token: str | None = None
    expires_at: datetime | None = None

    @property
    def authenticated(self) -> bool:
        return self.access_token is not None

    @property
    def expired(self) -> bool:

        if self.expires_at is None:
            return True

        return datetime.utcnow() >= self.expires_at