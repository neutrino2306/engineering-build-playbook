import os
import tempfile
from pathlib import Path

db = Path(tempfile.gettempdir()) / "job_queue_test.db"
if db.exists():
    db.unlink()
os.environ["DB_PATH"] = str(db)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_success_job():
    r = client.post("/jobs", json={
        "task_type": "sum",
        "payload": {"numbers": [1, 2, 3]},
        "max_attempts": 3
    })
    assert r.status_code == 202
    job_id = r.json()["id"]

    r = client.get(f"/jobs/{job_id}")
    assert r.status_code == 200
    assert r.json()["status"] == "succeeded"
    assert r.json()["result"]["sum"] == 6

def test_failed_job_can_retry_until_limit():
    r = client.post("/jobs", json={
        "task_type": "fail",
        "payload": {},
        "max_attempts": 2
    })
    job_id = r.json()["id"]

    r = client.get(f"/jobs/{job_id}")
    assert r.json()["status"] == "failed"
    assert r.json()["attempts"] == 1

    r = client.post(f"/jobs/{job_id}/retry")
    assert r.status_code == 202

    r = client.get(f"/jobs/{job_id}")
    assert r.json()["status"] == "failed"
    assert r.json()["attempts"] == 2

    r = client.post(f"/jobs/{job_id}/retry")
    assert r.status_code == 409
