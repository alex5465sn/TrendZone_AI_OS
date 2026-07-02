from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "TrendZone AI OS"

    VERSION: str = "0.0.1"

    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"


settings = Settings()