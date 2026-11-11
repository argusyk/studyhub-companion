"""Захист від помилки з Додатка Б: `exports/` без слеша ховає apps/api/app/exports/ (розд. 13)."""
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git не знайдено")


def ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT).returncode == 0


@pytest.mark.parametrize("path", [
    "apps/api/app/exports/csv.py",
    "apps/api/tests/exports/test_exports_csv.py",
    "apps/api/app/exports/__init__.py",
])
def test_code_directories_named_exports_are_tracked(path):
    assert not ignored(path)


@pytest.mark.parametrize("path", ["exports/grades.csv", "data/exports/dump.csv", ".env", "dumps/x.sql"])
def test_data_and_secrets_are_ignored(path):
    assert ignored(path)


def test_env_example_is_tracked():
    assert not ignored(".env.example")
