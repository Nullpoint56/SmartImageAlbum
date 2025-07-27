from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from db import async_session_factory


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an AsyncSession for each request,
    and ensures proper cleanup after the request.
    """
    session: AsyncSession
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()