"""Application configuration settings."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file."""

    # Database
    database_url: str = "sqlite:///./database.db"

    # Logging
    log_level: str = "INFO"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: List[str] = ["http://localhost", "http://localhost:8000"]

    # DB pooling (ignored for sqlite)
    pool_size: int = 5
    max_overflow: int = 10

    class ConfigDict:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Return cached Settings instance."""
    return Settings()
