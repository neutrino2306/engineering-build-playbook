from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))
    from app.main import app
    with TestClient(app) as c:
        yield c


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_set_and_list_quota(client):
    r = client.put("/tenants/acme/quotas/droplets", json={"limit": 5})
    assert r.status_code == 200
    assert r.json() == {
        "tenant_id": "acme", "resource": "droplets",
        "limit": 5, "used": 0, "available": 5,
    }
    assert len(client.get("/tenants/acme/quotas").json()) == 1


def test_reserve_within_limit(client):
    client.put("/tenants/acme/quotas/droplets", json={"limit": 5})
    r = client.post("/tenants/acme/reservations", json={"resource": "droplets", "amount": 3})
    assert r.status_code == 201
    assert r.json()["status"] == "active"
    quota = client.get("/tenants/acme/quotas").json()[0]
    assert quota["used"] == 3 and quota["available"] == 2


def test_reserve_exceeding_limit_returns_409(client):
    client.put("/tenants/acme/quotas/droplets", json={"limit": 5})
    client.post("/tenants/acme/reservations", json={"resource": "droplets", "amount": 4})
    r = client.post("/tenants/acme/reservations", json={"resource": "droplets", "amount": 2})
    assert r.status_code == 409
    assert r.json()["detail"]["error"] == "quota_exceeded"
    # Usage must be unchanged after a rejected request.
    assert client.get("/tenants/acme/quotas").json()[0]["used"] == 4


def test_reserve_without_quota_returns_404(client):
    r = client.post("/tenants/acme/reservations", json={"resource": "volumes", "amount": 1})
    assert r.status_code == 404


def test_release_returns_capacity(client):
    client.put("/tenants/acme/quotas/droplets", json={"limit": 5})
    rid = client.post(
        "/tenants/acme/reservations", json={"resource": "droplets", "amount": 5}
    ).json()["id"]
    assert client.delete(f"/reservations/{rid}").json()["status"] == "released"
    assert client.get("/tenants/acme/quotas").json()[0]["used"] == 0


def test_release_is_idempotent(client):
    client.put("/tenants/acme/quotas/droplets", json={"limit": 5})
    rid = client.post(
        "/tenants/acme/reservations", json={"resource": "droplets", "amount": 2}
    ).json()["id"]
    client.delete(f"/reservations/{rid}")
    client.delete(f"/reservations/{rid}")  # second release must not refund again
    assert client.get("/tenants/acme/quotas").json()[0]["used"] == 0


def test_idempotency_key_prevents_double_charge(client):
    client.put("/tenants/acme/quotas/droplets", json={"limit": 5})
    headers = {"Idempotency-Key": "req-123"}
    body = {"resource": "droplets", "amount": 2}
    first = client.post("/tenants/acme/reservations", json=body, headers=headers)
    second = client.post("/tenants/acme/reservations", json=body, headers=headers)
    assert first.status_code == 201
    assert second.status_code == 200  # replay, not a new reservation
    assert first.json()["id"] == second.json()["id"]
    assert client.get("/tenants/acme/quotas").json()[0]["used"] == 2


def test_idempotency_key_reused_with_different_body_is_rejected(client):
    client.put("/tenants/acme/quotas/droplets", json={"limit": 5})
    headers = {"Idempotency-Key": "req-456"}
    client.post("/tenants/acme/reservations",
                json={"resource": "droplets", "amount": 1}, headers=headers)
    r = client.post("/tenants/acme/reservations",
                    json={"resource": "droplets", "amount": 3}, headers=headers)
    assert r.status_code == 422


def test_lowering_limit_below_usage_blocks_new_reservations(client):
    client.put("/tenants/acme/quotas/droplets", json={"limit": 5})
    client.post("/tenants/acme/reservations", json={"resource": "droplets", "amount": 4})
    client.put("/tenants/acme/quotas/droplets", json={"limit": 2})
    quota = client.get("/tenants/acme/quotas").json()[0]
    assert quota["used"] == 4 and quota["available"] == 0
    r = client.post("/tenants/acme/reservations", json={"resource": "droplets", "amount": 1})
    assert r.status_code == 409


def test_invalid_amount_rejected(client):
    client.put("/tenants/acme/quotas/droplets", json={"limit": 5})
    r = client.post("/tenants/acme/reservations", json={"resource": "droplets", "amount": 0})
    assert r.status_code == 422


def test_concurrent_reservations_never_exceed_limit(tmp_path, monkeypatch):
    """50 threads race for 10 units. Exactly 10 must succeed.

    This test calls the service layer directly with real threads and real
    SQLite connections, which is the scenario the conditional UPDATE protects.
    """
    monkeypatch.setenv("DB_PATH", str(tmp_path / "race.db"))
    from app import service
    from app.db import init_db

    init_db()
    service.set_quota("acme", "droplets", 10)

    def attempt(_):
        try:
            service.reserve("acme", "droplets", 1)
            return True
        except service.QuotaExceeded:
            return False

    with ThreadPoolExecutor(max_workers=20) as pool:
        results = list(pool.map(attempt, range(50)))

    assert sum(results) == 10
    assert service.list_quotas("acme")[0]["used"] == 10
