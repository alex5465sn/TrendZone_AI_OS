"""
TrendZone AI OS

Camada de Services.

Toda regra de negócio do sistema
deve ser acessada através desta
camada.

Nunca utilize Repositories
diretamente nas APIs.
"""

from app.services.base_service import BaseService

from app.services.product_service import ProductService
from app.services.user_service import UserService
from app.services.system_info_service import SystemInfoService

from app.services.product_validator import ProductValidator
from app.services.product_score import ProductScore

from app.services.decision_engine import DecisionEngine
from app.services.executive_report import ExecutiveReport

from app.services.scout_service import ScoutService
from app.services.ranking_engine import RankingEngine
from app.services.marketplace_service import MarketplaceBusiness

__all__ = [

    "BaseService",

    "ProductService",
    "UserService",
    "SystemInfoService",

    "ProductValidator",
    "ProductScore",

    "DecisionEngine",
    "ExecutiveReport",

    "ScoutService",
    "RankingEngine",
    "MarketplaceBusiness",
]