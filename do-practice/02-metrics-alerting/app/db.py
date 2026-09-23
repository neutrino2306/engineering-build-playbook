"""SQLite storage layer. See 01-quota-service/app/db.py for the rationale."""
import os
import sqlite3
from contextlib import contextmanager

SCHEMA = """
CREATE TABLE IF NOT EXISTS metrics (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id TEXT    NOT NULL,
    name        TEXT    NOT NULL,
    value       REAL    NOT NULL,
    ts          INTEGER NOT NULL
);
-- Every query filters by (resource_id, name) and a time range, so this
-- composite index turns range scans into index seeks.
CREATE INDEX IF NOT EXISTS idx_metrics_lookup ON metrics (resource_id, name, ts);

CREATE TABLE IF NOT EXISTS alert_rules (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id    TEXT    NOT NULL,
    metric_name    TEXT    NOT NULL,
    comparator     TEXT    NOT NULL CHECK (comparator IN ('gt', 'lt')),
    threshold      REAL    NOT NULL,
    window_seconds INTEGER NOT NULL CHECK (window_seconds > 0),
    created_at     INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS alerts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id     INTEGER NOT NULL REFERENCES alert_rules (id),
    state       TEXT    NOT NULL CHECK (state IN ('firing', 'resolved')),
    value       REAL    NOT NULL,
    started_at  INTEGER NOT NULL,
    resolved_at INTEGER
);
CREATE INDEX IF NOT EXISTS idx_alerts_rule_state ON alerts (rule_id, state);
"""


def db_path() -> str:
    return os.environ.get("DB_PATH", "metrics.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path(), timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


@contextmanager
def transaction(immediate: bool = False):
    conn = get_conn()
    try:
        conn.execute("BEGIN IMMEDIATE" if immediate else "BEGIN")
        yield conn
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.close()


def init_db() -> None:
    conn = get_conn()
    try:
        conn.executescript(SCHEMA)
    finally:
        conn.close()
