"""
TrendZone AI OS — Auto Scout Service

Roda em segundo plano dentro do backend e varre
periodicamente uma rotacao de palavras-chave reais
(mesmas categorias usadas na tela de Prospeccao),
alimentando a tabela "products" automaticamente.

Varre TODOS os marketplaces configurados (Shopee e
Mercado Livre), alternando entre eles a cada ciclo
para manter o catalogo equilibrado.
"""

import asyncio

from app.core.logger import logger
from app.database.session import SessionLocal
from app.services.scout_service import ScoutService
from app.services.marketplace_service import MarketplaceBusiness
from app.constants.categories import get_keyword_rotation
from app.repositories.product_repository import ProductRepository
from app.models.product import Product
from app.schemas.product import ProductCreate

CHECK_INTERVAL_SECONDS = 15 * 60

KEYWORD_ROTATION = get_keyword_rotation()

MARKETPLACES = ["shopee", "mercado_livre"]


class AutoScoutService:

    _task: asyncio.Task | None = None
    _running = False
    _index = 0
    _mp_index = 0

    @classmethod
    def start(cls):
        if cls._running:
            return
        cls._running = True
        cls._task = asyncio.create_task(cls._loop())
        logger.info("[AUTO_SCOUT] Servico multi-marketplace iniciado.")

    @classmethod
    def stop(cls):
        cls._running = False
        if cls._task:
            cls._task.cancel()
        logger.info("[AUTO_SCOUT] Servico parado.")

    @classmethod
    async def _loop(cls):
        while cls._running:
            try:
                cls._run_once()
            except Exception as e:
                logger.warning(f"[AUTO_SCOUT] Erro no ciclo: {e}")
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)

    @classmethod
    def _run_once(cls):
        category_id, keyword = KEYWORD_ROTATION[cls._index % len(KEYWORD_ROTATION)]
        marketplace = MARKETPLACES[cls._mp_index % len(MARKETPLACES)]
        cls._index += 1
        cls._mp_index += 1

        db = SessionLocal()
        try:
            if marketplace == "shopee":
                reports = ScoutService(db).search_products(keyword=keyword, page=1, limit=10)
                count = len(reports)
            else:
                service = MarketplaceBusiness()
                data = service.search_products(
                    marketplace_name=marketplace,
                    keyword=keyword,
                    page=1,
                    limit=10,
                )
                count = 0
                for node in data.get("nodes", []):
                    existing = ProductRepository.get_by_item_id(db, node["itemId"])
                    if existing:
                        continue
                    try:
                        from app.services.product_service import ProductService
                        ProductService.create(
                            db,
                            ProductCreate(
                                marketplace=node.get("marketplace", marketplace),
                                item_id=node["itemId"],
                                shop_id=node.get("shopId", 0),
                                category="geral",
                                name=node["productName"],
                                price=node.get("price", 0),
                                commission=float(node.get("commissionRate") or 0) * 100,
                                image=node.get("imageUrl", ""),
                                offer_link=node.get("offerLink", ""),
                                rating=float(node.get("ratingStar") or 0),
                                sales=int(node.get("sales") or 0),
                            ),
                        )
                        count += 1
                    except Exception:
                        pass

            db.commit()
            logger.info(
                f"[AUTO_SCOUT] [{marketplace.upper()}] "
                f"Categoria '{category_id}' / palavra-chave '{keyword}': "
                f"{count} produto(s) processado(s)."
            )
        except Exception as e:
            db.rollback()
            logger.warning(
                f"[AUTO_SCOUT] [{marketplace.upper()}] "
                f"Falha ao varrer '{keyword}': {e}"
            )
        finally:
            db.close()
