from pydantic import BaseModel, AnyUrl


class EmbedderClientSettings(BaseModel):
    base_url: str
