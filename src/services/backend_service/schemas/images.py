import uuid
from typing import Optional

from pydantic import BaseModel, Field


class ImageMetadataSchema(BaseModel):
    """Metadata information about the uploaded image."""
    filename: str
    content_type: str

    size_bytes: int
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


class ImageSchema(BaseModel):
    id: uuid.UUID
    metadata: ImageMetadataSchema
    features: Optional[ImageFeaturesSchema] = None
