from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from shared.config.db import DBSettings
from config.logger import LoggerSettings
from shared.config.object_store import ObjectStoreSettings
from shared.config.vector_db import VectorDBSettings


class AppConfig(BaseSettings):
    db: DBSettings
    logger: LoggerSettings = Field(default=LoggerSettings())
    object_store: ObjectStoreSettings
    vector_db: VectorDBSettings
    celery_broker_url: Optional[str] = Field(None, alias="CELERY_BROKER_URL")

    model_config = SettingsConfigDict(
        env_file="app/app.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__"
    )

def get_app_config() -> AppConfig:
    return AppConfig()
