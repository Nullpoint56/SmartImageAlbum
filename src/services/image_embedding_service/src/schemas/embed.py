import uuid

from pydantic import BaseModel, HttpUrl
from typing import List

class EncodeRequest(BaseModel):
    image_id: uuid.UUID
    image_url: HttpUrl

class EncodeResponse(BaseModel):
    image_id: uuid.UUID
    model_name: str
    embedding: List[float]
