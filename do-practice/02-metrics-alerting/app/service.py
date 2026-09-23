"""Metrics ingestion, time-bucketed queries, and threshold alerting.

Alerts are modelled as a state machine per rule: at most one firing alert
exists per rule at any time. A breach only creates an alert on the
not-firing -> firing transition, so a sustained breach does not produce a
new alert on every evaluation.
"""
import time

from .db import get_conn, transaction

# Reject points too far in the future; they usually mean a client clock bug,
# and they would sit in the window of every future evaluation.
MAX_FUTURE_SKEW_SECONDS = 300

AGGREGATIONS = {"avg": "AVG", "max": "MAX", "min": "MIN", "sum": "SUM", "count": "COUNT"}


class RuleNotFound(Exception):
    pass


def _now() -> int:
    return int(time.time())


def ingest(points: list[dict], now: int | None = None) -> dict:
    """Insert a batch of points. Valid points are stored even if others fail."""
    now = now if now is not None else _now()
    accepted, errors = [], []

    for i, p in enumerate(points):
        ts = p.get("ts") if p.get("ts") is not None else now
        if ts > now + MAX_FUTURE_SKEW_SECONDS:
            errors.append(f"point {i}: timestamp {ts} is too far in the future")
            continue
        accepted.append((p["resource_id"], p["name"], float(p["value"]), int(ts)))

    if accepted:
        with transaction() as conn:
            conn.executemany(
                "INSERT INTO metrics (resource_id, name, value, ts) VALUES (?, ?, ?, ?)",
                accepted,
            )

    return {"accepted": len(accepted), "rejected": len(errors), "errors": errors}


def query(resource_id: str, name: str, start: int, end: int,
          bucket_seconds: int, agg: str) -> list[dict]:
    """Aggregate points into fixed-width time buckets over [start, end)."""
    sql_agg = AGGREGATIONS[agg]  # caller validates agg, so no injection risk
    conn = get_conn()
    try:
        rows = conn.execute(
            f"""
            SELECT (ts / ?) * ? AS bucket_start,
                   {sql_agg}(value) AS value,
                   COUNT(*)        AS count
              FROM metrics
             WHERE resource_id = ? AND name = ? AND ts >= ? AND ts < ?
             GROUP BY bucket_start
             ORDER BY bucket_start
            """,
            (bucket_seconds, bucket_seconds, resource_id, name, start, end),
        ).fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]


def create_rule(rule: dict, now: int | None = None) -> dict:
    created_at = now if now is not None else _now()
    with transaction() as conn:
        cur = conn.execute(
            """
            INSERT INTO alert_rules
                (resource_id, metric_name, comparator, threshold, window_seconds, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (rule["resource_id"], rule["metric_name"], rule["comparator"],
             rule["threshold"], rule["window_seconds"], created_at),
        )
        rule_id = cur.lastrowid
    return {**rule, "id": rule_id, "created_at": created_at}


def list_rules() -> list[dict]:
    conn = get_conn()
    try:
        return [dict(r) for r in conn.execute("SELECT * FROM alert_rules ORDER BY id")]
    finally:
        conn.close()


def list_alerts(state: str | None = None) -> list[dict]:
    conn = get_conn()
    try:
        if state:
            rows = conn.execute(
                "SELECT * FROM alerts WHERE state = ? ORDER BY id", (state,)
            )
        else:
            rows = conn.execute("SELECT * FROM alerts ORDER BY id")
        return [dict(r) for r in rows]
    finally:
        conn.close()


def _breached(value: float, comparator: str, threshold: float) -> bool:
    return value > threshold if comparator == "gt" else value < threshold


def evaluate(now: int | None = None) -> dict:
    """Evaluate every rule once and apply state transitions.

    For each rule: take the average over the trailing window, compare with the
    threshold, then transition. With no data in the window we leave the state
    unchanged rather than resolving, because missing data is not the same as
    healthy data. A dead agent should not silently clear its own alert.
    """
    now = now if now is not None else _now()
    fired, resolved, no_data = [], [], []

    with transaction(immediate=True) as conn:
        rules = conn.execute("SELECT * FROM alert_rules").fetchall()
        for rule in rules:
            row = conn.execute(
                """
                SELECT AVG(value) AS avg_value, COUNT(*) AS n
                  FROM metrics
                 WHERE resource_id = ? AND name = ? AND ts > ? AND ts <= ?
                """,
                (rule["resource_id"], rule["metric_name"],
                 now - rule["window_seconds"], now),
            ).fetchone()

            if row["n"] == 0:
                no_data.append(rule["id"])
                continue

            value = row["avg_value"]
            firing = conn.execute(
                "SELECT id FROM alerts WHERE rule_id = ? AND state = 'firing'",
                (rule["id"],),
            ).fetchone()
            is_breach = _breached(value, rule["comparator"], rule["threshold"])

            if is_breach and firing is None:
                cur = conn.execute(
                    """
                    INSERT INTO alerts (rule_id, state, value, started_at)
                    VALUES (?, 'firing', ?, ?)
                    """,
                    (rule["id"], value, now),
                )
                fired.append(cur.lastrowid)
            elif not is_breach and firing is not None:
                conn.execute(
                    "UPDATE alerts SET state = 'resolved', resolved_at = ? WHERE id = ?",
                    (now, firing["id"]),
                )
                resolved.append(firing["id"])
            # breach + already firing, or healthy + not firing: no transition

    return {"evaluated": len(rules), "fired": fired, "resolved": resolved, "no_data": no_data}
