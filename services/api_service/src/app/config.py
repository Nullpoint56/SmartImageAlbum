from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application configuration pulled from environment variables."""

    # MinIO (Object Storage)
    MINIO_ENDPOINT: str = Field(..., description="MinIO endpoint like 'minio:9000'")
    MINIO_ACCESS_KEY: str = Field(..., description="MinIO access key")
    MINIO_SECRET_KEY: str = Field(..., description="MinIO secret key")

    # Redis (Arq)
    REDIS_URL: str = Field(..., description="Redis connection string like 'redis://localhost:6379'")

    # Qdrant (Vector DB)
    QDRANT_HOST: str = Field(..., description="Qdrant host, e.g. 'qdrant'")
    QDRANT_PORT: int = Field(6333, description="Qdrant port, typically 6333")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
