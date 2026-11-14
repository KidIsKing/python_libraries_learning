from fastapi import HTTPException
from fastapi import status
from app.database import db


BASE_URL = "http://localhost:8000"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Welcome to the FastAPI Keycloak Auth Example"
    }


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


def test_public_route(client):
    response = client.get("/public")
    assert response.status_code == status.HTTP_200_OK
    assert "public" in response.json()["message"]


def test_login_success(client, mock_keycloak_client):
    response = client.post(
        "/login", json={"username": "testuser", "password": "password"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["username"] == "testuser"
    assert data["token_type"] == "bearer"
    assert data["message"] == "Login successful"


def test_login_invalid_credentials(client, mock_keycloak_client):
    mock_keycloak_client.authenticate_user.side_effect = HTTPException(
        status_code=401, detail="Invalid username or password"
    )

    response = client.post(
        "/login", json={"username": "invalid", "password": "invalid"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid username or password" in response.json()["detail"]


def test_protected_route_without_token(client):
    response = client.get("/protected")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_protected_route_with_valid_token(client, mock_keycloak_auth):
    response = client.get(
        "/protected", headers={"Authorization": "Bearer mocked_access_token"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "protected" in data["message"]
    assert data["authenticated_user"] == "testuser"


def test_logout_and_blacklist(client, mock_keycloak_client):
    response = client.post(
        "/logout", headers={"Authorization": "Bearer mocked_access_token"}
    )
    assert response.status_code == status.HTTP_200_OK

    response = client.get(
        "/protected", headers={"Authorization": "Bearer mocked_access_token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_without_token(client):
    response = client.post("/logout")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_info_success(client, mock_keycloak_auth):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "keycloak_id": "test-user-id",
        "roles": ["user"],
        "created_at": "2023-01-01T00:00:00",
    }
    db.set("users", "testuser", user_data)

    response = client.get(
        "/me", headers={"Authorization": "Bearer mocked_access_token"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "testuser"
    assert "user_data" in data
    assert "message" in data


def test_get_user_info_user_not_found(client, mock_keycloak_auth):
    response = client.get(
        "/me", headers={"Authorization": "Bearer mocked_access_token"}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "User not found" in response.json()["detail"]


def test_get_user_info_without_token(client):
    response = client.get("/me")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_keycloak_service_error(client, mock_keycloak_client):
    mock_keycloak_client.authenticate_user.side_effect = Exception(
        "Service unavailable"
    )

    response = client.post(
        "/login", json={"username": "testuser", "password": "password"}
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Authentication service error" in response.json()["detail"]
