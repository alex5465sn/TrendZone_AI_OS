"""
Testes da nova automacao da tela "Produtos Shopee":

- IA classifica e adiciona automaticamente produtos PROMOVER ao banco
  (sem depender de clique manual no "+").
- Endpoint /marketplace/promote gera conteudo de divulgacao + link de
  rastreamento + opcoes de compartilhamento (WhatsApp/Facebook).
"""

import json

from app.api.marketplace import _score_and_classify, _auto_add_if_promoted, promote
from app.api.marketplace_schemas import PromoteRequest
from app.repositories.product_repository import ProductRepository


def _node(**overrides):
    node = {
        "itemId": 111,
        "shopId": 222,
        "productName": "Fone Bluetooth Top",
        "imageUrl": "https://img.example/1.png",
        "offerLink": "https://s.shopee.com.br/abc",
        "price": "99.90",
        "commissionRate": "0.80",
        "ratingStar": "4.9",
        "sales": 5000,
    }
    node.update(overrides)
    return node


def test_score_and_classify_promotes_high_quality_product():
    score, decision = _score_and_classify(_node())

    assert decision == "PROMOVER"
    assert score > 80


def test_score_and_classify_discards_weak_product():
    score, decision = _score_and_classify(
        _node(commissionRate="0.01", ratingStar="1.0", sales=0)
    )

    assert decision == "DESCARTAR"
    assert score < 40


def test_auto_add_if_promoted_creates_product_once(db_session):
    node = _node()
    score, decision = _score_and_classify(node)

    tracked = _auto_add_if_promoted(db_session, node, decision, score)
    assert tracked is True
    assert ProductRepository.get_by_item_id(db_session, node["itemId"]) is not None

    tracked_again = _auto_add_if_promoted(db_session, node, decision, score)
    assert tracked_again is True


def test_auto_add_if_promoted_skips_low_score_product(db_session):
    node = _node(itemId=333, commissionRate="0.01", ratingStar="1.0", sales=0)
    score, decision = _score_and_classify(node)

    tracked = _auto_add_if_promoted(db_session, node, decision, score)

    assert tracked is False
    assert ProductRepository.get_by_item_id(db_session, node["itemId"]) is None


def test_promote_returns_content_link_and_share_options(db_session):
    payload = PromoteRequest(
        item_id=111,
        product_name="Fone Bluetooth Top",
        price=99.90,
        commission_rate=0.20,
        rating_star=4.9,
        sales=5000,
        offer_link="https://s.shopee.com.br/abc",
    )

    response = promote(payload, db=db_session, current_user=None)
    body = json.loads(response.body)

    data = body["data"]
    assert data["tracking_url"]
    assert data["content"]["title"]
    assert data["full_text"]
    assert "wa.me" in data["whatsapp_share_url"]
    assert "facebook.com/sharer" in data["facebook_share_url"]
