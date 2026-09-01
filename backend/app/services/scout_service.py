"""
TrendZone AI OS
================================

Scout Service

Camada de orquestração do Scout.
"""

from sqlalchemy.orm import Session

from app.pipelines.scout_pipeline import (
    ScoutPipeline,
)

from app.services.base_service import BaseService


class ScoutService(BaseService):

    SERVICE_NAME = "SCOUT_SERVICE"

    def __init__(

        self,

        db: Session,

    ):

        self.pipeline = ScoutPipeline(db)

    def search_products(

        self,

        keyword: str = "",

        page: int = 1,

        limit: int = 20,

    ):

        self.log_info(

            "Executando Scout Pipeline..."

        )

        reports = self.pipeline.run(

            keyword,

            page,

            limit,

        )

        self.log_success(

            f"{len(reports)} relatório(s) gerado(s)."

        )

        return reports