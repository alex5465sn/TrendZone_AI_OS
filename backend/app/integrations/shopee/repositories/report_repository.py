from app.integrations.shopee.services.report_service import ReportService


class ReportRepository:
    """
    Repositório responsável pelos
    relatórios da Shopee.
    """

    def __init__(
        self,
        service: ReportService,
    ):
        self.service = service

    def conversion_report(
        self,
        variables: dict,
    ):
        return self.service.conversion_report(
            **variables
        )

    def validated_report(
        self,
        variables: dict,
    ):
        return self.service.validated_report(
            **variables
        )