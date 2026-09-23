"""A durable task queue with leases, retries, backoff, and a dead-letter state.

State machine:
    queued --claim--> running --success--> succeeded
                         |
                         +--failure, attempts left--> queued (delayed by backoff)
                         +--failure, no attempts left--> dead
    running --lease expired--> queued      (worker crashed or hung)
    dead --manual retry--> queued

Delivery is at-least-once, so handlers must be idempotent.
"""
import json
import random
import time
import uuid

from .db import get_conn, transaction
from .handlers import HANDLERS, TaskError

LEASE_SECONDS = 30
BACKOFF_BASE_SECONDS = 2
BACKOFF_MAX_SECONDS = 300


class TaskNotFound(Exception):
    pass


class UnknownTaskType(Exception):
    pass


class InvalidTransition(Exception):
    pass


def _now() -> int:
    return int(time.time())


def _row_to_dict(row) -> dict:
    d = dict(row)
    d["payload"] = json.loads(d["payload"])
    d["result"] = json.loads(d["result"]) if d["result"] is not None else None
    d.pop("locked_until", None)
    d.pop("lease_token", None)
    return d


def backoff_seconds(attempts: int) -> int:
    """Exponential backoff with jitter: ~2s, 4s, 8s, ... capped at 300s.

    Jitter spreads retries out so that many tasks failing at the same moment
    (for example during a downstream outage) don't all retry in lockstep.
    """
    base = min(BACKOFF_BASE_SECONDS * (2 ** (attempts - 1)), BACKOFF_MAX_SECONDS)
    return max(1, int(base * random.uniform(0.5, 1.5)))


def enqueue(task_type: str, payload: dict, max_attempts: int, now: int | None = None) -> dict:
    if task_type not in HANDLERS:
        raise UnknownTaskType(task_type)
    now = now if now is not None else _now()
    task_id = str(uuid.uuid4())
    with transaction() as conn:
        conn.execute(
            """
            INSERT INTO tasks (id, type, payload, status, attempts, max_attempts,
                               next_run_at, created_at, updated_at)
            VALUES (?, ?, ?, 'queued', 0, ?, ?, ?, ?)
            """,
            (task_id, task_type, json.dumps(payload), max_attempts, now, now, now),
        )
    return get_task(task_id)


def get_task(task_id: str) -> dict:
    conn = get_conn()
    try:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    finally:
        conn.close()
    if row is None:
        raise TaskNotFound(task_id)
    return _row_to_dict(row)


def list_tasks(status: str | None = None, limit: int = 100) -> list[dict]:
    conn = get_conn()
    try:
        if status:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                (status, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
    finally:
        conn.close()
    return [_row_to_dict(r) for r in rows]


def reclaim_expired_leases(now: int) -> int:
    """Return running tasks whose lease expired to the queue.

    This is what makes a worker crash recoverable. The attempt already counted
    toward max_attempts, so a task that keeps crashing its worker still ends up
    in the dead state instead of looping forever.
    """
    with transaction(immediate=True) as conn:
        cur = conn.execute(
            """
            UPDATE tasks
               SET status = 'queued', locked_until = NULL, lease_token = NULL,
                   last_error = 'lease expired', next_run_at = ?, updated_at = ?
             WHERE status = 'running' AND locked_until < ?
               AND attempts < max_attempts
            """,
            (now, now, now),
        )
        reclaimed = cur.rowcount
        conn.execute(
            """
            UPDATE tasks
               SET status = 'dead', locked_until = NULL, lease_token = NULL,
                   last_error = 'lease expired on final attempt', updated_at = ?
             WHERE status = 'running' AND locked_until < ?
            """,
            (now, now),
        )
    return reclaimed


def claim_next(now: int) -> dict | None:
    """Atomically claim the oldest due task.

    The UPDATE re-checks status = 'queued', so even if two workers select the
    same candidate, only one UPDATE matches. The lease_token is a fencing
    token: completion must present it, so a worker that lost its lease cannot
    overwrite the result of the worker that took over.
    """
    with transaction(immediate=True) as conn:
        candidate = conn.execute(
            """
            SELECT id FROM tasks
             WHERE status = 'queued' AND next_run_at <= ?
             ORDER BY next_run_at, created_at
             LIMIT 1
            """,
            (now,),
        ).fetchone()
        if candidate is None:
            return None
        token = str(uuid.uuid4())
        cur = conn.execute(
            """
            UPDATE tasks
               SET status = 'running', attempts = attempts + 1,
                   locked_until = ?, lease_token = ?, updated_at = ?
             WHERE id = ? AND status = 'queued'
            """,
            (now + LEASE_SECONDS, token, now, candidate["id"]),
        )
        if cur.rowcount == 0:
            return None
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (candidate["id"],)).fetchone()
    task = dict(row)
    task["payload"] = json.loads(task["payload"])
    return task


