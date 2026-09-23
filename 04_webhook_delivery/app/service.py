import json
import sqlite3
from datetime import datetime, timezone
from .database import get_conn
from . import client

class DuplicateEvent(Exception):
    pass

class DeliveryNotFound(Exception):
    pass

class RetryNotAllowed(Exception):
    pass

def _now():
    return datetime.now(timezone.utc).isoformat()

def create_subscription(event_type, target_url):
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO subscriptions(event_type, target_url) VALUES (?, ?)",
            (event_type, target_url),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM subscriptions WHERE id=?",
            (cur.lastrowid,),
        ).fetchone()
        return dict(row)
    finally:
        conn.close()

def _attempt_delivery(delivery_id, payload):
    conn = get_conn()
    try:
        delivery = conn.execute(
            "SELECT * FROM deliveries WHERE id=?",
            (delivery_id,),
        ).fetchone()

        if not delivery:
            raise DeliveryNotFound()

        status_code, error = client.deliver(delivery["target_url"], payload)
        status = "delivered" if error is None and 200 <= status_code < 300 else "failed"

        conn.execute(
            """
            UPDATE deliveries
            SET attempts=attempts+1, status=?, response_code=?, last_error=?
            WHERE id=?
            """,
            (status, status_code or None, error, delivery_id),
        )
        conn.commit()
    finally:
        conn.close()

def dispatch_event(event_id, event_type, payload):
    conn = get_conn()
    try:
        try:
            conn.execute(
                """
                INSERT INTO events(event_id, event_type, payload, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (event_id, event_type, json.dumps(payload), _now()),
            )
        except sqlite3.IntegrityError as exc:
            raise DuplicateEvent() from exc

        subscriptions = conn.execute(
            "SELECT * FROM subscriptions WHERE event_type=?",
            (event_type,),
        ).fetchall()

        delivery_ids = []
        for sub in subscriptions:
            cur = conn.execute(
                """
                INSERT INTO deliveries(
                    event_id, subscription_id, target_url, status, attempts
                )
                VALUES (?, ?, ?, 'pending', 0)
                """,
                (event_id, sub["id"], sub["target_url"]),
            )
            delivery_ids.append(cur.lastrowid)

        conn.commit()
    finally:
        conn.close()

    for delivery_id in delivery_ids:
        _attempt_delivery(delivery_id, payload)

    return list_deliveries(event_id)

def list_deliveries(event_id=None):
    conn = get_conn()
    try:
        if event_id:
            rows = conn.execute(
                "SELECT * FROM deliveries WHERE event_id=? ORDER BY id",
                (event_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM deliveries ORDER BY id DESC"
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def retry_delivery(delivery_id):
    conn = get_conn()
    try:
        delivery = conn.execute(
            "SELECT * FROM deliveries WHERE id=?",
            (delivery_id,),
        ).fetchone()

        if not delivery:
            raise DeliveryNotFound()

        if delivery["status"] != "failed":
            raise RetryNotAllowed()

        event = conn.execute(
            "SELECT payload FROM events WHERE event_id=?",
            (delivery["event_id"],),
        ).fetchone()
        payload = json.loads(event["payload"])
    finally:
        conn.close()

    _attempt_delivery(delivery_id, payload)

    conn = get_conn()
    try:
        return dict(conn.execute(
            "SELECT * FROM deliveries WHERE id=?",
            (delivery_id,),
        ).fetchone())
    finally:
        conn.close()
