import json
import time

import pytest
from fastapi.testclient import TestClient

T0 = int(time.time()) + 60


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))
    from app.main import app
    with TestClient(app) as c:
        yield c


@pytest.fixture
def svc(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "svc.db"))
    from app import service
    from app.db import init_db
    init_db()
    return service


class FakeSender:
    """Records requests and returns scripted status codes."""

    def __init__(self, *codes):
        self.codes = list(codes)
        self.calls = []

    def __call__(self, url, headers, body):
        self.calls.append({"url": url, "headers": headers, "body": body})
        code = self.codes.pop(0) if self.codes else 200
        if isinstance(code, Exception):
            raise code
        return code


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_endpoint_returns_secret_once(client):
    r = client.post("/endpoints", json={"url": "https://example.com/hook"})
    assert r.status_code == 201
    assert r.json()["secret"].startswith("whsec_")
    listed = client.get("/endpoints").json()[0]
    assert "secret" not in listed  # never shown again


def test_invalid_url_rejected(client):
    assert client.post("/endpoints", json={"url": "not-a-url"}).status_code == 422


def test_fan_out_respects_event_type_filter(client):
    client.post("/endpoints", json={"url": "https://a.com", "event_types": ["droplet.created"]})
    client.post("/endpoints", json={"url": "https://b.com", "event_types": ["volume.deleted"]})
    client.post("/endpoints", json={"url": "https://c.com"})  # wildcard
    event = client.post("/events", json={"type": "droplet.created", "payload": {"id": 1}}).json()
    assert event["deliveries_created"] == 2  # a.com and the wildcard, not b.com


def test_inactive_endpoint_gets_no_deliveries(client):
    ep = client.post("/endpoints", json={"url": "https://a.com"}).json()
    client.delete(f"/endpoints/{ep['id']}")
    event = client.post("/events", json={"type": "x"}).json()
    assert event["deliveries_created"] == 0


def test_fan_out_is_idempotent(svc):
    svc.create_endpoint("https://a.com", ["*"])
    event = svc.publish_event("x", {}, now=T0)
    assert svc.refan_event(event["id"], now=T0) == 0  # UNIQUE blocks duplicates
    assert len(svc.list_deliveries(event["id"])) == 1


def test_successful_delivery_is_signed(svc):
    ep = svc.create_endpoint("https://a.com", ["*"])
    svc.publish_event("droplet.created", {"id": 42}, now=T0)
    sender = FakeSender(200)
    summary = svc.dispatch_once(now=T0, sender=sender)
    assert len(summary["succeeded"]) == 1

    call = sender.calls[0]
    from app import signing
    ts = int(call["headers"]["X-Webhook-Timestamp"])
    assert signing.verify(ep["secret"], ts, call["body"],
                          call["headers"]["X-Webhook-Signature"], now=T0)
    assert json.loads(call["body"])["data"] == {"id": 42}


def test_5xx_retries_with_backoff_then_succeeds(svc):
    svc.create_endpoint("https://a.com", ["*"])
    event = svc.publish_event("x", {}, now=T0)
    sender = FakeSender(503, 200)

    first = svc.dispatch_once(now=T0, sender=sender)
    assert len(first["retrying"]) == 1
    delivery = svc.list_deliveries(event["id"])[0]
    assert delivery["next_attempt_at"] > T0 and delivery["last_status_code"] == 503

    assert svc.dispatch_once(now=T0, sender=sender)["attempted"] == 0  # not due yet
    later = svc.dispatch_once(now=T0 + 10_000, sender=sender)
    assert len(later["succeeded"]) == 1


def test_network_error_is_retried(svc):
    svc.create_endpoint("https://a.com", ["*"])
    svc.publish_event("x", {}, now=T0)
    summary = svc.dispatch_once(now=T0, sender=FakeSender(ConnectionError("refused")))
    assert len(summary["retrying"]) == 1


def test_non_retryable_4xx_goes_dead_immediately(svc):
    svc.create_endpoint("https://a.com", ["*"])
    svc.publish_event("x", {}, now=T0)
    summary = svc.dispatch_once(now=T0, sender=FakeSender(400))
    assert len(summary["dead"]) == 1


def test_429_is_retried(svc):
    svc.create_endpoint("https://a.com", ["*"])
    svc.publish_event("x", {}, now=T0)
    assert len(svc.dispatch_once(now=T0, sender=FakeSender(429))["retrying"]) == 1


def test_gives_up_after_max_attempts(svc):
    svc.create_endpoint("https://a.com", ["*"])
    event = svc.publish_event("x", {}, now=T0)
    sender = FakeSender(*[500] * 10)
    t = T0
    for _ in range(svc.DEFAULT_MAX_ATTEMPTS):
        svc.dispatch_once(now=t, sender=sender)
        t += 100_000
    delivery = svc.list_deliveries(event["id"])[0]
    assert delivery["status"] == "dead"
    assert delivery["attempts"] == svc.DEFAULT_MAX_ATTEMPTS


def test_dead_delivery_can_be_retried(client, monkeypatch):
    from app import service
    monkeypatch.setattr(service, "http_sender", FakeSender(400))
    client.post("/endpoints", json={"url": "https://a.com"})
    event = client.post("/events", json={"type": "x"}).json()
    client.post("/dispatcher/run-once")
    dlv = client.get(f"/events/{event['id']}/deliveries").json()[0]
    assert dlv["status"] == "dead"
    assert client.post(f"/deliveries/{dlv['id']}/retry").json()["status"] == "pending"


def test_signature_rejects_tampered_body_and_old_timestamp():
    from app import signing
    secret = "whsec_test_secret_value"
    sig = signing.sign(secret, T0, b'{"a":1}')
    assert signing.verify(secret, T0, b'{"a":1}', sig, now=T0)
    assert not signing.verify(secret, T0, b'{"a":2}', sig, now=T0)          # tampered
    assert not signing.verify(secret, T0, b'{"a":1}', sig, now=T0 + 1000)   # replayed later
    assert not signing.verify("whsec_wrong_secret_x", T0, b'{"a":1}', sig, now=T0)


def test_builtin_receiver_verifies_signature(client):
    from app import signing
    ep = client.post("/endpoints", json={"url": "https://self/receiver"}).json()
    body = b'{"id":"evt_1","type":"x","data":{}}'
    ts = int(time.time())
    good = {"x-webhook-endpoint-id": ep["id"], "x-webhook-timestamp": str(ts),
            "x-webhook-signature": signing.sign(ep["secret"], ts, body), "x-webhook-id": "evt_1"}
    assert client.post("/receiver", content=body, headers=good).status_code == 200

    bad = {**good, "x-webhook-signature": "v1=deadbeef"}
    assert client.post("/receiver", content=body, headers=bad).status_code == 401
    assert client.get("/receiver/log").json()[0]["webhook_id"] == "evt_1"
