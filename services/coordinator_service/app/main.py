from fastapi import FastAPI
from starlette.middleware import Middleware

from app.dependencies import engine, Base
from app.middleware.location_header import AbsoluteLocationHeaderMiddleware
from app.routers.jobs import router

middleware = [
    Middleware(AbsoluteLocationHeaderMiddleware)
]

app = FastAPI(title="Coordinator Service", version="1.0")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

app.include_router(router)
