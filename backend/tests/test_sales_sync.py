"""
Testes de regressao para a sincronizacao de vendas reais da Shopee.

Cobre a classe de bug corrigida em 2026-10: um servico/endpoint que
existe e funciona isoladamente, mas nunca e chamado por ninguem
(nem agendado, nem disparado por nenhuma tela), fazendo com que
vendas reais nunca cheguem ao banco nem ao motor de Score.
"""

from app.models.product import Product
from app.models.sale import Sale
from app.repositories.sale_repository import SaleRepository
from app.services.sales_tracker_service import SalesTrackerService
from app.services.facebook_scheduler_service import FacebookSchedulerService
from app.services.product_performance_score import ProductPerformanceScore


def _make_product(db_session, item_id: int) -> Product:
    product = Product(
        marketplace="shopee",
        item_id=item_id,
        shop_id=1,
        category="geral",
        name=f"Produto {item_id}",
        price=99.9,
        score=50.0,
        base_score=50.0,
        performance_adjustment=0.0,
        recommendation="observar",
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


def _conversion_node(conversion_id: str, utm_content: str, order_status: str = "completed") -> dict:
    return {
        "conversionId": conversion_id,
        "totalCommission": 10.0,
        "sellerCommission": 8.0,
        "shopeeCommissionCapped": 2.0,
        "netCommission": 9.5,
        "buyerType": "new",
        "device": "mobile",
        "productType": "mall",
        "utmContent": utm_content,
        "clickTime": "1700000000",
        "purchaseTime": "1700000100",
        "orders": [{"orderId": "ORDER123", "shopType": "mall", "orderStatus": order_status}],
    }


def test_sync_and_persist_creates_sale_linked_to_product(db_session, monkeypatch):
    product = _make_product(db_session, item_id=555)

    monkeypatch.setattr(
        SalesTrackerService,
        "fetch_conversions",
        staticmethod(lambda **kwargs: [_conversion_node("conv-1", "555")]),
    )

    result = SalesTrackerService.sync_and_persist(db_session, days_back=7)

    assert result["new_sales"] == 1
    assert result["updated_sales"] == 0

    sale = SaleRepository.get_by_conversion_id(db_session, "conv-1")
    assert sale is not None
    assert sale.product_id == product.id
    assert sale.status == "confirmada"


def test_sync_and_persist_keeps_sale_without_known_product(db_session, monkeypatch):
    monkeypatch.setattr(
        SalesTrackerService,
        "fetch_conversions",
        staticmethod(lambda **kwargs: [_conversion_node("conv-2", "9999999")]),
    )

    result = SalesTrackerService.sync_and_persist(db_session, days_back=7)

    assert result["new_sales"] == 1
    sale = SaleRepository.get_by_conversion_id(db_session, "conv-2")
    assert sale.product_id is None


def test_sync_and_persist_updates_existing_sale(db_session, monkeypatch):
    product = _make_product(db_session, item_id=777)

    monkeypatch.setattr(
        SalesTrackerService,
        "fetch_conversions",
        staticmethod(lambda **kwargs: [_conversion_node("conv-3", "777", order_status="pending")]),
    )
    SalesTrackerService.sync_and_persist(db_session, days_back=7)

    monkeypatch.setattr(
        SalesTrackerService,
        "fetch_conversions",
        staticmethod(lambda **kwargs: [_conversion_node("conv-3", "777", order_status="completed")]),
    )
    result = SalesTrackerService.sync_and_persist(db_session, days_back=7)

    assert result["new_sales"] == 0
    assert result["updated_sales"] == 1

    sale = SaleRepository.get_by_conversion_id(db_session, "conv-3")
    assert sale.status == "confirmada"
    assert sale.product_id == product.id


def test_scheduler_job_health_tracks_success_and_failure():
    FacebookSchedulerService._run_job("sales_sync", lambda: None)
    health = FacebookSchedulerService.get_health()
    assert health["sales_sync"]["never_ran"] is False
    assert health["sales_sync"]["last_error"] is None

    def _boom():
        raise RuntimeError("falha simulada")

    FacebookSchedulerService._run_job("sales_sync", _boom)
    health = FacebookSchedulerService.get_health()
    assert health["sales_sync"]["last_error"] == "falha simulada"


def test_recalculate_all_boosts_product_with_only_real_sales(db_session):
    product = _make_product(db_session, item_id=888)

    sale = Sale(
        marketplace="shopee",
        conversion_id="conv-4",
        product_id=product.id,
        order_id="ORDER-4",
        order_status="completed",
        status="confirmada",
        total_commission=10.0,
        net_commission=9.0,
    )
    db_session.add(sale)
    db_session.commit()

    summary = ProductPerformanceScore.recalculate_all(db_session)

    assert summary["products_with_real_sales"] == 1
    db_session.refresh(product)
    assert product.performance_adjustment == ProductPerformanceScore.REAL_SALE_BONUS
    assert product.score > product.base_score
