import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

load_dotenv()

test_database_url = os.getenv("TEST_DATABASE_URL")

if not test_database_url:
    raise RuntimeError("TEST_DATABASE_URL is missing from .env")

# Make sure the application connects to the TEST database.
os.environ["DATABASE_URL"] = test_database_url
os.environ["SECRET_KEY"] = "test-secret-key-for-automated-tests"

from app.main import app
from app.database import Base, engine, get_db, SessionLocal


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def registered_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "ali",
            "email": "ali@example.com",
            "password": "SecurePass123!",
        },
    )

    assert response.status_code in (200, 201)

    login_response = client.post(
        "/auth/login",
        json={
            "email": "ali@example.com",
            "password": "SecurePass123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }