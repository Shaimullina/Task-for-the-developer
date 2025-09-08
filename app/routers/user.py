"""Файл содержит все эндпоинты, который применяются к пользователям."""

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.main import get_db
from app.models.user import User
from app.env import get_password_hash
from app.auth.jwt_handler import get_current_user, check_user_permissions
from app.schemas.user import UserBase, UserCreate, UserRead, UserUpdate


router = APIRouter()


@router.post("/users", response_model=UserBase)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создание пользователя."""
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, password=hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users", response_model=list[UserRead])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Получить список пользователей."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить конкретного пользователя."""
    check_user_permissions(user_id, current_user, db)
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить данные о пользователе."""
    check_user_permissions(user_id, current_user, db)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить пользователя."""
    check_user_permissions(user_id, current_user, db)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    else:
        db.delete(user)
        db.commit()
        return {"message": "Пользователь удален"}
