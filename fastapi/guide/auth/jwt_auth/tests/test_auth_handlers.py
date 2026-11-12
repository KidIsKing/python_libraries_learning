import pytest
from fastapi import status
from fastapi.testclient import TestClient
from datetime import datetime, timezone, timedelta
from main import app
from app.auth import cleanup_expired_blacklisted_tokens, blacklisted_tokens
 

BASE_URL = "http://localhost:8000"
USERNAME = "admin"
PASSWORD = "password"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to the FastAPI JWT Auth Example"}


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


def test_public_route(client):
    response = client.get("/public")
    assert response.status_code == 200
    assert response.json()["message"] == "This is a public route"


def test_protected_route_without_token(client):
    response = client.get("/protected")
    assert response.status_code == 401


def test_protected_route_with_valid_token(client, auth_headers):
    response = client.get("/protected", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "This is a protected route"
    assert response.json()["authenticated_user"] == "admin"


def test_protected_route_with_invalid_token(client):
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


def test_login_with_valid_credentials(client):
    response = client.post(
        "/login",
        json={"username": "admin", "password": "password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert data["token_type"] == "bearer"
    assert "access_token" in data
    assert len(data["access_token"]) > 0


def test_login_with_invalid_credentials(client):
    response = client.post(
        "/login",
        json={"username": "wrong", "password": "credentials"}
    )
    assert response.status_code == 401


def test_logout_without_token(client):
    response = client.post("/logout")
    assert response.status_code == 401


def test_logout_with_valid_token(client, auth_headers, login_user):
    token = login_user.json()["access_token"]

    response = client.post("/logout", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"

    assert token in blacklisted_tokens

    # Проверяем защищённую ручку после выхода из учётки
    response = client.get("/protected", headers=auth_headers)
    assert response.status_code == 401


def test_me_endpoint_with_valid_token(client, auth_headers):
    response = client.get("/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert "message" in data


def test_me_endpoint_without_token(client):
    response = client.get("/me")
    assert response.status_code == 401


def test_expired_token_cleanup():
    # Закончившийся по времени токен
    expired_token = "expired_token"
    blacklisted_tokens[expired_token] = datetime.now(timezone.utc) - timedelta(hours=1)

    # Активный токен
    valid_token = "valid_token"
    blacklisted_tokens[valid_token] = datetime.now(timezone.utc) + timedelta(hours=1)

    cleanup_expired_blacklisted_tokens()

    assert expired_token not in blacklisted_tokens
    assert valid_token in blacklisted_tokens
