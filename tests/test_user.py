"""Модуль содержит тестовые случаи для проверки функциональности работы с пользователями в приложении."""

from app.schemas.user import UserRead


def test_create_user(create_user):
    """Тест создания пользователя."""
    user = create_user(
        email="test@example.com", password="securepassword123", name="Test User"
    )
    assert user.email == "test@example.com"
    assert user.name == "Test User"


def test_get_user(create_user, db):
    """Тест получения пользователя."""
    user = create_user(
        email="test@example.com", password="securepassword123", name="Test User"
    )
    db_user = db.query(UserRead).filter(UserRead.email == "test@example.com").first()
    assert db_user.id == user.id
    assert db_user.name == "Test User"
