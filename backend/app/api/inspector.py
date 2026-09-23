"""
TrendZone AI OS — Inspector API

Endpoints do Inspetor Automatico da Plataforma.
Varre codigo, imports, banco, logs e .env,
reportando problemas com arquivo + linha + severidade.
"""

from fastapi import APIRouter, Depends

from app.dependencies import get_admin_user
from app.models.user import User
from app.services.inspector_service import InspectorService
from app.api.response import ResponseBuilder

router = APIRouter(prefix="/inspector", tags=["Inspector"])


@router.get("/full")
def full_inspection(
    current_user: User = Depends(get_admin_user),
):
    results = InspectorService.full_inspection()

    errors = [r for r in results if r["severity"] == "error"]
    warnings = [r for r in results if r["severity"] == "warning"]
    info = [r for r in results if r["severity"] == "info"]

    return ResponseBuilder.success(
        data={
            "total_checks": len(results),
            "errors": len(errors),
            "warnings": len(warnings),
            "info": len(info),
            "status": "OK" if not errors else "PROBLEMAS ENCONTRADOS",
            "results": results,
        },
    )


@router.get("/syntax")
def check_syntax(current_user: User = Depends(get_admin_user)):
    return ResponseBuilder.success(data=InspectorService.check_python_syntax())


@router.get("/imports")
def check_imports(current_user: User = Depends(get_admin_user)):
    return ResponseBuilder.success(data=InspectorService.check_imports())


@router.get("/models")
def check_models(current_user: User = Depends(get_admin_user)):
    return ResponseBuilder.success(data=InspectorService.check_models_registered())


@router.get("/routes")
def check_routes(current_user: User = Depends(get_admin_user)):
    return ResponseBuilder.success(data=InspectorService.check_routes_registered())


@router.get("/env")
def check_env(current_user: User = Depends(get_admin_user)):
    return ResponseBuilder.success(data=InspectorService.check_env_vars())


@router.get("/database")
def check_database(current_user: User = Depends(get_admin_user)):
    return ResponseBuilder.success(data=InspectorService.check_database())


@router.get("/logs")
def check_logs(current_user: User = Depends(get_admin_user)):
    return ResponseBuilder.success(data=InspectorService.check_logs())
