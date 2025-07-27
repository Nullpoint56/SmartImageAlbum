from pydantic_settings import BaseSettings, SettingsConfigDict

from config.embedding import EmbedderSettings


class AppConfig(BaseSettings):
    embedder: EmbedderSettings

    model_config = SettingsConfigDict(
        env_file="app.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__"
    )

