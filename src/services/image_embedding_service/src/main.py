from contextlib import asynccontextmanager
from typing import AsyncIterator, Any

import uvicorn
from fastapi import FastAPI

from ai.model_management import CLIPEmbeddingService
from config.app import AppConfig
from routers.embed import embed_router
from routers.service_management import service_management_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[dict[str, Any]]:
    # TODO: Find a solution to the untyped nature of state
    app_config = AppConfig()
    model_service = CLIPEmbeddingService(app_config.embedder.model_name)
    await model_service.load_model()
    yield {"model_service": model_service}


app = FastAPI(title="Embedding Service", version="1.0", lifespan=lifespan)

# Register routers
app.include_router(embed_router)
app.include_router(service_management_router)


if __name__ == "__main__":
    uvicorn.run(app, port=8001, host="0.0.0.0")