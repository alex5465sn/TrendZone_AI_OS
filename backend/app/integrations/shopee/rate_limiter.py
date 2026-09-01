from collections import deque
from datetime import datetime, timedelta

from app.integrations.shopee.constants import (
    RATE_LIMIT_PER_HOUR,
)


class RateLimiter:

    def __init__(
        self,
        limit: int = RATE_LIMIT_PER_HOUR,
    ):

        self.limit = limit
        self.requests = deque()

    def acquire(self):

        now = datetime.utcnow()

        while (
            self.requests
            and self.requests[0]
            < now - timedelta(hours=1)
        ):
            self.requests.popleft()

        if len(self.requests) >= self.limit:

            raise RuntimeError(
                "Shopee Rate Limit excedido."
            )

        self.requests.append(now)