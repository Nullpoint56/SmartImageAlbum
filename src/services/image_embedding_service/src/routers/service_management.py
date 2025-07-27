from fastapi import APIRouter, Request

from schemas.service_management import HealthResponse, ReadinessResponse

service_management_router = APIRouter(prefix="", tags=["service_management"])


@service_management_router.get("/health")
async def health() -> HealthResponse:
    """
    Liveness and readiness check: verifies model is loaded.
    """
    return HealthResponse(
        status="ok"
    )


@service_management_router.get("/ready")
async def health(request: Request) -> ReadinessResponse:
    """
    Liveness and readiness check: verifies model is loaded.
    """
    model_service = request.state.model_service
    ready = model_service.model is not None

    return ReadinessResponse(
        status="ok" if ready else "unavailable",
        model_loaded=ready,
        model_name=model_service.model_id if ready else None,
    )
