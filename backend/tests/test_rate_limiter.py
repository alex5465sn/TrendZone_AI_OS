"""
Testes do RateLimiter da integracao Shopee.

Garante que o limitador (agora conectado ao cliente HTTP da
Shopee) bloqueia corretamente quando o limite por hora e excedido
e libera novamente apos a janela de 1 hora.
"""

from datetime import datetime, timedelta

from app.integrations.shopee.rate_limiter import RateLimiter


def test_acquire_allows_requests_within_limit():
    limiter = RateLimiter(limit=3)

    limiter.acquire()
    limiter.acquire()
    limiter.acquire()

    assert len(limiter.requests) == 3


def test_acquire_blocks_when_limit_exceeded():
    limiter = RateLimiter(limit=2)

    limiter.acquire()
    limiter.acquire()

    try:
        limiter.acquire()
        assert False, "Deveria ter lancado RuntimeError."
    except RuntimeError:
        pass


def test_acquire_frees_slot_after_one_hour_window():
    limiter = RateLimiter(limit=1)
    limiter.requests.append(datetime.utcnow() - timedelta(hours=1, minutes=1))

    limiter.acquire()

    assert len(limiter.requests) == 1
