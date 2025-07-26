from pydantic import BaseModel


class VectorDBConfig(BaseModel):
    host: str
    port: int
    collection: str