from functools import lru_cache
from minio import Minio
from backend_service.config.app import get_app_config


@lru_cache()
def get_object_store_client() -> Minio:
    """
    Initializes and returns a cached MinIO client using settings from AppConfig.

    Returns:
        Minio: Configured and reusable MinIO client instance.
    """
    config = get_app_config()
    settings = config.object_store

    return Minio(
        endpoint=settings.endpoint,
        access_key=settings.access_key,
        secret_key=settings.secret_key,
        secure=settings.secure,
    )
