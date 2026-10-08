from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.settings import settings
from app.core.exceptions import (
    TrendZoneException,
    trendzone_exception_handler,
    generic_exception_handler,
)

from app.database.base import Base
from app.database.session import engine
from app.database.migrations import run as run_migrations

from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.product import router as product_router
from app.api.scout import router as scout_router
from app.api.system_info import router as system_router
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router

from app.api.marketplace import router as marketplace_router
from app.api.admin import router as admin_router
from app.api.analytics import router as analytics_router
from app.api.opportunities import router as opportunities_router
from app.api.prospects import router as prospects_router
from app.api.sales import router as sales_router
from app.api.inspector import router as inspector_router
from app.api.marketplace_accounts import router as marketplace_accounts_router
from app.api.facebook import router as facebook_router
from app.api.shopee_video import router as shopee_video_router
from app.api.scheduled_posts import router as scheduled_posts_router
from app.api.published_posts import router as tracking_router, public_router as tracking_public_router
from app.api.admin_seed import router as admin_seed_router
from app.commercial_intelligence.api.commercial_intelligence import router as commercial_intelligence_router
from app.api.funnel import router as funnel_router
from app.api.content_strategy import router as content_strategy_router
from app.api.mercadolivre import router as mercadolivre_router
from app.api.follow_up import router as follow_up_router
from app.api.channel_tracking import router as channel_tracking_router
from app.api.seasonal import router as seasonal_router
from app.api.discovery import router as discovery_router
from app.api.automation import router as automation_router
from app.api.audit_log import router as audit_log_router
from app.api.vocabulary import router as vocabulary_router
from app.api.whatsapp import router as whatsapp_router
from app.api.ai_agent import router as ai_agent_router
from app.api.divulgation_groups import router as divulgation_groups_router
from app.api.first_sale_plan import router as first_sale_plan_router
from app.api.notifications import router as notifications_router

from app.services.auto_publisher_service import AutoPublisherService
from app.services.facebook_scheduler_service import FacebookSchedulerService
from app.services.auto_scout_service import AutoScoutService
from app.services.video_generator import MEDIA_DIR

# ============================
# NOVA API SHOPEE
# ============================

from app.routes import (
    shopee_router,
)


# =====================================================
# Startup / Shutdown
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\n========================================")
    print(settings.APP_NAME)
    print("Inicializando Backend...")
    print("========================================\n")

    run_migrations(engine)

    Base.metadata.create_all(bind=engine)

    print("[ORQUESTRADOR] Iniciando servicos de background...")
    AutoPublisherService.start()
    print("[ORQUESTRADOR] AutoPublisher: OK")
    FacebookSchedulerService.start()
    print("[ORQUESTRADOR] FacebookScheduler: OK")
    AutoScoutService.start()
    print("[ORQUESTRADOR] AutoScout: OK")
    print("[ORQUESTRADOR] Todos os servicos iniciados. Backend pronto.")

    yield

    print("[ORQUESTRADOR] Encerrando servicos...")
    AutoPublisherService.stop()
    FacebookSchedulerService.stop()
    AutoScoutService.stop()

    print("\n========================================")
    print("Backend encerrado.")
    print("========================================\n")


# =====================================================
# Aplicação
# =====================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)


# =====================================================
# Exception Handler
# =====================================================

app.add_exception_handler(
    TrendZoneException,
    trendzone_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)


# =====================================================
# CORS
# =====================================================

origins = settings.cors_origin_list

app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


# =====================================================
# Rotas
# =====================================================

app.include_router(auth_router)

app.include_router(user_router)

app.include_router(product_router)

app.include_router(scout_router)

app.include_router(system_router)

app.include_router(dashboard_router)

app.include_router(health_router)

app.include_router(marketplace_router)

app.include_router(admin_router)

app.include_router(analytics_router)

app.include_router(opportunities_router)

app.include_router(prospects_router)

app.include_router(sales_router)

app.include_router(inspector_router)

app.include_router(marketplace_accounts_router)

app.include_router(mercadolivre_router)

app.include_router(facebook_router)
app.include_router(shopee_video_router)

app.include_router(scheduled_posts_router)

app.include_router(tracking_router)

app.include_router(tracking_public_router)

app.include_router(admin_seed_router)

app.include_router(commercial_intelligence_router)

app.include_router(funnel_router)

app.include_router(content_strategy_router)

app.include_router(follow_up_router)

app.include_router(channel_tracking_router)

app.include_router(seasonal_router)

app.include_router(discovery_router)

app.include_router(automation_router)

app.include_router(audit_log_router)

app.include_router(vocabulary_router)

app.include_router(whatsapp_router)

app.include_router(ai_agent_router)
app.include_router(divulgation_groups_router)
app.include_router(first_sale_plan_router)
app.include_router(notifications_router)

app.mount("/media", StaticFiles(directory=str(MEDIA_DIR.parent)), name="media")

# ============================
# Shopee Affiliate API
# ============================

app.include_router(
    shopee_router,
)


# =====================================================
# Home
# =====================================================

@app.get("/", tags=["System"])
def home():

    return {

        "status": "online",

        "application": settings.APP_NAME,

        "version": settings.VERSION,

        "docs": "/docs",

    }