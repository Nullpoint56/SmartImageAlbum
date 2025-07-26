from typing import Optional

from pydantic import BaseModel, Field


class DBSettings(BaseModel):
    url: Optional[str] = Field(default=None, validation_alias="APP_DATABASE_URL",)
