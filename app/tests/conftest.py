import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app import models
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


@pytest.fixture
def champions(session) -> list[models.Champion]:
    champions = []
    champions.append(models.Champion(name="Sylas"))
    champions.append(models.Champion(name="Yone"))
    champions.append(models.Champion(name="zed"))
    champions.append(models.Champion(name="Ahri"))
    champions[2].base_stats = models.BaseStats(health=500, mana=0, attack_damage=20, armor=30)
    champions[3].base_stats = models.BaseStats(health=520, mana=200, attack_damage=10, armor=25)

    session.add_all(champions)
    session.commit()
    return champions
