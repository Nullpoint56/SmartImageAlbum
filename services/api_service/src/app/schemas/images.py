import uuid
from pydantic import BaseModel, HttpUrl
from typing import Optional


class ImageMetadata(BaseModel):
    id: uuid.UUID
    filename: str
    content_type: str
    url: HttpUrl
    status: str
    state: Optional[str] = None
    detail: Optional[str] = None


class SimilarImageResult(BaseModel):
    image_id: uuid.UUID
    similarity: float
    url: HttpUrl
