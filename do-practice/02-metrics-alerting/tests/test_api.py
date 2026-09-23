import pytest
from fastapi.testclient import TestClient

# Fixed reference time, aligned to an hour boundary. Buckets are aligned to
# the Unix epoch (ts / bucket * bucket), not to the query start, so an
# unaligned T0 would split points across buckets unpredictably.
T0 = 1_700_000_000 // 3600 * 3600


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))
    from app.main import app
    with TestClient(app) as c:
        yield c


def push(client, values, start=T0, step=10, resource="droplet-1", name="cpu"):
    points = [
        {"resource_id": resource, "name": name, "value": v, "ts": start + i * step}
        for i, v in enumerate(values)
    ]
    return client.post("/metrics", json={"points": points})


def make_rule(client, threshold=80.0, window=60, comparator="gt"):
    return client.post("/alert-rules", json={
        "resource_id": "droplet-1", "metric_name": "cpu",
        "comparator": comparator, "threshold": threshold, "window_seconds": window,
    }).json()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_ingest_and_bucketed_query(client):
    push(client, [10, 20, 30, 40, 50, 60], step=10)  # 6 points over 60s
    r = client.get("/metrics", params={
        "resource_id": "droplet-1", "name": "cpu",
        "start": T0, "end": T0 + 60, "bucket_seconds": 30,
    })
    buckets = r.json()
    assert len(buckets) == 2
    assert buckets[0]["value"] == pytest.approx(20.0)  # avg(10,20,30)
    assert buckets[1]["value"] == pytest.approx(50.0)  # avg(40,50,60)
    assert buckets[0]["count"] == 3


def test_query_max_aggregation(client):
    push(client, [10, 90, 30], step=10)
    r = client.get("/metrics", params={
        "resource_id": "droplet-1", "name": "cpu", "start": T0, "end": T0 + 60,
        "bucket_seconds": 60, "agg": "max",
    })
    assert r.json()[0]["value"] == 90


def test_non_finite_value_rejected(client):
    # JSON has no NaN literal, but Python's json module emits one; the
    # validator must still reject it.
    r = client.post(
        "/metrics",
        content='{"points": [{"resource_id": "d", "name": "cpu", "value": NaN}]}',
        headers={"content-type": "application/json"},
    )
    assert r.status_code == 422


def test_far_future_timestamp_rejected_but_batch_partially_accepted(client):
    import time
    now = int(time.time())
    r = client.post("/metrics", json={"points": [
        {"resource_id": "d", "name": "cpu", "value": 1, "ts": now},
        {"resource_id": "d", "name": "cpu", "value": 2, "ts": now + 10_000},
    ]})
    assert r.json()["accepted"] == 1
    assert r.json()["rejected"] == 1


def test_alert_fires_on_breach(client):
    rule = make_rule(client, threshold=80, window=60)
    push(client, [90, 95, 92], start=T0, step=10)
    result = client.post("/alerts/evaluate", params={"now": T0 + 30}).json()
    assert len(result["fired"]) == 1
    firing = client.get("/alerts", params={"state": "firing"}).json()
    assert firing[0]["rule_id"] == rule["id"]


def test_sustained_breach_does_not_duplicate_alert(client):
    make_rule(client, threshold=80, window=60)
    push(client, [90] * 10, start=T0, step=10)
    client.post("/alerts/evaluate", params={"now": T0 + 30})
    second = client.post("/alerts/evaluate", params={"now": T0 + 60}).json()
    assert second["fired"] == []
    assert len(client.get("/alerts").json()) == 1


def test_alert_resolves_when_metric_recovers(client):
    make_rule(client, threshold=80, window=30)
    push(client, [90, 90, 90], start=T0, step=10)
    client.post("/alerts/evaluate", params={"now": T0 + 20})
    push(client, [40, 40, 40], start=T0 + 100, step=10)
    result = client.post("/alerts/evaluate", params={"now": T0 + 120}).json()
    assert len(result["resolved"]) == 1
    assert client.get("/alerts", params={"state": "firing"}).json() == []


def test_no_data_does_not_resolve_firing_alert(client):
    make_rule(client, threshold=80, window=30)
    push(client, [90, 90], start=T0, step=10)
    client.post("/alerts/evaluate", params={"now": T0 + 10})
    # An hour later nothing has been reported: the agent may be dead.
    result = client.post("/alerts/evaluate", params={"now": T0 + 3600}).json()
    assert result["no_data"] and result["resolved"] == []
    assert len(client.get("/alerts", params={"state": "firing"}).json()) == 1


def test_lt_comparator(client):
    make_rule(client, threshold=10, window=60, comparator="lt")
    push(client, [2, 3, 1], start=T0, step=10)
    assert len(client.post("/alerts/evaluate", params={"now": T0 + 30}).json()["fired"]) == 1


def test_brief_spike_averaged_out(client):
    """A single spike inside a healthy window should not fire (avg-based rule)."""
    make_rule(client, threshold=80, window=60)
    push(client, [20, 20, 99, 20, 20], start=T0, step=10)
    assert client.post("/alerts/evaluate", params={"now": T0 + 50}).json()["fired"] == []
