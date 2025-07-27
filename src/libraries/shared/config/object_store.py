from pydantic import BaseModel


class ObjectStoreSettings(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    secure: bool = False
    bucket: str = "uploads"