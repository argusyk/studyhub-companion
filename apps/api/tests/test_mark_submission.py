"""Тести позначки is_late. Зверніть увагу, що перший тест ЗЕЛЕНИЙ – і саме це підозріло (ЛР9)."""
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from app.services.submissions import mark_submission

# Дедлайн 06.04.2026 23:59 за Києвом (літній час, UTC+3) = 20:59 UTC
LAB = SimpleNamespace(deadline=datetime(2026, 4, 6, 20, 59, tzinfo=timezone.utc))


def _mark(at_utc: datetime) -> bool:
    sub = SimpleNamespace(is_late=None)
    mark_submission(sub, LAB, at_utc)
    return sub.is_late


def test_mark_submission_before_deadline(monkeypatch):
    monkeypatch.delenv("SERVER_TZ", raising=False)  # як на CI: сервер у UTC
    assert _mark(datetime(2026, 4, 6, 20, 58, tzinfo=timezone.utc)) is False


def test_mark_submission_after_deadline(monkeypatch):
    monkeypatch.delenv("SERVER_TZ", raising=False)
    assert _mark(datetime(2026, 4, 6, 21, 0, tzinfo=timezone.utc)) is True


@pytest.mark.xfail(reason="ЛР9: відомий баг – сервер у Europe/Kyiv, naive-порівняння", strict=False)
def test_not_late_one_minute_before_deadline_on_kyiv_server(monkeypatch):
    monkeypatch.setenv("SERVER_TZ", "Europe/Kyiv")
    # 23:58 за Києвом = 20:58 UTC, тобто за хвилину до дедлайну
    assert _mark(datetime(2026, 4, 6, 20, 58, tzinfo=timezone.utc)) is False
