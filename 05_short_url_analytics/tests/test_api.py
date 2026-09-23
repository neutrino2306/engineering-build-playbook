import os
import tempfile
from pathlib import Path

db = Path(tempfile.gettempdir()) / "short_url_test.db"
if db.exists():
    db.unlink()
os.environ["DB_PATH"] = str(db)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, follow_redirects=False)

def test_create_redirect_and_stats():
    r = client.post(
        "/links",
        json={"target_url": "https://example.com/hello"},
    )
    assert r.status_code == 201
    code = r.json()["code"]

    r = client.get(
        f"/{code}",
        headers={"user-agent": "pytest"},
    )
    assert r.status_code == 307
    assert r.headers["location"].startswith("https://example.com/hello")

    r = client.get(f"/links/{code}/stats")
    assert r.status_code == 200
    assert r.json()["click_count"] == 1
    assert len(r.json()["recent_clicks"]) == 1

def test_unknown_link():
    r = client.get("/nope")
    assert r.status_code == 404
