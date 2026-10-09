"""
TrendZone AI OS
===============================

Models Oficiais da Aplicação.

Este módulo centraliza a exportação de todos
os Models SQLAlchemy utilizados pelo sistema.

Sempre importe os Models através deste package,
evitando importações diretas dos arquivos.

Exemplo:

from app.models import Product
from app.models import User

Nunca:

from app.models.product import Product
"""

from app.models.product import Product
from app.models.system_info import SystemInfo
from app.models.user import User
from app.models.campaign import Campaign
from app.models.prospect import Prospect
from app.models.schedule import Schedule
from app.models.sale import Sale
from app.models.marketplace_account import MarketplaceAccount
from app.models.scheduled_post import ScheduledPost
from app.models.published_post import PublishedPost
from app.models.funnel import FunnelStage, FunnelCard
from app.models.content_strategy import ContentStrategy
from app.models.follow_up import FollowUp
from app.models.channel_tracking import ChannelTracking
from app.models.seasonal_event import SeasonalEvent
from app.models.automation_rule import AutomationRule
from app.models.audit_log import AuditLog
from app.models.niche_vocabulary import NicheVocabulary
from app.models.whatsapp import WhatsAppConnection, WhatsAppMessage
from app.models.ai_agent_config import AIAgentConfig
from app.models.divulgation_group import DivulgationGroup
from app.models.first_sale_plan import FirstSalePlan
from app.models.notification import Notification
from app.models.product_snapshot import ProductSnapshot

__all__ = (
    "Product",
    "ProductSnapshot",
    "SystemInfo",
    "User",
    "Campaign",
    "Prospect",
    "Schedule",
    "Sale",
    "MarketplaceAccount",
    "ScheduledPost",
    "PublishedPost",
    "FunnelStage",
    "FunnelCard",
    "ContentStrategy",
    "FollowUp",
    "ChannelTracking",
    "SeasonalEvent",
    "AutomationRule",
    "AuditLog",
    "NicheVocabulary",
    "WhatsAppConnection",
    "WhatsAppMessage",
    "AIAgentConfig",
    "DivulgationGroup",
    "FirstSalePlan",
    "Notification",
)