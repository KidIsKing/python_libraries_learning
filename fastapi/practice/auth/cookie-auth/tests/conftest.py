import pytest
from fastapi.testclient import TestClient
from main import app
from app.auth import active_sessions


@pytest.fixture(autouse=True)
def clear_session():
    active_sessions.clear()
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
