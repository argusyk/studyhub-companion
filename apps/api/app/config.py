"""Налаштування з оточення (локальний .env у apps/api або в корені репозиторію)."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../../.env"), extra="ignore")

    # Для локальної розробки без Docker достатньо SQLite-файлу.
    database_url: str = "sqlite:///./studyhub_dev.sqlite3"
    department_tz: str = "Europe/Kyiv"
    upload_dir: str = "uploads"


@lru_cache
def get_settings() -> Settings:
    return Settings()
