from datetime import datetime, timezone

import pytest
from sqlalchemy import select

from app import storage
from app.models import Lab, Submission
from app.seed import load_seed

RUBRIC = {"criteria": [
    {"name": "Функціональність", "weight": 50, "score": 8, "max_score": 10},
    {"name": "Звіт", "weight": 50, "score": 6, "max_score": 10},
]}


@pytest.fixture
def sub(db):
    load_seed(db)
    lab = db.scalar(select(Lab).where(Lab.number == 1))
    # дедлайн лаб. 1: 22.02.2026 23:59 Київ; здача 24.02.2026 00:30 Київ (UTC+2) = 23.02 22:30 UTC
    s = Submission(student_id=1, lab_id=lab.id, file_url="x", filename="a.pdf", size_bytes=1,
                   submitted_at=datetime(2026, 2, 23, 22, 30, tzinfo=timezone.utc))
    db.add(s)
    db.commit()
    return s


def test_grade_with_penalty_and_publish(client, sub):
    resp = client.put(f"/api/v1/submissions/{sub.id}/grade", json=RUBRIC | {"publish": True})
    assert resp.status_code == 200
    body = resp.json()
    assert body["raw_score"] == 70.0 and body["late_days"] == 2
    assert body["penalty_percent"] == 20 and body["penalty"] == 14.0
    assert body["final_score"] == 56.0 and body["status"] == "final"
    assert client.get(f"/api/v1/submissions/{sub.id}").json()["score"] == 56


def test_draft_does_not_publish_score(client, sub):
    client.put(f"/api/v1/submissions/{sub.id}/grade", json=RUBRIC)
    assert client.get(f"/api/v1/submissions/{sub.id}").json()["score"] is None
    assert client.get(f"/api/v1/submissions/{sub.id}/grade").json()["status"] == "draft"


def test_bad_weights_422(client, sub):
    bad = {"criteria": [{"name": "A", "weight": 60, "score": 1, "max_score": 1}]}
    assert client.put(f"/api/v1/submissions/{sub.id}/grade", json=bad).status_code == 422


def test_unknown_submission_404(client):
    assert client.put("/api/v1/submissions/99/grade", json=RUBRIC).status_code == 404
