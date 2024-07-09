import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


@pytest.fixture(scope="function")
def auth_headers(test_user):
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def test_create_post(auth_headers):
    response = client.post(
        "/posts",
        json={"title": "Test Post", "content": "This is a test post"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"
    assert response.json()["content"] == "This is a test post"


def test_read_post(auth_headers):
    # First, create a post
    response = client.post(
        "/posts",
        json={"title": "Test Post", "content": "This is a test post"},
        headers=auth_headers
    )
    post_id = response.json()["id"]

    # Now, read the post
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"
    assert response.json()["content"] == "This is a test post"


def test_update_post(auth_headers):
    # First, create a post
    response = client.post(
        "/posts",
        json={"title": "Test Post", "content": "This is a test post"},
        headers=auth_headers
    )
    post_id = response.json()["id"]

    # Now, update the post
    response = client.put(
        f"/posts/{post_id}",
        json={"title": "Updated Test Post", "content": "This is an updated test post"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Post"
    assert response.json()["content"] == "This is an updated test post"


def test_delete_post(auth_headers):
    # First, create a post
    response = client.post(
        "/posts",
        json={"title": "Test Post", "content": "This is a test post"},
        headers=auth_headers
    )
    post_id = response.json()["id"]

    # Now, delete the post
    response = client.delete(f"/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 204

    # Try to read the deleted post
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404
