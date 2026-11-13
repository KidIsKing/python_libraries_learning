import pytest
from fastapi.testclient import TestClient
from main import app
from app.auth import blacklisted_tokens, refresh_tokens


@pytest.fixture(autouse=True)
def clear_token_stores():
    blacklisted_tokens.clear()
    refresh_tokens.clear()
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def login_user(client):
    response = client.post("/login", json={"username": "admin", "password": "password"})
    return response


@pytest.fixture
def auth_headers(login_user):
    token = login_user.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def refresh_token(login_user):
    return login_user.json()["refresh_token"]
