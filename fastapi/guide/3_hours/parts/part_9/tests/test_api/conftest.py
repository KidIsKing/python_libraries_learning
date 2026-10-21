from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi.testclient import TestClient
import pytest
from main import app
from app.database import Base
from app.dependency import get_db


TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def get_test_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture()  # В тестовых функциях будет подтягиваться эта фикстура
def client():
    yield TestClient(app)


@pytest.fixture(autouse=True)  # Запускаем автоматически для всех функций тестов
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield  # Передача запущенному тесту созданной базы во время выполнения фикстуры
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
