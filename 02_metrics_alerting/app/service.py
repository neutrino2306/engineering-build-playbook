import sqlite3
from datetime import datetime, timezone
from .database import get_conn

class DuplicateEvent(Exception):
    pass

OPS = {
    "gt": lambda value, threshold: value > threshold,
    "gte": lambda value, threshold: value >= threshold,
    "lt": lambda value, threshold: value < threshold,
    "lte": lambda value, threshold: value <= threshold,
}

def create_rule(metric_name, operator, threshold):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO alert_rules(metric_name, operator, threshold) VALUES (?, ?, ?)",
            (metric_name, operator, threshold),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM alert_rules WHERE id=?",
            (cur.lastrowid,),
        ).fetchone()
        return dict(row)

def ingest_metric(event_id, source, metric_name, value, timestamp):
    with get_conn() as conn:
        try:
            cur = conn.execute(
                """
                INSERT INTO metrics(event_id, source, metric_name, value, ts)
                VALUES (?, ?, ?, ?, ?)
                """,
                (event_id, source, metric_name, value, timestamp),
            )
        except sqlite3.IntegrityError as exc:
            raise DuplicateEvent() from exc

        metric_id = cur.lastrowid
        rules = conn.execute(
            "SELECT * FROM alert_rules WHERE metric_name=?",
            (metric_name,),
        ).fetchall()

        now = datetime.now(timezone.utc).isoformat()
        for rule in rules:
            if OPS[rule["operator"]](value, rule["threshold"]):
                msg = f"{metric_name}={value} triggered {rule['operator']} {rule['threshold']}"
                conn.execute(
                    """
                    INSERT INTO alerts(rule_id, metric_id, triggered_at, message)
                    VALUES (?, ?, ?, ?)
                    """,
                    (rule["id"], metric_id, now, msg),
                )

        conn.commit()
        row = conn.execute(
            "SELECT * FROM metrics WHERE id=?",
            (metric_id,),
        ).fetchone()
        return dict(row)

def list_metrics(metric_name=None, source=None, limit=20):
    query = "SELECT * FROM metrics WHERE 1=1"
    params = []

    if metric_name:
        query += " AND metric_name=?"
        params.append(metric_name)

    if source:
        query += " AND source=?"
        params.append(source)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    with get_conn() as conn:
        return [dict(r) for r in conn.execute(query, params).fetchall()]

def list_alerts(limit=20):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM alerts ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
