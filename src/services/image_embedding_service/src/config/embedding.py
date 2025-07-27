from pydantic import BaseModel


class EmbeddingConfig(BaseModel):
    model_name: str
