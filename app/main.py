"""Основной файл приложения FastAPI, который инициализирует и настраивает веб-приложение."""

from fastapi import FastAPI, Depends, HTTPException
from app.database import engine, get_db, Base
from app.models import user, tasks
from app.schemas.user import UserRead
from app.routers import user, tasks
from app.auth.jwt_handler import get_current_user

"""Основной экземпляр FastAPI приложения."""
app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(
    user.router, prefix="/users", dependencies=[Depends(get_db)]
)  # Подключение роутера для работы с пользователями


app.include_router(
    tasks.router, prefix="/tasks", dependencies=[Depends(get_db)]
)  # Подключение роутера для работы с pflfxfvb


def check_user_permissions(
    user_id: int,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Проверяет, что текущий пользователь может управлять данным пользователем"""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен: вы можете управлять только своим профилем",
        )
