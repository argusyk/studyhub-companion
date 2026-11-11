import pytest

from app import storage
from app.seed import load_seed


@pytest.fixture(autouse=True)
def _uploads(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "UPLOAD_ROOT", tmp_path / "uploads")


def _post(client, lab_id=1, student_id=1, name="report.pdf", data=b"%PDF-1.4 test"):
    return client.post(f"/api/v1/labs/{lab_id}/submissions", data={"student_id": student_id},
                       files={"file": (name, data, "application/pdf")})


def test_submit_creates_record_and_file(client, db, tmp_path):
    load_seed(db)
    resp = _post(client)
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "submitted" and body["score"] is None
    assert body["size_bytes"] == len(b"%PDF-1.4 test")
    assert (tmp_path / "uploads" / "1" / "1" / "report.pdf").exists()
    assert client.get(f"/api/v1/submissions/{body['id']}").json()["id"] == body["id"]


def test_empty_file_400(client, db):
    load_seed(db)
    assert _post(client, data=b"").status_code == 400


def test_too_big_413(client, db):
    load_seed(db)
    assert _post(client, data=b"x" * (10 * 1024 * 1024 + 1)).status_code == 413


def test_path_traversal_name_rejected(client, db):
    load_seed(db)
    assert _post(client, name="../evil.pdf").status_code == 422


def test_unknown_lab_404(client, db):
    load_seed(db)
    assert _post(client, lab_id=99).status_code == 404


def test_unknown_student_404(client, db):
    load_seed(db)
    assert _post(client, student_id=99).status_code == 404
