import time

import pytest
from fastapi.testclient import TestClient

# Tasks enqueued through the API get next_run_at = real server time. T0 must be
# at or after that, otherwise the worker sees every task as not yet due.
# (The first version used a fixed 2023 timestamp and every retry test failed.)
T0 = int(time.time()) + 60


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("ENABLE_WORKER", "false")
    from app.main import app
    with TestClient(app) as c:
        yield c


@pytest.fixture
def svc(tmp_path, monkeypatch):
    """Direct access to the service layer for lease and fencing tests."""
    monkeypatch.setenv("DB_PATH", str(tmp_path / "svc.db"))
    from app import service
    from app.db import init_db
    init_db()
    return service


def enqueue(client, task_type, payload=None, max_attempts=3):
    return client.post("/tasks", json={
        "type": task_type, "payload": payload or {}, "max_attempts": max_attempts,
    }).json()


def run(client, now=None):
    params = {"now": now} if now is not None else {}
    return client.post("/worker/run-once", params=params).json()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_enqueue_and_succeed(client):
    task = enqueue(client, "add", {"numbers": [1, 2, 3]})
    assert task["status"] == "queued"
    summary = run(client)
    assert summary["succeeded"] == [task["id"]]
    done = client.get(f"/tasks/{task['id']}").json()
    assert done["status"] == "succeeded"
    assert done["result"] == {"sum": 6}
    assert done["attempts"] == 1


def test_unknown_task_type_rejected(client):
    r = client.post("/tasks", json={"type": "nope", "payload": {}})
    assert r.status_code == 422


def test_failed_task_is_retried_later_not_immediately(client):
    task = enqueue(client, "flaky", {"succeed_on_attempt": 2}, max_attempts=3)
    first = run(client, now=T0)
    assert first["retried"] == [task["id"]]

    state = client.get(f"/tasks/{task['id']}").json()
    assert state["status"] == "queued"
    assert state["next_run_at"] > T0  # backoff pushed it into the future
    assert "simulated failure" in state["last_error"]

    # Running again at the same instant must not pick it up.
    assert run(client, now=T0)["processed"] == 0

    # After the backoff window it succeeds on attempt 2.
    later = run(client, now=T0 + 1000)
    assert later["succeeded"] == [task["id"]]
    assert client.get(f"/tasks/{task['id']}").json()["attempts"] == 2


def test_task_goes_dead_after_max_attempts(client):
    task = enqueue(client, "fail", max_attempts=2)
    run(client, now=T0)
    summary = run(client, now=T0 + 1000)
    assert summary["dead"] == [task["id"]]
    state = client.get(f"/tasks/{task['id']}").json()
    assert state["status"] == "dead" and state["attempts"] == 2


def test_dead_task_can_be_manually_retried(client):
    task = enqueue(client, "fail", max_attempts=1)
    run(client, now=T0)
    retried = client.post(f"/tasks/{task['id']}/retry").json()
    assert retried["status"] == "queued" and retried["attempts"] == 0


def test_only_dead_tasks_can_be_retried(client):
    task = enqueue(client, "echo")
    assert client.post(f"/tasks/{task['id']}/retry").status_code == 409


def test_handler_exception_counts_as_failed_attempt(client):
    task = enqueue(client, "add", {"numbers": "not a list"}, max_attempts=1)
    summary = run(client, now=T0)
    assert summary["dead"] == [task["id"]]


def test_list_by_status(client):
    enqueue(client, "echo")
    enqueue(client, "echo")
    assert len(client.get("/tasks", params={"status": "queued"}).json()) == 2


def test_expired_lease_is_reclaimed(svc):
    """A worker that crashes mid-task: its lease expires and the task is requeued."""
    task = svc.enqueue("echo", {}, 3, now=T0)
    claimed = svc.claim_next(T0)
    assert claimed["id"] == task["id"]
    # Simulate the worker dying: nobody calls complete().
    reclaimed = svc.reclaim_expired_leases(T0 + svc.LEASE_SECONDS + 1)
    assert reclaimed == 1
    assert svc.get_task(task["id"])["status"] == "queued"


def test_fencing_token_rejects_stale_worker(svc):
    """Worker A's lease expires; worker B takes over. A's late result must be discarded."""
    task = svc.enqueue("echo", {}, 3, now=T0)
    worker_a = svc.claim_next(T0)
    later = T0 + svc.LEASE_SECONDS + 1
    svc.reclaim_expired_leases(later)
    worker_b = svc.claim_next(later)
    assert worker_b["lease_token"] != worker_a["lease_token"]

    assert svc.complete(task["id"], worker_a["lease_token"], {"from": "A"}, later) is False
    assert svc.complete(task["id"], worker_b["lease_token"], {"from": "B"}, later) is True
    assert svc.get_task(task["id"])["result"] == {"from": "B"}


def test_task_that_repeatedly_crashes_worker_eventually_dies(svc):
    task = svc.enqueue("echo", {}, 2, now=T0)
    t = T0
    for _ in range(2):
        svc.claim_next(t)
        t += svc.LEASE_SECONDS + 1
        svc.reclaim_expired_leases(t)
    assert svc.get_task(task["id"])["status"] == "dead"


def test_backoff_grows_and_is_capped():
    from app.service import backoff_seconds, BACKOFF_MAX_SECONDS
    assert backoff_seconds(1) <= 3
    assert backoff_seconds(3) >= 4
    assert all(backoff_seconds(20) <= BACKOFF_MAX_SECONDS * 1.5 for _ in range(50))
