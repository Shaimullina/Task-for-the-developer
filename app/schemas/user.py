"""Модуль содержит схемы Pydantic для работы с пользователями в приложении."""

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    """Модель для создания нового пользователя."""

    name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Модель для апдейта пользователя."""

    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserRead(BaseModel):
    """Модель для использования пользователя в ответе."""

    id: int
    name: str
    email: EmailStr

    class Config:
        """Конфигурация модели."""

        orm_mode = True


class UserBase(BaseModel):
    """Базовая модель."""

    username: str
    email: str

    class Config:
        """Конфигурация модели."""

        orm_mode = True


class Token(BaseModel):
    """Модель для представления JWT-токена."""

    access_token: str
    token_type: str
