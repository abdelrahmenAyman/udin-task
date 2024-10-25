import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.db import dispose_db, engine, initialize_db
from app.main import app
from app.models import db as models


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


@pytest.fixture
def champions(session) -> list[models.Champion]:
    champions = []
    champions.append(models.Champion(name="Sylas"))
    champions.append(models.Champion(name="Yone"))
    champions.append(models.Champion(name="zed"))
    champions.append(models.Champion(name="Ahri"))

    session.add_all(champions)
    session.commit()
    return champions
