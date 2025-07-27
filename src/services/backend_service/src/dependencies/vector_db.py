from qdrant_client import AsyncQdrantClient

from config.app import get_app_config


async def get_vector_db_client() -> AsyncQdrantClient:
    config = get_app_config()
    settings = config.vector_db
    return AsyncQdrantClient(
        host=settings.host,
        port=settings.port,
    )
