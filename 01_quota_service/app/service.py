from datetime import datetime, timezone
from .database import get_conn

class QuotaNotFound(Exception):
    pass

class QuotaExceeded(Exception):
    pass

class InvalidQuotaChange(Exception):
    pass

def _now():
    return datetime.now(timezone.utc).isoformat()

def _response(row):
    return {
        "subject_id": row["subject_id"],
        "resource": row["resource"],
        "limit_amount": row["limit_amount"],
        "used": row["used"],
        "remaining": row["limit_amount"] - row["used"],
    }

def set_quota(subject_id, resource, limit_amount):
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT * FROM quotas WHERE subject_id=? AND resource=?",
            (subject_id, resource),
        ).fetchone()

        if existing and limit_amount < existing["used"]:
            raise InvalidQuotaChange("limit cannot be lower than current usage")

        conn.execute(
            """
            INSERT INTO quotas(subject_id, resource, limit_amount, used, updated_at)
            VALUES (?, ?, ?, 0, ?)
            ON CONFLICT(subject_id, resource)
            DO UPDATE SET limit_amount=excluded.limit_amount, updated_at=excluded.updated_at
            """,
            (subject_id, resource, limit_amount, _now()),
        )
        conn.commit()

        row = conn.execute(
            "SELECT * FROM quotas WHERE subject_id=? AND resource=?",
            (subject_id, resource),
        ).fetchone()
        return _response(row)

def get_quota(subject_id, resource):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM quotas WHERE subject_id=? AND resource=?",
            (subject_id, resource),
        ).fetchone()
        if not row:
            raise QuotaNotFound()
        return _response(row)

def consume(subject_id, resource, amount):
    with get_conn() as conn:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute(
            "SELECT * FROM quotas WHERE subject_id=? AND resource=?",
            (subject_id, resource),
        ).fetchone()

        if not row:
            conn.rollback()
            raise QuotaNotFound()

        if row["used"] + amount > row["limit_amount"]:
            conn.rollback()
            raise QuotaExceeded()

        conn.execute(
            "UPDATE quotas SET used=used+?, updated_at=? WHERE subject_id=? AND resource=?",
            (amount, _now(), subject_id, resource),
        )
        conn.commit()

    return get_quota(subject_id, resource)

def release(subject_id, resource, amount):
    with get_conn() as conn:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute(
            "SELECT * FROM quotas WHERE subject_id=? AND resource=?",
            (subject_id, resource),
        ).fetchone()

        if not row:
            conn.rollback()
            raise QuotaNotFound()

        new_used = max(0, row["used"] - amount)
        conn.execute(
            "UPDATE quotas SET used=?, updated_at=? WHERE subject_id=? AND resource=?",
            (new_used, _now(), subject_id, resource),
        )
        conn.commit()

    return get_quota(subject_id, resource)
