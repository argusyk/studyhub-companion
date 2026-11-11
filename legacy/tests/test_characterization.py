"""Характеризаційні тести: фіксують ФАКТИЧНУ поведінку старого коду (а не бажану)."""
import json
import os
import pathlib

import pytest

pytest.importorskip("flask")
os.environ["STUDYHUB_DB_URL"] = "sqlite:///:memory:"  # шов: тестова база

from legacy.flask_app.app import app, seed_from_fixtures  # noqa: E402

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    seed_from_fixtures(FIXTURES / "group_ki21.json")
    return app.test_client()


def test_grades_of_group_are_stable(client):
    resp = client.get("/api/groups/ki-21/grades")
    assert resp.status_code == 200
    expected = json.loads((FIXTURES / "ki21_golden.json").read_text("utf-8"))
    assert resp.get_json() == expected  # фіксуємо фактичну поведінку


def test_late_penalty_rounding(client):
    # 85 балів, 1 повний день запізнення: 85 * 0.9 = 76.5; Python round(76.5) == 76 (до парного)
    resp = client.get("/api/submissions/1042/score")
    assert resp.get_json()["final"] == 76


def test_submission_after_five_days_is_not_accepted(client):
    resp = client.get("/api/submissions/1008/score")
    assert resp.get_json()["final"] is None


def test_stats_snapshot(client):
    body = client.get("/api/groups/ki-21/stats").get_json()
    assert body == {"group": "ki-21", "submissions": 9, "avg_final": 82.38, "late_count": 3}


def test_unknown_submission_404(client):
    assert client.get("/api/submissions/999999/score").status_code == 404
