from fastapi import FastAPI

from dependencies import lifespan
from routers import images, health

app = FastAPI(title="Image API Service", lifespan=lifespan)

# Register routers
app.include_router(health.router)
app.include_router(images.router, prefix="/images")
