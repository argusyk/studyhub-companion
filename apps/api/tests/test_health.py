def test_health(client):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_old_unprefixed_path_is_gone(client):
    assert client.get("/health").status_code == 404
