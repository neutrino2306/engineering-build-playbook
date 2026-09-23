import os
import tempfile
from pathlib import Path

db = Path(tempfile.gettempdir()) / "metrics_service_test.db"
if db.exists():
    db.unlink()
os.environ["DB_PATH"] = str(db)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_metric_triggers_alert_and_dedupes():
    r = client.post("/rules", json={
        "metric_name": "cpu",
        "operator": "gt",
        "threshold": 80
    })
    assert r.status_code == 201

    payload = {
        "event_id": "evt-1",
        "source": "host-1",
        "metric_name": "cpu",
        "value": 92,
        "timestamp": "2026-09-23T12:00:00Z"
    }

    r = client.post("/metrics", json=payload)
    assert r.status_code == 201

    r = client.post("/metrics", json=payload)
    assert r.status_code == 409

    r = client.get("/alerts")
    assert r.status_code == 200
    assert len(r.json()) == 1
