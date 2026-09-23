"""Webhook registration, event fan-out, and reliable delivery.

Delivery is at-least-once: a receiver may see the same event more than once
(for example if it processed the request but its 200 response was lost).
Every request carries the event id in X-Webhook-Id so receivers can dedupe.
"""
import json
import random
import time
import uuid
from typing import Callable

import httpx

from . import signing
from .db import get_conn, transaction

DEFAULT_MAX_ATTEMPTS = 5
REQUEST_TIMEOUT_SECONDS = 5
BACKOFF_BASE_SECONDS = 5
BACKOFF_MAX_SECONDS = 3600

# 4xx means the receiver rejected the request itself; retrying the identical
# request will not change the answer. 408 and 429 are the exceptions: both
# describe transient conditions on the receiver side.
RETRYABLE_4XX = {408, 429}

# (url, headers, body) -> status code. Injectable so tests never hit the network.
Sender = Callable[[str, dict, bytes], int]


class EndpointNotFound(Exception):
    pass


class DeliveryNotFound(Exception):
    pass


class InvalidTransition(Exception):
    pass


def _now() -> int:
    return int(time.time())


def http_sender(url: str, headers: dict, body: bytes) -> int:
    response = httpx.post(url, content=body, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
    return response.status_code


def backoff_seconds(attempts: int) -> int:
    base = min(BACKOFF_BASE_SECONDS * (2 ** (attempts - 1)), BACKOFF_MAX_SECONDS)
    return max(1, int(base * random.uniform(0.5, 1.5)))


def is_retryable(status_code: int | None) -> bool:
    if status_code is None:  # network error or timeout
        return True
    if 400 <= status_code < 500:
        return status_code in RETRYABLE_4XX
    return True  # 5xx and anything unexpected


def _endpoint_out(row) -> dict:
    return {
        "id": row["id"], "url": row["url"],
        "event_types": json.loads(row["event_types"]),
        "active": bool(row["active"]), "created_at": row["created_at"],
    }


def create_endpoint(url: str, event_types: list[str], secret: str | None = None) -> dict:
    endpoint_id = "ep_" + uuid.uuid4().hex[:16]
    secret = secret or signing.generate_secret()
    now = _now()
    with transaction() as conn:
        conn.execute(
            "INSERT INTO endpoints (id, url, secret, event_types, active, created_at) "
            "VALUES (?, ?, ?, ?, 1, ?)",
            (endpoint_id, url, secret, json.dumps(event_types), now),
        )
    return {"id": endpoint_id, "url": url, "event_types": event_types,
            "active": True, "created_at": now, "secret": secret}


def list_endpoints() -> list[dict]:
    conn = get_conn()
    try:
        return [_endpoint_out(r) for r in conn.execute("SELECT * FROM endpoints ORDER BY created_at")]
    finally:
        conn.close()


def get_secret(endpoint_id: str) -> str | None:
    conn = get_conn()
    try:
        row = conn.execute("SELECT secret FROM endpoints WHERE id = ?", (endpoint_id,)).fetchone()
    finally:
        conn.close()
    return row["secret"] if row else None


def deactivate_endpoint(endpoint_id: str) -> dict:
    with transaction(immediate=True) as conn:
        cur = conn.execute("UPDATE endpoints SET active = 0 WHERE id = ?", (endpoint_id,))
        if cur.rowcount == 0:
            raise EndpointNotFound(endpoint_id)
        row = conn.execute("SELECT * FROM endpoints WHERE id = ?", (endpoint_id,)).fetchone()
    return _endpoint_out(row)


def _matches(event_type: str, subscribed: list[str]) -> bool:
    return "*" in subscribed or event_type in subscribed


def publish_event(event_type: str, payload: dict, now: int | None = None) -> dict:
    """Store the event and fan it out to every matching active endpoint.

    The event row and its delivery rows are written in one transaction, so an
    event is never stored without its deliveries (or vice versa).
    """
    now = now if now is not None else _now()
    event_id = "evt_" + uuid.uuid4().hex[:16]
    with transaction(immediate=True) as conn:
        conn.execute(
            "INSERT INTO events (id, type, payload, created_at) VALUES (?, ?, ?, ?)",
            (event_id, event_type, json.dumps(payload), now),
        )
        created = _fan_out(conn, event_id, event_type, now)
    return {"id": event_id, "type": event_type, "payload": payload,
            "created_at": now, "deliveries_created": created}


def _fan_out(conn, event_id: str, event_type: str, now: int) -> int:
    endpoints = conn.execute("SELECT id, event_types FROM endpoints WHERE active = 1").fetchall()
    created = 0
    for ep in endpoints:
        if not _matches(event_type, json.loads(ep["event_types"])):
            continue
        # INSERT OR IGNORE plus the UNIQUE constraint makes fan-out idempotent.
        cur = conn.execute(
            """
            INSERT OR IGNORE INTO deliveries
                (id, event_id, endpoint_id, status, attempts, max_attempts,
                 next_attempt_at, created_at, updated_at)
            VALUES (?, ?, ?, 'pending', 0, ?, ?, ?, ?)
            """,
            ("dlv_" + uuid.uuid4().hex[:16], event_id, ep["id"],
             DEFAULT_MAX_ATTEMPTS, now, now, now),
        )
        created += cur.rowcount
    return created


def refan_event(event_id: str, now: int | None = None) -> int:
    """Re-run fan-out for an existing event. Safe to call repeatedly."""
    now = now if now is not None else _now()
    with transaction(immediate=True) as conn:
        row = conn.execute("SELECT type FROM events WHERE id = ?", (event_id,)).fetchone()
        if row is None:
            return 0
        return _fan_out(conn, event_id, row["type"], now)


def list_deliveries(event_id: str) -> list[dict]:
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM deliveries WHERE event_id = ? ORDER BY created_at", (event_id,)
        ).fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]


