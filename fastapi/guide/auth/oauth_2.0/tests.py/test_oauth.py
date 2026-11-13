import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import status
from app.database.users import clear_oauth_users, oauth_users, github_id_to_username
from app.oauth.models import OAuthUser
from app.database.users import create_or_update_oauth_user
from app.auth import create_jwt_token
from app.database.users import get_oauth_user_by_username, get_oauth_user_by_github_id, delete_oauth_user


@pytest.fixture
def mock_github_user_data():
    return {
        "id": 123456,
        "login": "testuser",
        "name": "Test User",
        "email": "test@example.com",
        "avatar_url": "https://avatars.githubusercontent.com/u/123456",
        "html_url": "https://github.com/testuser",
        "created_at": "2020-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_github_token_response():
    return {
        "access_token": "gho_test_token_123",
        "token_type": "bearer",
        "scope": "user:email",
    }


@pytest.fixture
def oauth_user():
    user = OAuthUser(
        github_id=123456,
        username="testuser",
        display_name="Test User",
        email="test@example.com",
        avatar_url="https://avatars.githubusercontent.com/u/123456",
        profile_url="https://github.com/testuser",
    )
    oauth_users["testuser"] = user
    github_id_to_username[123456] = "testuser"
    yield user
    clear_oauth_users()


@pytest.fixture(autouse=True)
def cleanup_oauth_users():
    yield
    clear_oauth_users()


def test_github_login_not_configured(client):
    with patch("app.oauth.handlers.github_oauth", None):
        response = client.get("/auth/github")

        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert "not configured" in response.json()["detail"]


@patch("app.oauth.handlers.github_oauth")
def test_github_login_success(mock_oauth, client):
    mock_oauth.get_authorization_url.return_value = (
        "https://github.com/login/oauth/authorize?client_id=test"
    )

    response = client.get("/auth/github")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "auth_url" in data
    assert "github.com" in data["auth_url"]


def test_github_redirect_not_configured(client):
    with patch("app.oauth.handlers.github_oauth", None):
        response = client.get("/auth/github/redirect")

        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


@patch("app.oauth.handlers.github_oauth")
def test_github_redirect_success(mock_oauth, client):
    mock_oauth.get_authorization_url.return_value = (
        "https://github.com/login/oauth/authorize?client_id=test"
    )

    response = client.get("/auth/github/redirect", follow_redirects=False)

    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert "github.com" in response.headers["location"]


def test_github_callback_not_configured(client):
    with patch("app.oauth.handlers.github_oauth", None):
        response = client.get("/auth/github/callback?code=test_code")

        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


@patch("app.oauth.handlers.github_oauth")
def test_github_callback_error(mock_oauth, client):
    response = client.get(
        "/auth/github/callback?error=access_denied&error_description=User denied access"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "denied access" in response.json()["detail"]


@patch("app.oauth.handlers.github_oauth")
def test_github_callback_no_code(mock_oauth, client):
    response = client.get("/auth/github/callback")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "code not provided" in response.json()["detail"]


@patch("app.oauth.handlers.github_oauth")
async def test_github_callback_success(
    mock_oauth, client, mock_github_token_response, mock_github_user_data
):
    mock_token = MagicMock(
        access_token="gho_test_token_123",
        token_type="bearer",
        scope="user:email"
    )

    mock_user = MagicMock()
    mock_user.id = 123456
    mock_user.login = "testuser"
    mock_user.name = "Test User"
    mock_user.email = "test@example.com"
    mock_user.avatar_url = "https://avatars.githubusercontent.com/u/123456"
    mock_user.html_url = "https://github.com/testuser"
    mock_user.dict.return_value = mock_github_user_data

    mock_email_obj = MagicMock(
        email="test@example.com", 
        primary=True, 
        verified=True
    )
    mock_email_obj.dict.return_value = {"email": "test@example.com", "primary": True, "verified": True}
    mock_emails = [mock_email_obj]

    mock_oauth.exchange_code_for_token = AsyncMock(return_value=mock_token)
    mock_oauth.get_user_info = AsyncMock(return_value=mock_user)
    mock_oauth.get_user_emails = AsyncMock(return_value=mock_emails)

    response = client.get("/auth/github/callback?code=test_code")
    print(response.text)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data
    assert data["token_type"] == "bearer"
    assert data["message"] == "OAuth login successful"

    user_data = data["user"]
    assert user_data["github_id"] == 123456
    assert user_data["username"] == "testuser"
    assert user_data["email"] == "test@example.com"


@patch("app.oauth.handlers.github_oauth")
def test_github_callback_token_exchange_error(mock_oauth, client):
    mock_oauth.exchange_code_for_token.side_effect = Exception("Token exchange failed")

    response = client.get("/auth/github/callback?code=test_code")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "OAuth process failed" in response.json()["detail"]


def test_get_oauth_user_not_authenticated(client):
    response = client.get("/auth/user")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_oauth_user_not_oauth_user(client):
    token = create_jwt_token("regular_user")

    response = client.get("/auth/user", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "OAuth user not found" in response.json()["detail"]


def test_get_oauth_user_success(client, oauth_user):
    token = create_jwt_token(oauth_user.username)

    response = client.get("/auth/user", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["github_id"] == oauth_user.github_id
    assert data["username"] == oauth_user.username
    assert data["email"] == oauth_user.email


def test_create_new_oauth_user(mock_github_user_data):
    user = create_or_update_oauth_user(mock_github_user_data)

    assert user.github_id == 123456
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert "testuser" in oauth_users
    assert github_id_to_username[123456] == "testuser"


def test_update_existing_oauth_user(oauth_user, mock_github_user_data):
    mock_github_user_data["name"] = "Updated Name"
    mock_github_user_data["email"] = "updated@example.com"

    updated_user = create_or_update_oauth_user(mock_github_user_data)

    assert updated_user.username == oauth_user.username
    assert updated_user.display_name == "Updated Name"
    assert updated_user.email == "updated@example.com"
    assert updated_user.github_id == oauth_user.github_id


def test_get_oauth_user_by_username(oauth_user):
    result = get_oauth_user_by_username("testuser")
    assert result == oauth_user

    result = get_oauth_user_by_username("nonexistent")
    assert result is None


def test_get_oauth_user_by_github_id(oauth_user):
    result = get_oauth_user_by_github_id(123456)
    assert result == oauth_user

    result = get_oauth_user_by_github_id(999999)
    assert result is None


def test_delete_oauth_user(oauth_user):
    result = delete_oauth_user("testuser")
    assert result is True
    assert "testuser" not in oauth_users
    assert 123456 not in github_id_to_username

    result = delete_oauth_user("nonexistent")
    assert result is False
