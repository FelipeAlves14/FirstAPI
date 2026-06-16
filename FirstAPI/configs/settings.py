"""Application settings."""

# pylint: disable=import-error,too-few-public-methods

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Environment-driven application settings."""

    DB_URL: str = Field(default="postgresql+asyncpg://first:first@localhost/first")


settings = Settings()
