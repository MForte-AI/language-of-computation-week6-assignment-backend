"""Tests that run without a live database by swapping in fake sessions."""

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.database import get_db
from app.main import app

client = TestClient(app)


class WorkingSession:
    def execute(self, statement):
        return None


class BrokenSession:
    def execute(self, statement):
        raise OperationalError("SELECT 1", {}, Exception("connection refused"))


def use_session(session):
    app.dependency_overrides[get_db] = lambda: session


def teardown_function():
    app.dependency_overrides.clear()


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Week 6 backend is running"}


def test_health_when_database_is_up():
    use_session(WorkingSession())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}


def test_health_when_database_is_down():
    use_session(BrokenSession())
    response = client.get("/health")
    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
