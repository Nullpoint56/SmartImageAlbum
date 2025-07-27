from functools import cached_property

from minio import Minio
from qdrant_client import QdrantClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import WorkerConfig
from shared.clients.embedder import EmbedderClient


class WorkerContext:
    """Central place for all worker service dependencies."""

    def __init__(self, config: WorkerConfig):
        self.config = config

        # Database engine and session factory
        self._engine = None
        self._SessionLocal = None

    @cached_property
    def minio(self) -> Minio:
        cfg = self.config.object_store
        return Minio(
            endpoint=cfg.endpoint,
            access_key=cfg.access_key,
            secret_key=cfg.secret_key,
            secure=cfg.secure,
        )

    @cached_property
    def embedder(self) -> EmbedderClient:
        return EmbedderClient(base_url=self.config.embedder_client.base_url)

    @cached_property
    def qdrant(self) -> QdrantClient:
        cfg = self.config.vector_db
        return QdrantClient(
            host=cfg.host,
            port=cfg.port,
            https=cfg.port == 443 or cfg.host.startswith("https")
        )

    @cached_property
    def db(self) -> Session:
        """Returns a SQLAlchemy session (use `.close()` manually after use)."""
        if self._SessionLocal is None:
            self._engine = create_engine(str(self.config.db.url), future=True, echo=False)
            self._SessionLocal = sessionmaker(bind=self._engine, autoflush=False, autocommit=False)
        return self._SessionLocal()

    def close(self) -> None:
        """Closes the active SQLAlchemy session."""
        self.db.close()