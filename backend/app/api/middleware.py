"""
TrendZone AI OS
================================

Global Middleware

Responsável por:

- Logging
- Tempo de resposta
- Request ID
- Headers
- Auditoria

Arquitetura Enterprise.
"""

from time import perf_counter
from uuid import uuid4

from fastapi import Request

from app.core.logger import TZLogger


class RequestMiddleware:

    @staticmethod
    async def dispatch(request: Request, call_next):

        request_id = str(uuid4())

        start = perf_counter()

        TZLogger.info(

            "REQUEST",

            f"{request.method} {request.url.path}",

        )

        response = await call_next(request)

        elapsed = perf_counter() - start

        response.headers["X-Request-ID"] = request_id

        response.headers["X-Execution-Time"] = f"{elapsed:.4f}s"

        TZLogger.success(

            "REQUEST",

            f"{request.method} {request.url.path} ({elapsed:.3f}s)",

        )

        return response