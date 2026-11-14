from datetime import datetime, timezone, timedelta
from fastapi import status
from app.auth import blacklisted_tokens, refresh_tokens
from app.auth import (
    cleanup_expired_blacklisted_tokens, cleanup_expired_refresh_tokens,
)


BASE_URL = "http://localhost:8000"
USERNAME = "admin"
PASSWORD = "password"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to the FastAPI Refresh JWT Auth Example"}


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
        "/protected", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


def test_login_with_valid_credentials(client):
    response = client.post("/login", json={"username": "admin", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert data["token_type"] == "bearer"
    assert "access_token" in data
    assert "refresh_token" in data
    assert len(data["access_token"]) > 0
    assert len(data["refresh_token"]) > 0


def test_login_with_invalid_credentials(client):
    response = client.post(
        "/login", json={"username": "wrong", "password": "credentials"}
    )
    assert response.status_code == 401


def test_refresh_token_endpoint_with_valid_token(client, refresh_token):
    response = client.post("/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["message"] == "Token refreshed successfully"
    assert len(data["access_token"]) > 0


def test_refresh_token_endpoint_with_invalid_token(client):
    response = client.post("/refresh", json={"refresh_token": "invalid_refresh_token"})
    assert response.status_code == 401
    assert "Invalid refresh token" in response.json()["detail"]


def test_refresh_token_endpoint_with_expired_token(client):
    expired_token = "expired_refresh_token"
    refresh_tokens[expired_token] = {
        "username": "admin",
        "exp": datetime.now(timezone.utc) - timedelta(hours=1),
    }

    response = client.post("/refresh", json={"refresh_token": expired_token})
    assert response.status_code == 401
    assert "Refresh token has expired" in response.json()["detail"]

    assert expired_token not in refresh_tokens


def test_logout_without_token(client):
    response = client.post("/logout")
    assert response.status_code == 401


def test_logout_with_valid_token_only(client, auth_headers, login_user):
    access_token = login_user.json()["access_token"]

    response = client.post("/logout", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"

    assert access_token in blacklisted_tokens

    response = client.get("/protected", headers=auth_headers)
    assert response.status_code == 401


def test_logout_with_both_tokens(client, auth_headers, login_user, refresh_token):
    access_token = login_user.json()["access_token"]

    response = client.post(
        "/logout", headers=auth_headers, json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"

    assert access_token in blacklisted_tokens
    assert refresh_token not in refresh_tokens

    response = client.post("/refresh", json={"refresh_token": refresh_token})
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


def test_refresh_token_creates_valid_access_token(client, refresh_token):
    response = client.post("/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    new_access_token = response.json()["access_token"]

    new_auth_headers = {"Authorization": f"Bearer {new_access_token}"}
    response = client.get("/protected", headers=new_auth_headers)
    assert response.status_code == 200
    assert response.json()["authenticated_user"] == "admin"


def test_expired_token_cleanup():
    expired_access_token = "expired_access_token"
    blacklisted_tokens[expired_access_token] = datetime.now(timezone.utc) - timedelta(
        hours=1
    )

    expired_refresh_token = "expired_refresh_token"
    refresh_tokens[expired_refresh_token] = {
        "username": "admin",
        "exp": datetime.now(timezone.utc) - timedelta(hours=1),
    }

    valid_access_token = "valid_access_token"
    blacklisted_tokens[valid_access_token] = datetime.now(timezone.utc) + timedelta(
        hours=1
    )

    valid_refresh_token = "valid_refresh_token"
    refresh_tokens[valid_refresh_token] = {
        "username": "admin",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }

    cleanup_expired_blacklisted_tokens()
    cleanup_expired_refresh_tokens()

    assert expired_access_token not in blacklisted_tokens
    assert valid_access_token in blacklisted_tokens
    assert expired_refresh_token not in refresh_tokens
    assert valid_refresh_token in refresh_tokens


def test_refresh_token_flow_integration(client):
    login_response = client.post(
        "/login", json={"username": "admin", "password": "password"}
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    access_token = login_data["access_token"]
    refresh_token = login_data["refresh_token"]

    auth_headers = {"Authorization": f"Bearer {access_token}"}
    protected_response = client.get("/protected", headers=auth_headers)
    assert protected_response.status_code == 200

    refresh_response = client.post("/refresh", json={"refresh_token": refresh_token})
    assert refresh_response.status_code == 200
    new_access_token = refresh_response.json()["access_token"]
    assert new_access_token != access_token

    new_auth_headers = {"Authorization": f"Bearer {new_access_token}"}
    protected_response2 = client.get("/protected", headers=new_auth_headers)
    assert protected_response2.status_code == 200

    logout_response = client.post(
        "/logout", headers=new_auth_headers, json={"refresh_token": refresh_token}
    )
    assert logout_response.status_code == 200

    protected_response3 = client.get("/protected", headers=new_auth_headers)
    assert protected_response3.status_code == 401

    refresh_response2 = client.post("/refresh", json={"refresh_token": refresh_token})
    assert refresh_response2.status_code == 401
