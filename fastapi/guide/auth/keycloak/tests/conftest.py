import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi.security import HTTPAuthorizationCredentials
from typing import Optional
import main as main_module
from main import app
from app.database import db
import app.keycloak.auth as auth_module


@pytest.fixture(autouse=True)
def clear_database():
    db.clear()
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_keycloak_client():
    with patch("app.keycloak.client.keycloak_client") as mock_core_client:
        main_module.keycloak_client = mock_core_client

        auth_module.keycloak_client = mock_core_client

        mock_client = mock_core_client

        mock_client.authenticate_user.return_value = {
            "access_token": "mocked_access_token",
            "token_type": "bearer",
            "expires_in": 3600,
        }

        mock_client.validate_token.return_value = {
            "sub": "test-user-id",
            "preferred_username": "testuser",
            "email": "test@example.com",
            "realm_access": {"roles": ["user"]},
        }

        mock_client.get_user_info.return_value = {
            "sub": "test-user-id",
            "preferred_username": "testuser",
            "email": "test@example.com",
            "realm_access": {"roles": ["user"]},
        }

        yield mock_client


@pytest.fixture
def mock_keycloak_auth():
    def _mock_user(credentials: Optional[HTTPAuthorizationCredentials] = None):
        return "testuser"

    app.dependency_overrides.clear()
    app.dependency_overrides[__import__("main").main.get_current_user_keycloak] = (
        _mock_user
    )

    yield _mock_user

    app.dependency_overrides.clear()


@pytest.fixture
def authenticated_headers():
    """Headers with valid authorization token."""
    return {"Authorization": "Bearer mocked_access_token"}
