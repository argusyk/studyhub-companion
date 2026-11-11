from app.seed import load_seed


def _numbers(resp):
    assert resp.status_code == 200
    return [x["number"] for x in resp.json()]


def test_search_by_title(client, db):
    load_seed(db)
    assert _numbers(client.get("/api/v1/labs", params={"q": "docker"})) == [5]


def test_deadline_before_filter(client, db):
    load_seed(db)
    resp = client.get("/api/v1/labs", params={"deadline_before": "2026-03-10T00:00:00Z"})
    assert _numbers(resp) == [1, 2]


def test_pagination(client, db):
    load_seed(db)
    assert _numbers(client.get("/api/v1/labs", params={"limit": 2, "offset": 2})) == [3, 4]


def test_naive_deadline_filter_is_rejected(client, db):
    load_seed(db)
    resp = client.get("/api/v1/labs", params={"deadline_before": "2026-03-10T00:00:00"})
    assert resp.status_code == 422


def test_limit_is_bounded(client):
    assert client.get("/api/v1/labs", params={"limit": 1000}).status_code == 422
