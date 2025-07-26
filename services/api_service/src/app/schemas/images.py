import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, Field


class ImageMetadataSchema(BaseModel):
    """Metadata information about the uploaded image."""
    filename: str
    content_type: str
    upload_time: datetime
    size_bytes: int
    link: HttpUrl
    embedding_model: Optional[str] = Field(
        default=None,
        description="Model used for generating the embedding"
    )


class ImageFeaturesSchema(BaseModel):
    """Image feature representation."""
    vector: list[float]
    dimension: int


class ScoredImageSchema(BaseModel):
    id: uuid.UUID
    score: float
    metadata: ImageMetadataSchema


class ImageSchema(BaseModel):
    id: uuid.UUID
    metadata: ImageMetadataSchema
    features: Optional[ImageFeaturesSchema] = None
