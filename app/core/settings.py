from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Smart Haram Monitoring System"
    APP_ENV: str = "development"
    API_PREFIX: str = "/api"

    MODEL_PATH: str = "app/models/haram_smart_detection.keras"
    MODEL_INPUT_SIZE: int = 64

    FIREBASE_SERVICE_ACCOUNT_PATH: str = "./firebase-service-account.json"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()