"""
TrendZone AI OS
================================

Report Service.
"""

from app.integrations.shopee.graphql.repository import (
    GraphQLRepository,
)


class ReportService:

    def __init__(
        self,
        access_token: str | None = None,
    ):

        self.repository = GraphQLRepository(
            access_token=access_token,
        )

    # =====================================================
    # CONVERSION REPORT
    # =====================================================

    def conversion_report(
        self,
        **filters,
    ):

        variables = self._int64_to_string(
            filters,
            (
                "purchaseTimeStart",
                "purchaseTimeEnd",
                "completeTimeStart",
                "completeTimeEnd",
            ),
        )

        return self.repository.conversion_report(
            variables
        )

    # =====================================================
    # VALIDATED REPORT
    # =====================================================

    def validated_report(
        self,
        **filters,
    ):

        variables = self._int64_to_string(
            filters,
            (
                "validationId",
            ),
        )

        return self.repository.validated_report(
            variables
        )

    # =====================================================
    # HELPERS
    # =====================================================

    @staticmethod
    def _int64_to_string(
        filters: dict,
        fields: tuple,
    ) -> dict:

        variables = dict(filters)

        for field in fields:

            value = variables.get(field)

            if value is not None:

                variables[field] = str(value)

        return variables