import os
import tempfile
from pathlib import Path

db = Path(tempfile.gettempdir()) / "quota_service_test.db"
if db.exists():
    db.unlink()
os.environ["DB_PATH"] = str(db)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_quota_flow():
    r = client.put("/quotas/p1/droplets", json={"limit_amount": 10})
    assert r.status_code == 200
    assert r.json()["remaining"] == 10

    r = client.post("/quotas/p1/droplets/consume", json={"amount": 7})
    assert r.status_code == 200
    assert r.json()["used"] == 7

    r = client.post("/quotas/p1/droplets/consume", json={"amount": 4})
    assert r.status_code == 429

    r = client.post("/quotas/p1/droplets/release", json={"amount": 2})
    assert r.status_code == 200
    assert r.json()["used"] == 5

def test_missing_quota():
    r = client.get("/quotas/missing/cpu")
    assert r.status_code == 404
