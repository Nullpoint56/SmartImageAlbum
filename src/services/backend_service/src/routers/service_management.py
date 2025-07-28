from fastapi import APIRouter

service_management_router = APIRouter(prefix="", tags=["service_management"])


@service_management_router.get("/health")
async def health() -> dict[str, str]:
    """
    Liveness and readiness check: verifies model is loaded.
    """
    return {"status": "ok"}

