class TestAuth:
    def test_login_success(self, client, test_user):
        """Успешный логин с правильными данными"""
        login_data = {"username": test_user.email, "password": "password123"}
        response = client.post("/token", data=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_password(self, client, test_user):
        """Логин с неправильным паролем"""
        login_data = {"username": test_user.email, "password": "wrongpass"}
        response = client.post("/token", data=login_data)

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_invalid_user(self, client):
        """Логин с несуществующим пользователем"""
        login_data = {"username": "nouser@example.com", "password": "password123"}
        response = client.post("/token", data=login_data)

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_missing_password(self, client):
        """Попытка логина без пароля"""
        login_data = {"username": "test@example.com"}
        response = client.post("/token", data=login_data)
        assert response.status_code == 422
