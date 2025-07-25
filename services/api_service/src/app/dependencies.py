from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from arq.connections import create_pool, ArqRedis
from qdrant_client import AsyncQdrantClient

from app.config import settings


# --- SQLAlchemy ---
engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionMaker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionMaker() as session:
        yield session


# --- Arq + Qdrant Clients (startup globals) ---
arq_redis: ArqRedis = None
qdrant: AsyncQdrantClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """App startup/shutdown context manager for shared connections."""
    global arq_redis, qdrant

    arq_redis = await create_pool(settings.REDIS_URL)
    qdrant = AsyncQdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

    yield

    await arq_redis.close()
    await qdrant.close()
