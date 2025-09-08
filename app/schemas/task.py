"""Модуль содержит схемы Pydantic для работы с задачами в приложении."""

from pydantic import BaseModel
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    """Возможные статусы задачи."""

    new = "новая"
    in_progress = "в процессе"
    completed = "завершена"


class TaskCreate(BaseModel):
    """Модель создания задачи."""

    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.new


class TaskUpdate(BaseModel):
    """Модель апдейта задачи."""

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskRead(BaseModel):
    """Модель для представления задачи в ответе."""

    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    user_id: int

    class Config:
        """Конфигурация модели."""

        orm_mode = True
