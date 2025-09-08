"""Модуль конфигурации приложения. Содержит основные настройки и параметры для работы приложения."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс используется для настройки приложения."""

    DATABASE_URL: str = "postgresql://user:password@postgresserver/db"

    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        """Конфигурация настройки."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        from_attributes = True


settings = Settings()
