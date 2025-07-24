from pydantic import BaseModel, HttpUrl
from uuid import UUID
from typing import Optional, List

class ImageUploadResponse(BaseModel):
    image_id: UUID
    url: HttpUrl

class ImageMetadataResponse(BaseModel):
    image_id: UUID
    filename: str
    content_type: str
    url: HttpUrl
    embedding: Optional[list[float]] = None

class SimilarImage(BaseModel):
    image_id: UUID
    score: float

class SimilarImageResponse(BaseModel):
    matches: List[SimilarImage]
