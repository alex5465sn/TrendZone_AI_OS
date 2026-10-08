"""
TrendZone AI OS
================================

Dashboard API

Fornece métricas gerais do sistema.
"""

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.product_service import ProductService

from app.api.response import ResponseBuilder

router = APIRouter(

    prefix="/dashboard",

    tags=["Dashboard"],

)


@router.get("")
def dashboard(

    db: Session = Depends(get_db),

):

    statistics = ProductService.statistics(db)

    return ResponseBuilder.success(

        data={

            **statistics,

            "version": "2.0",

            "status": "online",

            "pipeline": "READY",

        }

    )