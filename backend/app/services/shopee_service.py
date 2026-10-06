"""
TrendZone AI OS
================================

Shopee Service.

Camada responsável por toda comunicação
entre o sistema e a integração Shopee.

Nenhum Controller deve acessar
ShopeeGateway diretamente.
"""

from app.services.base_service import BaseService

from app.integrations.shopee.gateway import ShopeeGateway

from app.integrations.shopee.graphql.products import (
    PRODUCT_OFFER_V2,
)

from app.integrations.shopee.graphql.campaigns import (
    SHOP_OFFER_V2,
)

from app.integrations.shopee.graphql.reports import (
    CONVERSION_REPORT,
)


class ShopeeService(BaseService):

    SERVICE_NAME = "SHOPEE_SERVICE"

    def __init__(
        self,
        gateway: ShopeeGateway,
    ):

        self.gateway = gateway

    # ==========================================
    # PRODUTOS
    # ==========================================

    def product_offers(
        self,
        variables: dict,
    ):

        self.log_info(
            "Consultando ProductOfferV2..."
        )

        return self.gateway.execute(
            PRODUCT_OFFER_V2,
            variables,
        )

    # ==========================================
    # CAMPANHAS
    # ==========================================

    def shop_offers(
        self,
        variables: dict,
    ):

        self.log_info(
            "Consultando ShopOfferV2..."
        )

        return self.gateway.execute(
            SHOP_OFFER_V2,
            variables,
        )

    # ==========================================
    # CONVERSÕES
    # ==========================================

    def conversion_report(
        self,
        variables: dict,
    ):

        self.log_info(
            "Consultando ConversionReport..."
        )

        return self.gateway.execute(
            CONVERSION_REPORT,
            variables,
        )