from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check() -> dict:
    """Returns basic health check response."""
    return {"status": "ok"}
