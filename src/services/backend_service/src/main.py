from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from backend_service.db import engine
from backend_service.dependencies.logging import setup_logging
from backend_service.routers.images import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context.
    - Runs Alembic migrations on startup using sync DB (from env)
    - Keeps app config available via app.state
    - Disposes async engine on shutdown
    """
    await setup_logging()
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    yield


    # Clean up engine on shutdown
    await engine.dispose()


app = FastAPI(lifespan=lifespan, docs_url="/api/docs", debug=True)

# Routers
app.include_router(router)
