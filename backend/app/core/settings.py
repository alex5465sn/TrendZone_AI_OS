from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "TrendZone AI OS"

    VERSION: str = "0.1.0"

    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"

    APP_BASE_URL: str = "http://127.0.0.1:8000"

    #################################
    # DATABASE
    #################################

    DATABASE_URL: str = "sqlite:///trendzone.db"

    #################################
    # JWT
    #################################

    SECRET_KEY: str = "trendzone-super-secret-key"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    #################################
    # LOGS
    #################################

    LOG_LEVEL: str = "INFO"

    #################################
    # SHOPEE
    #################################

    SHOPEE_GRAPHQL_URL: str = ""

    SHOPEE_APP_ID: str = ""

    SHOPEE_SECRET: str = ""

    SHOPEE_ACCESS_TOKEN: str = ""

    SHOPEE_REFRESH_TOKEN: str = ""

    #################################
    # FACEBOOK
    #################################

    FACEBOOK_PAGE_ID: str = ""

    FACEBOOK_PAGE_TOKEN: str = ""

    NTFY_TOPIC: str = ""

    #################################
    # ABACUS AI
    ABACUS_API_KEY: str = ""

    # WHATSAPP (WAHA)
    WAHA_URL: str = "http://localhost:3000"

    WAHA_API_KEY: str = ""

    # AI PROVIDERS
    OPENROUTER_API_KEY: str = ""

    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"

    # Liga/desliga a geração de legenda (hook/corpo/CTA) por IA nos posts
    # automáticos. Se desligado ou se a chamada falhar, usa os templates
    # prontos (sem custo de API). Desligado por padrão para não consumir
    # crédito do OpenRouter sem o usuário decidir ativar.
    AI_CONTENT_GENERATION_ENABLED: bool = False

    OPENAI_API_KEY: str = ""

    ANTHROPIC_API_KEY: str = ""

    #################################
    # CORS / URLS
    #################################

    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174,http://192.168.0.5:5173,http://192.168.0.5:8000,https://trend-zone-ai-os.vercel.app,https://app.trendzone.app,https://www.trendzone.app,https://api.trendzone.app"

    FRONTEND_URL: str = "http://127.0.0.1:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    #################################
    # ENV
    #################################

    model_config = SettingsConfigDict(

        env_file=(
            Path(__file__).resolve().parents[3] / ".env"
        ),

        extra="ignore",

    )


settings = Settings()