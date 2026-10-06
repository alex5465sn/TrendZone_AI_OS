"""
TrendZone AI OS
================================

Camada Repository.

Responsável exclusivamente pelo acesso
aos dados persistidos.

Nunca coloque regras de negócio aqui.

Fluxo correto:

API
 ↓
Service
 ↓
Repository
 ↓
Database
"""

from app.repositories.base_repository import BaseRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.system_info_repository import SystemInfoRepository
from app.repositories.user_repository import UserRepository
from app.repositories.campaign_repository import CampaignRepository
from app.repositories.divulgation_group_repository import DivulgationGroupRepository
from app.repositories.first_sale_plan_repository import FirstSalePlanRepository
from app.repositories.notification_repository import NotificationRepository
from app.repositories.prospect_repository import ProspectRepository
from app.repositories.published_post_repository import PublishedPostRepository
from app.repositories.sale_repository import SaleRepository
from app.repositories.schedule_repository import ScheduleRepository
from app.repositories.scheduled_post_repository import ScheduledPostRepository
from app.repositories.trend_product_repository import TrendProductRepository

__all__ = (
    "BaseRepository",
    "ProductRepository",
    "SystemInfoRepository",
    "UserRepository",
    "CampaignRepository",
    "DivulgationGroupRepository",
    "FirstSalePlanRepository",
    "NotificationRepository",
    "ProspectRepository",
    "PublishedPostRepository",
    "SaleRepository",
    "ScheduleRepository",
    "ScheduledPostRepository",
    "TrendProductRepository",
)