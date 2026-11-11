from app.seed import load_seed


def test_list_labs_returns_seeded_labs_in_order(client, db):
    load_seed(db)
    resp = client.get("/api/v1/labs")
    assert resp.status_code == 200
    numbers = [lab["number"] for lab in resp.json()]
    assert numbers == sorted(numbers) and len(numbers) == 6


def test_get_lab_404(client):
    assert client.get("/api/v1/labs/999").status_code == 404


def test_deadline_is_returned_in_utc(client, db):
    load_seed(db)
    lab3 = client.get("/api/v1/labs").json()[2]
    # 29.03.2026 23:59 за Києвом (вже літній час, UTC+3) = 20:59 UTC
    assert lab3["deadline"].startswith("2026-03-29T20:59")
