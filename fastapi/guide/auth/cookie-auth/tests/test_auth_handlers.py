import pytest
import base64
from fastapi import status
from main import app
from app.auth import active_sessions


BASE_URL = "http://localhost:8000"
USERNAME = "admin"
PASSWORD = "password"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to the FastAPI Session Auth Example"}


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


def test_public_route(client):
    response = client.get("/public")
    assert response.status_code == 200
    assert response.json()["message"] == "This is a public route"


def test_protected_route_without_cookie(client):
    response = client.get("/protected")
    assert response.status_code == 401


def test_protected_route_with_valid_cookie(client, login_user):
    response = client.get(
        "/protected",
        cookies=login_user.cookies
    )
    assert response.status_code == 200
    assert response.json()["message"] == 'This is a protected route'
    assert response.json()["authenticated_user"] == "admin"


def test_protected_route_with_invalid_cookie(client):
    response = client.get(
        "/protected",
        cookies={"session_token": "invalid_token"}
    )
    assert response.status_code == 401


def test_login_with_valid_credentials(client):
    response = client.post(
        "/login",
        json={"username": "admin", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "admin"
    assert "session_token" in response.cookies

    session_token = response.cookies["session_token"]
    assert session_token in active_sessions
    assert active_sessions[session_token] == "admin"


def test_login_with_invalid_credentials(client):
    response = client.post(
        "/login",
        json={"username": "wrong", "password": "credentials"}
    )
    assert response.status_code == 401


def test_logout_without_cookie(client):
    response = client.post("/logout")
    assert response.status_code == 401


def test_logout_with_valid_cookie(client, login_user):
    session_token = login_user.cookies["session_token"]

    response = client.post(
        "/logout",
        cookies=login_user.cookies
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"

    assert session_token not in active_sessions

    assert not response.cookies


@pytest.mark.parametrize("malformed_header", [
    {"Authorization": "Basic invalid-base64"},
    {"Authorization": "NotBasic valid-base64"},
    {"Authorization": "Bearer token"}
])
def test_protected_endpoint_malformed_auth(client, malformed_header):
    response = client.get("/protected", headers=malformed_header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
