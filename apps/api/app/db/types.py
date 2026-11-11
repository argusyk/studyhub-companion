"""Тип «завжди UTC»: відмовляється від naive datetime і повертає aware-значення.

PostgreSQL (timestamptz) і SQLite (у тестах) поводяться по-різному: SQLite забуває
часовий пояс. Цей тип вирівнює поведінку, щоб тести не брехали про часові пояси.
"""
from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator


class UtcDateTime(TypeDecorator):
    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(self, value: datetime | None, dialect):
        if value is None:
            return None
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("naive datetime заборонено: передайте aware-значення")
        return value.astimezone(timezone.utc)

    def process_result_value(self, value: datetime | None, dialect):
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
