"""Міграції Alembic узгоджені з моделями (перевірка на тимчасовому SQLite)."""
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from app.db import Base

API_DIR = Path(__file__).resolve().parents[1]


def _config(tmp_path, monkeypatch):
    url = f"sqlite:///{(tmp_path / 'mig.sqlite3').as_posix()}"
    monkeypatch.setenv("ALEMBIC_DATABASE_URL", url)
    cfg = Config(str(API_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(API_DIR / "alembic"))
    return cfg, create_engine(url)


def test_migrations_cover_all_models(tmp_path, monkeypatch):
    cfg, engine = _config(tmp_path, monkeypatch)
    command.upgrade(cfg, "head")
    migrated = set(inspect(engine).get_table_names()) - {"alembic_version"}
    assert migrated == set(Base.metadata.tables)


def test_columns_match_models(tmp_path, monkeypatch):
    cfg, engine = _config(tmp_path, monkeypatch)
    command.upgrade(cfg, "head")
    insp = inspect(engine)
    for name, table in Base.metadata.tables.items():
        assert {c["name"] for c in insp.get_columns(name)} == {c.name for c in table.columns}, name


def test_downgrade_is_reversible(tmp_path, monkeypatch):
    cfg, engine = _config(tmp_path, monkeypatch)
    command.upgrade(cfg, "head")
    command.downgrade(cfg, "base")
    assert set(inspect(engine).get_table_names()) <= {"alembic_version"}
