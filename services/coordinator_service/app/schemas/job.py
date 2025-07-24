from uuid import UUID

from pydantic import BaseModel, HttpUrl, ConfigDict

from app.models.job import JobStatus, JobState


class JobCreateRequest(BaseModel):
    image_url: HttpUrl

class JobCreateResponse(BaseModel):
    id: UUID

class JobStatusResponse(BaseModel):
    id: UUID
    status: JobStatus
    state: JobState
    detail: str | None = None

    model_config = ConfigDict(from_attributes=True)