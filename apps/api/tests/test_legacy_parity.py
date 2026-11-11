"""Паритет нової реалізації зі знімком legacy. Відмінності – лише задокументовані (docs/legacy-diff.md)."""
import json
from pathlib import Path

import pytest

from app.testing import FIXTURE, seed_db

GOLDEN = json.loads((FIXTURE.parent / "ki21_golden.json").read_text("utf-8"))

# (студент, лабораторна) -> (legacy final, нова політика R-07 final)
INTENDED_DIFFS = {
    ("Іваненко О. П.", 3): (76, 68),   # 1 повний день -> 2 календарні доби; 85 - 20 % = 68
    ("Шевченко А. І.", 2): (67, 59),   # 74 - 20 % = 59,2 -> 59
    ("Бондаренко Д. С.", 3): (None, 49),  # legacy не приймав після 5 днів; нове: стеля 30 %
}


@pytest.fixture
def seeded(db):
    seed_db(db)


def test_new_endpoint_matches_legacy_except_documented_diffs(client, seeded):
    new = client.get("/api/v1/groups/ki-21/grades").json()
    assert new["group"] == GOLDEN["group"]
    assert len(new["grades"]) == len(GOLDEN["grades"])
    for old, cur in zip(GOLDEN["grades"], new["grades"]):
        key = (old["student"], old["lab"])
        assert (cur["student"], cur["lab"], cur["raw"]) == (old["student"], old["lab"], old["raw"])
        if key in INTENDED_DIFFS:
            assert (old["final"], cur["final"]) == INTENDED_DIFFS[key], key
        else:
            assert cur["final"] == old["final"] and cur["late_days"] == old["late_days"], key


def test_score_endpoint_for_1042(client, seeded):
    body = client.get("/api/v1/submissions/1042/score").json()
    assert body == {"id": 1042, "raw": 85, "final": 68, "late_days": 2}


def test_stats(client, seeded):
    body = client.get("/api/v1/groups/ki-21/stats").json()
    assert body["submissions"] == 9 and body["late_count"] == 3


def test_unknown_group_404(client, seeded):
    assert client.get("/api/v1/groups/xx-99/grades").status_code == 404
