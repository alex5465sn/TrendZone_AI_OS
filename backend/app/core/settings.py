from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "TrendZone AI OS"

    VERSION: str = "0.1.0"

    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"

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
    # ENV
    #################################

    model_config = SettingsConfigDict(

        env_file=(
            Path(__file__).resolve().parents[3] / ".env"
        ),

        extra="ignore",

    )


settings = Settings()