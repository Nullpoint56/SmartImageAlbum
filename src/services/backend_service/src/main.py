from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.app import get_app_config
from db import engine
from dependencies.logging import setup_logging
from routers.images import image_router
from routers.service_management import service_management_router
from utils import init_minio_bucket, init_vector_db_collection, create_schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context.
    - Runs Alembic migrations on startup using sync DB (from env)
    - Keeps app config available via app.state
    - Disposes async engine on shutdown
    """
    app_config = get_app_config()
    await setup_logging(app_config.logger)
    await create_schema(engine)
    await init_minio_bucket(app_config.object_store)
    await init_vector_db_collection(app_config.vector_db)

    yield
    # Clean up engine on shutdown
    await engine.dispose()


app = FastAPI(lifespan=lifespan, docs_url="/api/docs", debug=True)

# Routers
app.include_router(image_router)
app.include_router(service_management_router)
