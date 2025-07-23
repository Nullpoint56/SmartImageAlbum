from fastapi import FastAPI
from image_embedding_service.dependencies import get_model_and_processor
from image_embedding_service.routers.embed import embed_router

app = FastAPI(title="Embedding Service", version="1.0")

# Trigger lazy loading so model downloads on boot
get_model_and_processor()

# Register routers
app.include_router(embed_router)

@app.get("/health")
async def health() -> dict:
    """
    Liveness check.
    """
    return {"status": "ok"}
