from uuid import UUID

from pydantic import BaseModel, HttpUrl
from typing import Literal

class JobCreateRequest(BaseModel):
    image_url: HttpUrl

class JobCreateResponse(BaseModel):
    job_id: UUID

class JobStatusResponse(BaseModel):
    job_id: UUID
    status: Literal["pending", "processing", "done", "error"]
    detail: str | None = None
