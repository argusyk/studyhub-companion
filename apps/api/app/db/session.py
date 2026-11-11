from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings


@lru_cache
def get_engine() -> Engine:
    url = get_settings().database_url
    kwargs = {"connect_args": {"check_same_thread": False}} if url.startswith("sqlite") else {}
    return create_engine(url, **kwargs)


def get_session() -> Iterator[Session]:
    """Залежність FastAPI: одна сесія на запит."""
    with sessionmaker(bind=get_engine(), expire_on_commit=False)() as session:
        yield session
