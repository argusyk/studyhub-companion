"""Дедлайни: єдине місце, де порівнюються моменти часу (розд. 10, ЛР9)."""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

DEPARTMENT_TZ = ZoneInfo("Europe/Kyiv")


def require_aware(value: datetime, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value


def local_deadline_to_utc(local_iso: str) -> datetime:
    """Дедлайн, введений викладачем за часом кафедри, переводить в UTC."""
    naive = datetime.fromisoformat(local_iso)
    return naive.replace(tzinfo=DEPARTMENT_TZ).astimezone(timezone.utc)


def is_late(submitted_at: datetime, deadline: datetime) -> bool:
    """Запізнення: строго пізніше дедлайну. Рівно в момент дедлайну – не запізнення (E2)."""
    submitted = require_aware(submitted_at, "submitted_at").astimezone(timezone.utc)
    due = require_aware(deadline, "deadline").astimezone(timezone.utc)
    return submitted > due
