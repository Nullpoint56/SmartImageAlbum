from qdrant_client import QdrantClient

from backend_service.config.vector_db import VectorDBConfig


def get_vector_db_client(config: VectorDBConfig) -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            host=config.host,
            port=config.port,
        )
    return _qdrant_client
