from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tasks import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.auth.jwt_handler import get_current_user
from typing import List

router = APIRouter()


@router.post("/tasks", response_model=TaskRead)
async def create_tasks(
    task: TaskCreate,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Создание задачи новой
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=current_user.id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/users/{user_id}/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Получение конкретных задач пользователя
    """
    tasks = (
        db.query(Task)
        .filter(Task.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return tasks


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Обновление задачи
    """
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Удаление задачи
    """
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена!")
    else:
        db.delete(task)
        db.commit()
