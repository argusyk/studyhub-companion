from datetime import datetime, timezone
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest

from app.services import grading as g

KYIV = ZoneInfo("Europe/Kyiv")


def kyiv(*args):
    return datetime(*args, tzinfo=KYIV)


def test_ac1_raw_score():
    crit = [g.CriterionScore("A", Decimal(50), Decimal(8), Decimal(10)),
            g.CriterionScore("B", Decimal(50), Decimal(6), Decimal(10))]
    assert g.raw_score(crit) == Decimal("70.0")


def test_weights_must_sum_to_100():
    with pytest.raises(ValueError):
        g.raw_score([g.CriterionScore("A", Decimal(60), Decimal(1), Decimal(1))])


def test_ac2_r07_two_calendar_days():
    days = g.late_days(kyiv(2026, 3, 3, 0, 30), kyiv(2026, 3, 1, 23, 59), KYIV)
    assert days == 2
    pct = g.late_penalty_percent(days)
    assert pct == 20
    assert g.penalty_points(Decimal(70), pct) == Decimal("14.0")


def test_ac3_exactly_at_deadline_not_late():
    deadline = kyiv(2026, 3, 1, 23, 59)
    assert g.late_days(deadline, deadline, KYIV) == 0


def test_ac4_r07_cap_30_percent():
    assert g.late_penalty_percent(5) == 30
    assert g.late_penalty_percent(0) == 0


def test_e3_dst_does_not_change_day_count():
    # Перехід на літній час у Києві: 29.03.2026 (03:00 -> 04:00)
    days = g.late_days(kyiv(2026, 3, 30, 0, 30), kyiv(2026, 3, 28, 23, 59), KYIV)
    assert days == 2


def test_late_days_requires_aware_datetimes():
    with pytest.raises(ValueError):
        g.late_days(datetime(2026, 3, 3), datetime(2026, 3, 1, tzinfo=timezone.utc), KYIV)


def test_r08_round_half_up_not_bankers():
    assert g.published_score(Decimal("76.5")) == 77
    assert g.published_score(Decimal("77.5")) == 78
    assert g.round1(Decimal("0.25")) == Decimal("0.3")


def test_r09_final_not_negative():
    assert g.final_score(Decimal(10), Decimal(20)) == Decimal(0)
