from pydantic import BaseModel, Field

class LoggerSettings(BaseModel):
    level: str = Field(default="DEBUG", validation_alias="LOG_LEVEL")
    file_location: str = Field(default="logs/app.log", validation_alias="LOG_FILE")
