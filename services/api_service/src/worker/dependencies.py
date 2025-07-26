from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from qdrant_client import QdrantClient
from minio import Minio

from shared.clients.embedder import EmbedderClient
from worker.config import WorkerConfig

_engine = None
_SessionLocal = None
_qdrant_client = None


def get_minio_client(config: WorkerConfig) -> Minio:
    return Minio(
        endpoint=config.minio_endpoint,
        access_key=config.minio_access_key,
        secret_key=config.minio_secret_key,
        secure=config.minio_secure,
    )


def get_embedder_client(config: WorkerConfig) -> EmbedderClient:
    return EmbedderClient(base_url=config.embedder_base_url)


def get_qdrant_client(config: WorkerConfig) -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            host=config.qdrant_host,
            port=config.qdrant_port,
            https=config.qdrant_https,
        )
    return _qdrant_client


def get_engine(config: WorkerConfig):
    global _engine
    if _engine is None:
        _engine = create_engine(str(config.app_database_url), echo=False, future=True)
    return _engine


def get_session(config: WorkerConfig) -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(config), autoflush=False, autocommit=False)
    return _SessionLocal()
