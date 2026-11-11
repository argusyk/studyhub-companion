import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401  (реєструє моделі в Base.metadata)
from app.db import Base, get_session
from app.main import app


@pytest.fixture
def engine():
    eng = create_engine("sqlite://", connect_args={"check_same_thread": False},
                        poolclass=StaticPool)
    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()


@pytest.fixture
def db(engine) -> Session:
    with sessionmaker(bind=engine, expire_on_commit=False)() as session:
        yield session


@pytest.fixture
def client(engine):
    factory = sessionmaker(bind=engine, expire_on_commit=False)

    def _override():
        with factory() as session:
            yield session

    app.dependency_overrides[get_session] = _override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
