from pydantic import BaseModel, HttpUrl
import uuid

class EmbeddingRequest(BaseModel):
    image_id: uuid.UUID
    url: HttpUrl


class EmbeddingResponse(BaseModel):
    image_id: uuid.UUID
    model_name: str
    embedding: list[float]
    dimension: int