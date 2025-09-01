from fastapi import FastAPI, Depends
from app.database import engine, get_db, Base
from app.models import tasks, user


from app.routers import user, tasks


app = FastAPI()
"""  
Основной экземпляр FastAPI приложения

"""
Base.metadata.create_all(bind=engine)  # Создание таблиц в базе данных


app.include_router(
    user.router, prefix="/users", dependencies=[Depends(get_db)]
)  # Подключение роутера для работы с пользователями


app.include_router(
    tasks.router, prefix="/tasks", dependencies=[Depends(get_db)]
)  # Подключение роутера для работы с pflfxfvb
