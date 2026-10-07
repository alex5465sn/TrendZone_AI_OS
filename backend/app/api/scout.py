"""
TrendZone AI OS
================================

Scout API

Responsável por iniciar o Pipeline
completo de inteligência.
"""

from fastapi import APIRouter, Depends

from app.api.response import ResponseBuilder
from app.dependencies import get_admin_user
from app.models.user import User

from app.tasks.runner import Runner

router = APIRouter(

    prefix="/scout",

    tags=["Scout"],

)


@router.post("/run")
def execute_pipeline(current_user: User = Depends(get_admin_user)):

    runner = Runner()

    result = runner.execute()

    return ResponseBuilder.success(

        data=result,

        message="Pipeline executado.",

    )


@router.get("/status")
def status(current_user: User = Depends(get_admin_user)):

    return ResponseBuilder.success(

        data={

            "pipeline": "READY",

            "agents": 5,

            "tasks": 11,

        }

    )