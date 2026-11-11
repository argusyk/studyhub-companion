from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest

from app.services.deadlines import is_late, local_deadline_to_utc

UTC = timezone.utc
KYIV = ZoneInfo("Europe/Kyiv")


def test_summer_deadline_is_utc_plus_3():
    assert local_deadline_to_utc("2026-04-06T23:59") == datetime(2026, 4, 6, 20, 59, tzinfo=UTC)


def test_winter_deadline_is_utc_plus_2():
    assert local_deadline_to_utc("2026-02-22T23:59") == datetime(2026, 2, 22, 21, 59, tzinfo=UTC)


def test_dst_switch_day_29_march_2026():
    assert local_deadline_to_utc("2026-03-28T23:59") == datetime(2026, 3, 28, 21, 59, tzinfo=UTC)
    assert local_deadline_to_utc("2026-03-29T23:59") == datetime(2026, 3, 29, 20, 59, tzinfo=UTC)


def test_exactly_at_deadline_is_not_late():
    due = datetime(2026, 4, 6, 20, 59, tzinfo=UTC)
    assert is_late(due, due) is False


def test_one_second_after_is_late():
    due = datetime(2026, 4, 6, 20, 59, tzinfo=UTC)
    assert is_late(datetime(2026, 4, 6, 20, 59, 1, tzinfo=UTC), due) is True


def test_same_instant_in_different_zones_is_not_late():
    due = datetime(2026, 4, 6, 20, 59, tzinfo=UTC)
    assert is_late(datetime(2026, 4, 6, 23, 59, tzinfo=KYIV), due) is False


def test_naive_values_are_rejected():
    due = datetime(2026, 4, 6, 20, 59, tzinfo=UTC)
    with pytest.raises(ValueError, match="timezone-aware"):
        is_late(datetime(2026, 4, 6, 23, 58), due)
    with pytest.raises(ValueError, match="timezone-aware"):
        is_late(due, datetime(2026, 4, 6, 20, 59))
