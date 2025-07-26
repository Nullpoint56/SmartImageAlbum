from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from backend_service.config.db import DBSettings
from backend_service.config.logger import LoggerSettings


class AppConfig(BaseSettings):
    db: DBSettings
    logger: LoggerSettings
    # object_store: ObjectStoreSettings

    model_config = SettingsConfigDict(
        env_file="app/app.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__"
    )

@lru_cache()
def get_app_config() -> AppConfig:
    return AppConfig()
