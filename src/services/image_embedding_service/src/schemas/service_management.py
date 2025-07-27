from typing import Literal

from pydantic import BaseModel


class ReadinessResponse(BaseModel):
    status: Literal["ok", "unavailable"]
    model_loaded: bool
    model_name: str


class HealthResponse(BaseModel):
    status: Literal["ok", "unavailable"]
