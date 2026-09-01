from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.core.exceptions import (
    TrendZoneException,
    trendzone_exception_handler,
    generic_exception_handler,
)

from app.database.base import Base
from app.database.session import engine

from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.product import router as product_router
from app.api.scout import router as scout_router
from app.api.system_info import router as system_router
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router
from app.api.pipeline import router as pipeline_router
from app.api.marketplace import router as marketplace_router
from app.api.admin import router as admin_router
from app.api.analytics import router as analytics_router

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

    Base.metadata.create_all(bind=engine)

    yield

    print("\n========================================")
    print("Encerrando Backend...")
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

origins = [

    "http://localhost:5173",

    "http://127.0.0.1:5173",

    "http://localhost:5174",

    "http://127.0.0.1:5174",

]

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

app.include_router(pipeline_router)

app.include_router(marketplace_router)

app.include_router(admin_router)

app.include_router(analytics_router)

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