"""Міграції Alembic узгоджені з моделями (перевірка на тимчасовому SQLite)."""
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from app.db import Base

API_DIR = __import__("pathlib").Path(__file__).resolve().parents[1]


def _upgrade(tmp_path, monkeypatch):
    url = f"sqlite:///{(tmp_path / 'mig.sqlite3').as_posix()}"
    monkeypatch.setenv("ALEMBIC_DATABASE_URL", url)
    cfg = Config(str(API_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(API_DIR / "alembic"))
    command.upgrade(cfg, "head")
    return cfg, create_engine(url)


def test_upgrade_creates_students_and_labs(tmp_path, monkeypatch):
    _, engine = _upgrade(tmp_path, monkeypatch)
    assert {"students", "labs"} <= set(inspect(engine).get_table_names())


@pytest.mark.xfail(reason="ЛР5: додайте міграцію 0002_submissions", strict=False)
def test_migrations_cover_all_models(tmp_path, monkeypatch):
    _, engine = _upgrade(tmp_path, monkeypatch)
    migrated = set(inspect(engine).get_table_names()) - {"alembic_version"}
    assert migrated == set(Base.metadata.tables)
