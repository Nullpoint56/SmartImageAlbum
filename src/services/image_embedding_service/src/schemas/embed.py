from pydantic import BaseModel
from typing import List

class EmbeddingResponse(BaseModel):
    model_name: str
    embedding: List[float]
