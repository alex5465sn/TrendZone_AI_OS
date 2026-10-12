"""
Testes do sinal do Google Trends no Product Radar.

Cobre:
- _trend_keyword: nomes longos de marketplace viram keywords curtas.
- GoogleTrendsService._trend_from_series: classificacao rising/stable/declining.
- get_trend_signal_sync: lote com pytrends mockado (sem rede), cache e falha.
- MomentumService.radar: trend_signal aplicado ao radar_score.
"""

import pandas as pd
import pytest

from app.models.product import Product
from app.services.google_trends_service import GoogleTrendsService
from app.services.momentum_service import MomentumService


# =====================================================
# _trend_keyword
# =====================================================


def test_trend_keyword_reduces_long_name():
    name = "Vestido Balone Curto Moda Feminina Tendência 2026!"

    assert MomentumService._trend_keyword(name) == "vestido balone curto"


def test_trend_keyword_handles_empty_and_punctuation():
    assert MomentumService._trend_keyword("") == ""
    assert MomentumService._trend_keyword(None) == ""
    assert MomentumService._trend_keyword("!!!...") == ""


# =====================================================
# _trend_from_series
# =====================================================


def test_trend_from_series_rising():
    series = pd.Series([10, 10, 10, 10, 10, 10, 10, 20, 20, 20, 20, 20, 20, 20])

    assert GoogleTrendsService._trend_from_series(series) == "rising"


def test_trend_from_series_declining():
    series = pd.Series([20, 20, 20, 20, 20, 20, 20, 10, 10, 10, 10, 10, 10, 10])

    assert GoogleTrendsService._trend_from_series(series) == "declining"


def test_trend_from_series_stable():
    series = pd.Series([10] * 14)

    assert GoogleTrendsService._trend_from_series(series) == "stable"


def test_trend_from_series_empty_is_unknown():
    assert GoogleTrendsService._trend_from_series(None) == "unknown"
    assert GoogleTrendsService._trend_from_series(pd.Series([], dtype=float)) == "unknown"


# =====================================================
# get_trend_signal_sync (pytrends mockado, sem rede)
# =====================================================


class _FakePytrends:
    """Substituto do TrendReq: série alta para 'vestido', vazia para 'oioi'."""

    def __init__(self, *args, **kwargs):
        pass

    def build_payload(self, keywords, timeframe, geo):
        pass

    def interest_over_time(self):
        rising = pd.Series(
            [10] * 7 + [30] * 7,
            index=pd.date_range("2026-10-01", periods=14),
        )
        empty = pd.Series([], dtype=float)

        return pd.DataFrame({"vestido": rising, "oioi": empty})


@pytest.fixture()
def fake_pytrends(monkeypatch):
    monkeypatch.setattr(
        "app.services.google_trends_service.TrendReq", _FakePytrends
    )
    GoogleTrendsService.clear_cache()

    yield

    GoogleTrendsService.clear_cache()


def test_get_trend_signal_sync_batch(fake_pytrends):
    signals = GoogleTrendsService.get_trend_signal_sync(["vestido", "oioi"])

    assert signals["vestido"] == "rising"
    assert signals["oioi"] == "unknown"  # série vazia => unknown


def test_get_trend_signal_sync_failure_is_unknown(monkeypatch):
    GoogleTrendsService.clear_cache()

    class _BrokenPytrends:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("google fora do ar")

    monkeypatch.setattr(
        "app.services.google_trends_service.TrendReq", _BrokenPytrends
    )

    signals = GoogleTrendsService.get_trend_signal_sync(["vestido"])

    assert signals == {"vestido": "unknown"}

    GoogleTrendsService.clear_cache()


# =====================================================
# radar() com trend_signal
# =====================================================


def _add_product(db, item_id, name, score, sales, price=50.0):
    product = Product(
        item_id=item_id,
        shop_id=1,
        marketplace="shopee",
        name=name,
        image="",
        price=price,
        commission=0.13,
        rating=4.8,
        sales=sales,
        score=score,
        recommendation="TESTAR",
        offer_link="https://shopee.com.br/x",
        is_active=True,
    )

    db.add(product)
    db.commit()

    return product


def test_radar_applies_trend_signal(db_session, monkeypatch):
    GoogleTrendsService.clear_cache()

    _add_product(db_session, 1, "Vestido Balone Curto Moda", score=80, sales=100)
    _add_product(db_session, 2, "Fone Bluetooth TWS Pro", score=60, sales=50)

    monkeypatch.setattr(
        GoogleTrendsService,
        "get_trend_signal_sync",
        classmethod(lambda cls, kws: {"vestido balone curto": "rising", "fone bluetooth tws": "declining"}),
    )

    items = MomentumService.radar(db_session, limit=10)

    by_id = {item["id"]: item for item in items}

    assert by_id[1]["trend_signal"] == "rising"
    assert by_id[2]["trend_signal"] == "declining"

    # rising (85) vale mais que declining (15) com mesmo restante —
    # o produto 1 precisa terminar à frente.
    assert by_id[1]["radar_score"] > by_id[2]["radar_score"]

    assert any("Google Trends" in r for r in by_id[1]["reasons"])

    GoogleTrendsService.clear_cache()


def test_radar_trend_failure_keeps_neutral_score(db_session, monkeypatch):
    GoogleTrendsService.clear_cache()

    _add_product(db_session, 1, "Vestido Balone Curto Moda", score=80, sales=100)

    def _boom(cls, kws):
        raise RuntimeError("trends indisponivel")

    monkeypatch.setattr(
        GoogleTrendsService, "get_trend_signal_sync", classmethod(_boom)
    )

    items = MomentumService.radar(db_session, limit=10)

    assert items[0]["trend_signal"] is None
    assert items[0]["radar_score"] > 0  # score neutro não zera o radar

    GoogleTrendsService.clear_cache()


def test_radar_trend_applied_to_final_top_after_sort(db_session, monkeypatch):
    """
    Regressão: items vem da query ordenada por score INTERNO, mas o
    retorno é por radar_score — aplicar o trend no slice errado
    deixava trend_signal=None nos produtos retornados.
    """
    GoogleTrendsService.clear_cache()

    # Score interno ALTO, preço fora da faixa => radar_score baixo.
    _add_product(db_session, 1, "Produto Score Alto Sem Radar", score=99, sales=5, price=500.0)

    # Score interno MENOR, preço na faixa ideal => radar_score maior.
    _add_product(db_session, 2, "Produto Radar Campeao", score=60, sales=900, price=50.0)

    signals_received = {}

    def _fake_sync(cls, kws):
        signals_received["keywords"] = list(kws)
        return {kw: "rising" for kw in kws}

    monkeypatch.setattr(
        GoogleTrendsService, "get_trend_signal_sync", classmethod(_fake_sync)
    )

    items = MomentumService.radar(db_session, limit=1)

    # O top-1 por radar_score é o produto 2 — é ELE que precisa
    # receber o sinal (antes da correção, o slice pegava o produto 1).
    assert len(items) == 1
    assert items[0]["id"] == 2
    assert items[0]["trend_signal"] == "rising"
    assert "produto radar campeao" in signals_received["keywords"]

    GoogleTrendsService.clear_cache()
