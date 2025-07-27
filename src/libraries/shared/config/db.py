from pydantic import BaseModel


class DBSettings(BaseModel):
    url: str
