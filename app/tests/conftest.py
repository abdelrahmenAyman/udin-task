import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.db import dispose_db, engine, initialize_db
from app.main import app


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    initialize_db()
    yield
    dispose_db()
