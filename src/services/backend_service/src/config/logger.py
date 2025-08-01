from pydantic import BaseModel, Field

class LoggerSettings(BaseModel):
    level: str = Field(default="INFO")
    file_location: str = Field(default="logs/app.log")
