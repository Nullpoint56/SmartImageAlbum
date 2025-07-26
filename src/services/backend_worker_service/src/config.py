from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, AnyUrl


class WorkerConfig(BaseSettings):
    # Celery
    celery_broker_url: Optional[str] = Field(None, alias="CELERY_BROKER_URL")

    # MinIO
    minio_endpoint: Optional[str] = None
    minio_access_key: Optional[str] = None
    minio_secret_key: Optional[str] = None
    minio_secure: bool = Field(False)

    # Embedder
    embedder_base_url: Optional[AnyUrl] = None

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_https: bool = False

    # Database
    app_database_url: Optional[AnyUrl] = Field(None, alias="DB__APP_DATABASE_URL")

    class Config:
        env_file = ".env"
        case_sensitive = False
