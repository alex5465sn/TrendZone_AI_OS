"""
TrendZone AI OS — Sales Tracker Service

Consulta a Shopee Affiliate API (ConversionReport)
para buscar vendas/conversoes reais e salva no banco.

Tambem gera links curtos de afiliado via Shopee
para rastreamento de campanhas.
"""

import time
import logging
from typing import Any

from app.integrations.shopee.client import ShopeeClient
from app.integrations.shopee.graphql.reports import CONVERSION_REPORT
from app.integrations.shopee.graphql.links import GENERATE_SHORT_LINK

logger = logging.getLogger("trendzone")


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
