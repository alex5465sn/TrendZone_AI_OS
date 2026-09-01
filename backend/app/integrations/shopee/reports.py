from datetime import datetime

from app.integrations.shopee.gateway import ShopeeGateway


class ShopeeReports:
    """
    Operações relacionadas aos relatórios
    da Shopee Affiliate.
    """

    def __init__(
        self,
        gateway: ShopeeGateway,
    ):
        self.gateway = gateway

    def get_conversion_report(
        self,
        start_time: datetime,
        end_time: datetime,
    ):

        variables = {
            "startTime": start_time.isoformat(),
            "endTime": end_time.isoformat(),
        }

        return self.gateway.execute(
            query="",
            variables=variables,
        )