"""Business logic for quota enforcement.

The core invariant is: for every (tenant, resource), used <= limit.
It is enforced by a conditional UPDATE, so it holds even under concurrent
requests, and it would continue to hold across multiple app instances once
the storage moves to a shared database.
"""
import uuid
from datetime import datetime, timezone

from .db import transaction, get_conn


class QuotaNotFound(Exception):
    pass


class QuotaExceeded(Exception):
    def __init__(self, limit: int, used: int, requested: int):
        self.limit = limit
        self.used = used
        self.requested = requested
        super().__init__(f"requested {requested}, available {limit - used}")


class ReservationNotFound(Exception):
    pass


class IdempotencyConflict(Exception):
    """Same idempotency key reused with a different request body."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _quota_row_to_dict(row) -> dict:
    return {
        "tenant_id": row["tenant_id"],
        "resource": row["resource"],
        "limit": row["limit_value"],
        "used": row["used"],
        "available": max(row["limit_value"] - row["used"], 0),
    }


def set_quota(tenant_id: str, resource: str, limit: int) -> dict:
    """Create or update a quota limit.

    Lowering the limit below current usage is allowed: existing reservations
    are kept, and new reservations are blocked until usage drops. Forcibly
    revoking resources is a product decision, not something this service does.
    """
    with transaction(immediate=True) as conn:
        conn.execute(
            """
            INSERT INTO quotas (tenant_id, resource, limit_value, used, updated_at)
            VALUES (?, ?, ?, 0, ?)
            ON CONFLICT (tenant_id, resource)
            DO UPDATE SET limit_value = excluded.limit_value,
                          updated_at  = excluded.updated_at
            """,
            (tenant_id, resource, limit, _now()),
        )
        row = conn.execute(
            "SELECT * FROM quotas WHERE tenant_id = ? AND resource = ?",
            (tenant_id, resource),
        ).fetchone()
    return _quota_row_to_dict(row)


def list_quotas(tenant_id: str) -> list[dict]:
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM quotas WHERE tenant_id = ? ORDER BY resource",
            (tenant_id,),
        ).fetchall()
    finally:
        conn.close()
    return [_quota_row_to_dict(r) for r in rows]


def reserve(tenant_id: str, resource: str, amount: int,
            idempotency_key: str | None = None) -> tuple[dict, bool]:
    """Reserve units of a resource. Returns (reservation, replayed).

    replayed=True means this idempotency key was already processed and the
    original reservation is being returned without charging quota again.
    """
    reservation_id = idempotency_key or str(uuid.uuid4())

    with transaction(immediate=True) as conn:
        existing = conn.execute(
            "SELECT * FROM reservations WHERE id = ?", (reservation_id,)
        ).fetchone()
        if existing is not None:
            same_request = (
                existing["tenant_id"] == tenant_id
                and existing["resource"] == resource
                and existing["amount"] == amount
            )
            if not same_request:
                raise IdempotencyConflict(reservation_id)
            return dict(existing), True

        # The check lives inside the UPDATE, so it is evaluated atomically.
        # Two concurrent requests cannot both pass it.
        cur = conn.execute(
            """
            UPDATE quotas
               SET used = used + ?, updated_at = ?
             WHERE tenant_id = ? AND resource = ?
               AND used + ? <= limit_value
            """,
            (amount, _now(), tenant_id, resource, amount),
        )
        if cur.rowcount == 0:
            # Either the quota does not exist or it would be exceeded.
            quota = conn.execute(
                "SELECT * FROM quotas WHERE tenant_id = ? AND resource = ?",
                (tenant_id, resource),
            ).fetchone()
            if quota is None:
                raise QuotaNotFound(f"{tenant_id}/{resource}")
            raise QuotaExceeded(quota["limit_value"], quota["used"], amount)

        created_at = _now()
        conn.execute(
            """
            INSERT INTO reservations (id, tenant_id, resource, amount, status, created_at)
            VALUES (?, ?, ?, ?, 'active', ?)
            """,
            (reservation_id, tenant_id, resource, amount, created_at),
        )

    return {
        "id": reservation_id,
        "tenant_id": tenant_id,
        "resource": resource,
        "amount": amount,
        "status": "active",
        "created_at": created_at,
        "released_at": None,
    }, False


def release(reservation_id: str) -> dict:
    """Release a reservation. Releasing twice is a no-op (idempotent)."""
    with transaction(immediate=True) as conn:
        row = conn.execute(
            "SELECT * FROM reservations WHERE id = ?", (reservation_id,)
        ).fetchone()
        if row is None:
            raise ReservationNotFound(reservation_id)
        if row["status"] == "released":
            return dict(row)

        # max(..., 0) guards against usage going negative if data was ever
        # corrupted; the CHECK constraint would otherwise reject the update.
        conn.execute(
            """
            UPDATE quotas
               SET used = max(used - ?, 0), updated_at = ?
             WHERE tenant_id = ? AND resource = ?
            """,
            (row["amount"], _now(), row["tenant_id"], row["resource"]),
        )
        released_at = _now()
        conn.execute(
            "UPDATE reservations SET status = 'released', released_at = ? WHERE id = ?",
            (released_at, reservation_id),
        )

    result = dict(row)
    result["status"] = "released"
    result["released_at"] = released_at
    return result
