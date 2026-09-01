"""
TrendZone AI OS
================================

API Package

Centraliza todas as APIs
da aplicação.

Nunca importe endpoints
individualmente.
"""

from app.api.router import api_router

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.product import router as product_router
from app.api.user import router as user_router
from app.api.scout import router as scout_router
from app.api.dashboard import router as dashboard_router
from app.api.pipeline import router as pipeline_router
from app.api.system_info import router as system_router


api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(product_router)
api_router.include_router(user_router)
api_router.include_router(scout_router)
api_router.include_router(dashboard_router)
api_router.include_router(pipeline_router)
api_router.include_router(system_router)


__all__ = [

    "api_router",

]