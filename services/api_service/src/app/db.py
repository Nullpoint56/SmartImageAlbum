from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession,
    async_sessionmaker, create_async_engine
)

from app.config.app import get_app_config

db_config = get_app_config().db

engine: AsyncEngine = create_async_engine(
    url=db_config.url,
    connect_args={"check_same_thread": False}
)

async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)