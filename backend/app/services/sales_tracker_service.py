"""
TrendZone AI OS — Sales Tracker Service

Consulta a Shopee Affiliate API (ConversionReport)
para buscar vendas/conversoes reais e salva no banco.

Tambem gera links curtos de afiliado via Shopee
para rastreamento de campanhas.
"""

import time
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.integrations.shopee.client import ShopeeClient
from app.integrations.shopee.graphql.reports import CONVERSION_REPORT
from app.integrations.shopee.graphql.links import GENERATE_SHORT_LINK


class SalesTrackerService:

    @staticmethod
    def fetch_conversions(
        days_back: int = 7,
        limit: int = 50,
        credentials: dict | None = None,
    ) -> list[dict[str, Any]]:

        client = ShopeeClient(
            app_id=(credentials or {}).get("app_id"),
            secret=(credentials or {}).get("secret"),
        )

        now = int(time.time())
        start = now - (days_back * 86400)

        all_nodes: list[dict] = []
        scroll_id = None
        has_next = True

        while has_next:
            variables: dict[str, Any] = {
                "purchaseTimeStart": str(start),
                "purchaseTimeEnd": str(now),
                "limit": limit,
                "scrollId": scroll_id,
            }

            try:
                result = client.execute(
                    query=CONVERSION_REPORT,
                    variables=variables,
                )
            except Exception as e:
                logger.warning(f"[SALES_TRACKER] Erro ao consultar Shopee: {e}")
                break

            data = (result.get("data") or {}).get("conversionReport") or {}
            nodes = data.get("nodes") or []
            page_info = data.get("pageInfo") or {}

            all_nodes.extend(nodes)

            has_next = page_info.get("hasNextPage", False)
            scroll_id = page_info.get("scrollId")

            if not has_next or not scroll_id:
                break

        return all_nodes

    @staticmethod
    def parse_conversion(node: dict) -> dict:
        orders = node.get("orders") or []
        first_order = orders[0] if orders else {}

        return {
            "conversion_id": str(node.get("conversionId", "")),
            "order_id": str(first_order.get("orderId", "")),
            "order_status": first_order.get("orderStatus", ""),
            "shop_type": first_order.get("shopType", ""),
            "buyer_type": node.get("buyerType", ""),
            "device": node.get("device", ""),
            "product_type": node.get("productType", ""),
            "click_time": str(node.get("clickTime", "")),
            "purchase_time": str(node.get("purchaseTime", "")),
            "total_commission": float(node.get("totalCommission") or 0),
            "seller_commission": float(node.get("sellerCommission") or 0),
            "shopee_commission": float(node.get("shopeeCommissionCapped") or 0),
            "net_commission": float(node.get("netCommission") or 0),
            "utm_content": node.get("utmContent", ""),
        }

    @staticmethod
    def sync_and_persist(
        db: Session,
        days_back: int = 7,
        credentials: dict | None = None,
        user_id: int | None = None,
    ) -> dict:
        """
        Busca conversoes na Shopee e persiste na tabela "sales",
        tentando casar cada conversao com um produto conhecido
        (via utm_content = item_id, atribuido no link de divulgacao).

        Usado tanto pelo endpoint manual (POST /sales/sync) quanto
        pelo job periodico do FacebookSchedulerService, para que as
        duas rotas de sincronizacao nunca divirjam em comportamento.
        """
        from app.models.sale import Sale
        from app.repositories.sale_repository import SaleRepository
        from app.repositories.product_repository import ProductRepository

        nodes = SalesTrackerService.fetch_conversions(
            days_back=days_back,
            credentials=credentials,
        )

        new_count = 0
        updated_count = 0

        for node in nodes:
            parsed = SalesTrackerService.parse_conversion(node)
            existing = SaleRepository.get_by_conversion_id(db, parsed["conversion_id"])

            product_id = None
            try:
                item_id = int(parsed["utm_content"])
                product = ProductRepository.get_by_item_id(db, item_id)
                product_id = product.id if product else None
            except (TypeError, ValueError):
                product_id = None

            status = "pendente"
            if parsed["order_status"] in ("completed", "settled"):
                status = "confirmada"
            elif parsed["order_status"] in ("cancelled", "refunded"):
                status = "cancelada"

            if existing:
                if existing.user_id is None:
                    existing.user_id = user_id
                if existing.product_id is None:
                    existing.product_id = product_id

                existing.order_status = parsed["order_status"]
                existing.total_commission = parsed["total_commission"]
                existing.net_commission = parsed["net_commission"]
                existing.seller_commission = parsed["seller_commission"]
                existing.shopee_commission = parsed["shopee_commission"]
                existing.status = status
                existing.updated_at = datetime.utcnow()

                SaleRepository.update(db, existing)
                updated_count += 1
            else:
                sale = Sale(
                    conversion_id=parsed["conversion_id"],
                    user_id=user_id,
                    product_id=product_id,
                    order_id=parsed["order_id"],
                    order_status=parsed["order_status"],
                    shop_type=parsed["shop_type"],
                    buyer_type=parsed["buyer_type"],
                    device=parsed["device"],
                    product_type=parsed["product_type"],
                    click_time=parsed["click_time"],
                    purchase_time=parsed["purchase_time"],
                    total_commission=parsed["total_commission"],
                    seller_commission=parsed["seller_commission"],
                    shopee_commission=parsed["shopee_commission"],
                    net_commission=parsed["net_commission"],
                    utm_content=parsed["utm_content"],
                    status=status,
                )
                SaleRepository.create(db, sale)
                new_count += 1

        return {
            "synced_from_shopee": len(nodes),
            "new_sales": new_count,
            "updated_sales": updated_count,
        }

    @staticmethod
    def generate_tracking_link(
        origin_url: str,
        sub_ids: list[str] | None = None,
        credentials: dict | None = None,
    ) -> dict:
        client = ShopeeClient(
            app_id=(credentials or {}).get("app_id"),
            secret=(credentials or {}).get("secret"),
        )

        variables: dict[str, Any] = {
            "originUrl": origin_url,
            "subIds": sub_ids or [],
        }

        try:
            result = client.execute(
                query=GENERATE_SHORT_LINK,
                variables=variables,
            )
            data = (result.get("data") or {}).get("generateShortLink") or {}
            return {
                "short_link": data.get("shortLink", ""),
                "long_link": data.get("longLink", ""),
            }
        except Exception as e:
            logger.warning(f"[SALES_TRACKER] Erro ao gerar link: {e}")
            return {"short_link": "", "long_link": "", "error": str(e)}


def run_sales_sync(days_back: int = 3) -> dict:
    """
    Ponto de entrada usado pelo FacebookSchedulerService para
    sincronizar vendas/conversoes reais da Shopee periodicamente,
    sem exigir chamada manual de POST /sales/sync.

    Sem isso, nenhuma venda real chega ao banco: o endpoint existe
    mas nunca e chamado por ninguem (bug corrigido em 2026-10).
    """
    from app.database.session import SessionLocal

    db = SessionLocal()
    try:
        result = SalesTrackerService.sync_and_persist(db, days_back=days_back)
        if result["new_sales"] or result["updated_sales"]:
            logger.info(
                "[SALES_TRACKER] Sincronizacao periodica: "
                f"{result['new_sales']} nova(s), {result['updated_sales']} atualizada(s) "
                f"de {result['synced_from_shopee']} conversao(oes) na Shopee."
            )
        return result
    except Exception as e:
        logger.warning(f"[SALES_TRACKER] Erro na sincronizacao periodica: {e}")
        return {"error": str(e)}
    finally:
        db.close()
