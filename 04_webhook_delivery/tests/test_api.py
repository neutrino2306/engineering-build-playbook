import os
import tempfile
from pathlib import Path

db = Path(tempfile.gettempdir()) / "webhook_test.db"
if db.exists():
    db.unlink()
os.environ["DB_PATH"] = str(db)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_success_and_duplicate_event():
    r = client.post("/subscriptions", json={
        "event_type": "user.created",
        "target_url": "mock://success"
    })
    assert r.status_code == 201

    payload = {
        "event_id": "evt-1",
        "event_type": "user.created",
        "payload": {"user_id": 123}
    }

    r = client.post("/events", json=payload)
    assert r.status_code == 201
    assert r.json()[0]["status"] == "delivered"

    r = client.post("/events", json=payload)
    assert r.status_code == 409

def test_failed_delivery_can_retry():
    client.post("/subscriptions", json={
        "event_type": "payment.failed",
        "target_url": "mock://fail"
    })

    r = client.post("/events", json={
        "event_id": "evt-fail",
        "event_type": "payment.failed",
        "payload": {"amount": 10}
    })

    delivery = r.json()[0]
    assert delivery["status"] == "failed"

    r = client.post(f"/deliveries/{delivery['id']}/retry")
    assert r.status_code == 200
    assert r.json()["attempts"] == 2
