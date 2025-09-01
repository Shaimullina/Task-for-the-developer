from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс используется для настройки приложения
    """

    DATABASE_URL: str = "postgresql://user:password@postgresserver/db"

    SECRET_KEY: str = "5e7f8754073e5e9dd4eed3b3f1d797673670aa3eda75448ba0eb826fe738bef1"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        """
        Конфигурация настройки
        """

        env_file = ".env"  # файл с переменным окружением
        env_file_encoding = "utf-8"  # кодировка файла
        from_attributes = True  # Разрешить загрузку настроек из атрибутов


settings = Settings()  # экземпляр настроек приложения