def get_delivery(delivery_id: str) -> dict:
    conn = get_conn()
    try:
        row = conn.execute("SELECT * FROM deliveries WHERE id = ?", (delivery_id,)).fetchone()
    finally:
        conn.close()
    if row is None:
        raise DeliveryNotFound(delivery_id)
    return dict(row)


def _build_request(event, endpoint, now: int) -> tuple[dict, bytes]:
    body = json.dumps({
        "id": event["id"], "type": event["type"],
        "created_at": event["created_at"], "data": json.loads(event["payload"]),
    }, separators=(",", ":")).encode()
    headers = {
        "Content-Type": "application/json",
        "X-Webhook-Id": event["id"],            # receivers dedupe on this
        "X-Webhook-Endpoint-Id": endpoint["id"],
        "X-Webhook-Timestamp": str(now),
        "X-Webhook-Signature": signing.sign(endpoint["secret"], now, body),
    }
    return headers, body


def dispatch_once(now: int | None = None, batch_size: int = 20,
                  sender: Sender | None = None) -> dict:
    """Attempt every due delivery once.

    HTTP calls happen outside any transaction so a slow receiver cannot hold
    the database write lock.
    """
    now = now if now is not None else _now()
    sender = sender or http_sender
    summary = {"attempted": 0, "succeeded": [], "retrying": [], "dead": []}

    conn = get_conn()
    try:
        due = conn.execute(
            """
            SELECT d.id AS delivery_id, d.attempts, d.max_attempts,
                   e.id, e.type, e.payload, e.created_at,
                   p.id AS endpoint_id, p.url, p.secret, p.active
              FROM deliveries d
              JOIN events e    ON e.id = d.event_id
              JOIN endpoints p ON p.id = d.endpoint_id
             WHERE d.status = 'pending' AND d.next_attempt_at <= ?
             ORDER BY d.next_attempt_at
             LIMIT ?
            """,
            (now, batch_size),
        ).fetchall()
    finally:
        conn.close()

    for row in due:
        if not row["active"]:
            continue  # endpoint disabled after fan-out; leave pending
        endpoint = {"id": row["endpoint_id"], "secret": row["secret"]}
        headers, body = _build_request(row, endpoint, now)
        summary["attempted"] += 1

        status_code, error = None, None
        try:
            status_code = sender(row["url"], headers, body)
        except Exception as e:
            error = f"{type(e).__name__}: {e}"

        attempts = row["attempts"] + 1
        ok = status_code is not None and 200 <= status_code < 300
        if ok:
            new_status, next_at = "succeeded", now
        elif is_retryable(status_code) and attempts < row["max_attempts"]:
            new_status, next_at = "pending", now + backoff_seconds(attempts)
        else:
            new_status, next_at = "dead", now

        if error is None and not ok:
            error = f"HTTP {status_code}"

        with transaction(immediate=True) as conn:
            conn.execute(
                """
                UPDATE deliveries
                   SET status = ?, attempts = ?, next_attempt_at = ?,
                       last_status_code = ?, last_error = ?, updated_at = ?
                 WHERE id = ? AND status = 'pending'
                """,
                (new_status, attempts, next_at, status_code,
                 None if ok else error, now, row["delivery_id"]),
            )

        key = {"succeeded": "succeeded", "pending": "retrying", "dead": "dead"}[new_status]
        summary[key].append(row["delivery_id"])

    return summary


def retry_delivery(delivery_id: str, now: int | None = None) -> dict:
    now = now if now is not None else _now()
    with transaction(immediate=True) as conn:
        cur = conn.execute(
            """
            UPDATE deliveries
               SET status = 'pending', attempts = 0, next_attempt_at = ?,
                   last_error = NULL, updated_at = ?
             WHERE id = ? AND status = 'dead'
            """,
            (now, now, delivery_id),
        )
        if cur.rowcount == 0:
            row = conn.execute("SELECT status FROM deliveries WHERE id = ?",
                               (delivery_id,)).fetchone()
            if row is None:
                raise DeliveryNotFound(delivery_id)
            raise InvalidTransition(f"only dead deliveries can be retried, this one is {row['status']}")
    return get_delivery(delivery_id)
