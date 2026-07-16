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
    # ENV
    #################################

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()