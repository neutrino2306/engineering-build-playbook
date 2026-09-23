import json
import uuid
from datetime import datetime, timezone
from .database import get_conn

class JobNotFound(Exception):
    pass

class RetryNotAllowed(Exception):
    pass

def _now():
    return datetime.now(timezone.utc).isoformat()

def _decode(row):
    if not row:
        raise JobNotFound()

    data = dict(row)
    data["payload"] = json.loads(data["payload"])
    data["result"] = json.loads(data["result"]) if data["result"] else None
    return data

def create_job(task_type, payload, max_attempts):
    job_id = str(uuid.uuid4())
    now = _now()

    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO jobs(
                id, task_type, payload, status, attempts, max_attempts,
                created_at, updated_at
            )
            VALUES (?, ?, ?, 'queued', 0, ?, ?, ?)
            """,
            (job_id, task_type, json.dumps(payload), max_attempts, now, now),
        )
        conn.commit()

    return get_job(job_id)

def get_job(job_id):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM jobs WHERE id=?",
            (job_id,),
        ).fetchone()
        return _decode(row)

def mark_running(job_id):
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE jobs
            SET status='running', attempts=attempts+1, updated_at=?
            WHERE id=?
            """,
            (_now(), job_id),
        )
        conn.commit()

def mark_succeeded(job_id, result):
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE jobs
            SET status='succeeded', result=?, last_error=NULL, updated_at=?
            WHERE id=?
            """,
            (json.dumps(result), _now(), job_id),
        )
        conn.commit()

def mark_failed(job_id, error):
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE jobs
            SET status='failed', last_error=?, updated_at=?
            WHERE id=?
            """,
            (error, _now(), job_id),
        )
        conn.commit()

def retry_job(job_id):
    job = get_job(job_id)

    if job["status"] != "failed" or job["attempts"] >= job["max_attempts"]:
        raise RetryNotAllowed()

    with get_conn() as conn:
        conn.execute(
            """
            UPDATE jobs
            SET status='queued', last_error=NULL, updated_at=?
            WHERE id=?
            """,
            (_now(), job_id),
        )
        conn.commit()

    return get_job(job_id)
