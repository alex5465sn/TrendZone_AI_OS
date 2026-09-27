"""
Testes do ProductPerformanceScore.

Cobre a logica de reponderacao de score com base em performance
real (Canais & SubIDs), incluida no fechamento do loop de dados
do Scout.
"""

from app.models.channel_tracking import ChannelTracking
from app.models.product import Product
from app.services.product_performance_score import ProductPerformanceScore


def _make_product(db_session, item_id: int, base_score: float = 50.0) -> Product:
    product = Product(
        marketplace="shopee",
        item_id=item_id,
        shop_id=1,
        category="geral",
        name=f"Produto {item_id}",
        price=99.9,
        score=base_score,
        base_score=base_score,
        performance_adjustment=0.0,
        recommendation="observar",
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


def _make_tracking(db_session, product_id: int, clicks: int, conversions: int) -> ChannelTracking:
    tracking = ChannelTracking(
        user_id=1,
        product_id=product_id,
        channel="facebook",
        sub_id="teste",
        clicks=clicks,
        conversions=conversions,
        is_active=True,
    )
    db_session.add(tracking)
    db_session.commit()
    return tracking


def test_adjustment_is_zero_without_baseline():
    assert ProductPerformanceScore._adjustment(0.1, 0.0) == 0.0


def test_adjustment_boosts_above_average_conversion():
    adjustment = ProductPerformanceScore._adjustment(conversion_rate=0.2, baseline=0.1)
    assert adjustment > 0


def test_adjustment_penalizes_below_average_conversion():
    adjustment = ProductPerformanceScore._adjustment(conversion_rate=0.05, baseline=0.1)
    assert adjustment < 0


def test_adjustment_is_clamped_to_max():
    adjustment = ProductPerformanceScore._adjustment(conversion_rate=100.0, baseline=0.001)
    assert adjustment == ProductPerformanceScore.MAX_ADJUSTMENT


def test_recalculate_all_skips_products_below_min_clicks(db_session):
    product = _make_product(db_session, item_id=1)
    _make_tracking(db_session, product.id, clicks=5, conversions=1)

    summary = ProductPerformanceScore.recalculate_all(db_session)

    assert summary["products_analyzed"] == 0
    db_session.refresh(product)
    assert product.performance_adjustment == 0.0


def test_recalculate_all_boosts_top_performer_and_penalizes_worst(db_session):
    top = _make_product(db_session, item_id=1)
    worst = _make_product(db_session, item_id=2)

    _make_tracking(db_session, top.id, clicks=100, conversions=30)
    _make_tracking(db_session, worst.id, clicks=100, conversions=2)

    summary = ProductPerformanceScore.recalculate_all(db_session)

    assert summary["products_analyzed"] == 2
    assert summary["products_boosted"] == 1
    assert summary["products_penalized"] == 1

    db_session.refresh(top)
    db_session.refresh(worst)

    assert top.performance_adjustment > 0
    assert worst.performance_adjustment < 0
    assert top.score > top.base_score
    assert worst.score < worst.base_score
