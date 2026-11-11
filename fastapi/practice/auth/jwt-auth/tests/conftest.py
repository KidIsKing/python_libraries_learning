import pytest
from fastapi.testclient import TestClient
from main import app
from app.auth import blacklisted_tokens


@pytest.fixture(autouse=True)
def clear_blacklisted_tokens():
    blacklisted_tokens.clear()
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def login_user(client):
    response = client.post(
        "/login",
        json={"username": "admin", "password": "password"}
    )
    return response


@pytest.fixture
def auth_headers(login_user):
    token = login_user.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
