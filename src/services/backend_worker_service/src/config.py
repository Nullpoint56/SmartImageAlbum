from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from shared.config.object_store import ObjectStoreSettings
from shared.config.embedder import EmbedderClientSettings
from shared.config.vector_db import VectorDBSettings
from shared.config.db import DBSettings


class WorkerConfig(BaseSettings):
    celery_broker_url: Optional[str] = Field(None, alias="CELERY_BROKER_URL")
    object_store: ObjectStoreSettings
    embedder_client: EmbedderClientSettings
    vector_db: VectorDBSettings
    db: DBSettings

    model_config = SettingsConfigDict(
        env_file="app/app.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__"
    )