from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_login(test_user):
    response = client.post(
        "/token",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_incorrect_password(test_user):
    response = client.post(
        "/token",
        json={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_read_users_me(test_user, client):
    response = client.post(
        "/token",
        json={"username": "testuser", "password": "testpassword"}
    )
    access_token = response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"
