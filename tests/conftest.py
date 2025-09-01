import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User, Task

SQLALCHEMY_DATABASE_URL = (
    "sqlite:///./test.db"  # URL подключения к тестовой базе данных
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
"""  
Двигатель SQLAlchemy для тестовой базы данных
"""
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """
    Создает базу данных перед каждым тестом и удаляет после
    """

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """
    Фиксатура для создания тестового клиента FastAPI

    Переопределяет зависимость get_db для тестов
    """

    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def test_user(db):
    """
    Фиксатура для создания тестового пользователя

    Создает пользователя в базе данных
    """
    user = User(
        email="test@example.com",
        password="password123",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_task(db, test_user):
    """
    Фиксатура для создания тестовой задачи

    Создает задачу, привязанную к тестовому пользователю
    """
    task = Task(
        title="Test Task",
        description="This is a test task",
        completed=False,
        owner_id=test_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
