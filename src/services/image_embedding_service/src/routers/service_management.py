from fastapi import APIRouter


service_management_router = APIRouter(prefix="", tags=["service_management"])

@service_management_router.get("/health")
async def health() -> dict:
    """
    Liveness check.
    """
    return {"status": "ok"}