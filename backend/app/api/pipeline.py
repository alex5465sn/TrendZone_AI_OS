"""
TrendZone AI OS
================================

Pipeline API

Executa Pipelines completos
do sistema.

Enterprise Version.
"""

from fastapi import APIRouter

from app.api.response import ResponseBuilder

from app.tasks.runner import Runner

router = APIRouter(

    prefix="/pipeline",

    tags=["Pipeline"],

)


@router.post("/run")
def run_pipeline():

    runner = Runner()

    result = runner.execute()

    return ResponseBuilder.success(

        message="Pipeline executado com sucesso.",

        data=result,

    )


@router.get("/health")
def pipeline_health():

    return ResponseBuilder.success(

        data={

            "pipeline": "READY",

            "runner": "ONLINE",

            "scheduler": "READY",

            "monitor": "READY",

        }

    )