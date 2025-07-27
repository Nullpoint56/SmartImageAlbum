from pydantic import BaseModel


class EmbedderSettings(BaseModel):
    model_name: str
