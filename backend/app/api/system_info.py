"""
TrendZone AI OS
================================

System Information API

Informações administrativas
do sistema.
"""

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.api.response import ResponseBuilder

from app.services.system_info_service import SystemInfoService

router = APIRouter(

    prefix="/system",

    tags=["System"],

)


@router.get("")
def system_info(

    db: Session = Depends(get_db),

):

    info = SystemInfoService.get_first(db)

    if info is None:

        return ResponseBuilder.error(

            message="Informações do sistema não cadastradas.",

            status_code=404,

        )

    return ResponseBuilder.success(

        data={

            "app_name": info.app_name,

            "version": info.version,

            "status": info.status,

        }

    )