def complete(task_id: str, token: str, result: dict, now: int) -> bool:
    """Record success. Returns False if the lease was lost to another worker."""
    with transaction(immediate=True) as conn:
        cur = conn.execute(
            """
            UPDATE tasks
               SET status = 'succeeded', result = ?, last_error = NULL,
                   locked_until = NULL, lease_token = NULL, updated_at = ?
             WHERE id = ? AND status = 'running' AND lease_token = ?
            """,
            (json.dumps(result), now, task_id, token),
        )
    return cur.rowcount == 1


def record_failure(task_id: str, token: str, error: str, now: int) -> str | None:
    """Record a failed attempt. Returns the new status, or None if the lease was lost."""
    with transaction(immediate=True) as conn:
        row = conn.execute(
            "SELECT attempts, max_attempts FROM tasks WHERE id = ? AND lease_token = ?",
            (task_id, token),
        ).fetchone()
        if row is None:
            return None
        if row["attempts"] >= row["max_attempts"]:
            conn.execute(
                """
                UPDATE tasks
                   SET status = 'dead', last_error = ?, locked_until = NULL,
                       lease_token = NULL, updated_at = ?
                 WHERE id = ? AND lease_token = ?
                """,
                (error, now, task_id, token),
            )
            return "dead"
        conn.execute(
            """
            UPDATE tasks
               SET status = 'queued', last_error = ?, next_run_at = ?,
                   locked_until = NULL, lease_token = NULL, updated_at = ?
             WHERE id = ? AND lease_token = ?
            """,
            (error, now + backoff_seconds(row["attempts"]), now, task_id, token),
        )
        return "queued"


def run_once(now: int | None = None, batch_size: int = 10) -> dict:
    """Reclaim expired leases, then process up to batch_size due tasks.

    Handlers run outside any database transaction. Holding the write lock
    while running arbitrary task code would block every other writer for the
    duration of the task.
    """
    now = now if now is not None else _now()
    summary = {"reclaimed": reclaim_expired_leases(now), "processed": 0,
               "succeeded": [], "retried": [], "dead": [], "lost_lease": []}

    for _ in range(batch_size):
        task = claim_next(now)
        if task is None:
            break
        summary["processed"] += 1
        handler = HANDLERS[task["type"]]
        try:
            result = handler(task["payload"], task["attempts"])
        except TaskError as e:
            outcome = record_failure(task["id"], task["lease_token"], str(e), now)
        except Exception as e:  # a handler bug is still just a failed attempt
            outcome = record_failure(
                task["id"], task["lease_token"], f"{type(e).__name__}: {e}", now
            )
        else:
            outcome = "succeeded" if complete(task["id"], task["lease_token"], result, now) else None

        bucket = {"succeeded": "succeeded", "queued": "retried", "dead": "dead", None: "lost_lease"}
        summary[bucket[outcome]].append(task["id"])

    return summary


def retry_dead(task_id: str, now: int | None = None) -> dict:
    """Manually requeue a dead task with a fresh attempt budget."""
    now = now if now is not None else _now()
    with transaction(immediate=True) as conn:
        cur = conn.execute(
            """
            UPDATE tasks
               SET status = 'queued', attempts = 0, next_run_at = ?,
                   last_error = NULL, updated_at = ?
             WHERE id = ? AND status = 'dead'
            """,
            (now, now, task_id),
        )
        if cur.rowcount == 0:
            exists = conn.execute("SELECT status FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if exists is None:
                raise TaskNotFound(task_id)
            raise InvalidTransition(f"only dead tasks can be retried, task is {exists['status']}")
    return get_task(task_id)
