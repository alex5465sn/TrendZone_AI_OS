"""
TrendZone AI OS
================================

Scout API

Responsável por iniciar o Pipeline
completo de inteligência.
"""

from fastapi import APIRouter

from app.api.response import ResponseBuilder

from app.tasks.runner import Runner

router = APIRouter(

    prefix="/scout",

    tags=["Scout"],

)


@router.post("/run")
def execute_pipeline():

    runner = Runner()

    result = runner.execute()

    return ResponseBuilder.success(

        data=result,

        message="Pipeline executado.",

    )


@router.get("/status")
def status():

    return ResponseBuilder.success(

        data={

            "pipeline": "READY",

            "agents": 5,

            "tasks": 11,

        }

    )