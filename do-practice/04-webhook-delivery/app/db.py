"""SQLite storage layer. See 01-quota-service/app/db.py for the rationale."""
import os
import sqlite3
from contextlib import contextmanager

SCHEMA = """
CREATE TABLE IF NOT EXISTS endpoints (
    id          TEXT    PRIMARY KEY,
    url         TEXT    NOT NULL,
    secret      TEXT    NOT NULL,
    event_types TEXT    NOT NULL,          -- JSON list; ["*"] matches everything
    active      INTEGER NOT NULL DEFAULT 1,
    created_at  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id         TEXT    PRIMARY KEY,
    type       TEXT    NOT NULL,
    payload    TEXT    NOT NULL,
    created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS deliveries (
    id               TEXT    PRIMARY KEY,
    event_id         TEXT    NOT NULL REFERENCES events (id),
    endpoint_id      TEXT    NOT NULL REFERENCES endpoints (id),
    status           TEXT    NOT NULL
                     CHECK (status IN ('pending', 'succeeded', 'dead')),
    attempts         INTEGER NOT NULL DEFAULT 0,
    max_attempts     INTEGER NOT NULL,
    next_attempt_at  INTEGER NOT NULL,
    last_status_code INTEGER,
    last_error       TEXT,
    created_at       INTEGER NOT NULL,
    updated_at       INTEGER NOT NULL,
    -- One delivery per (event, endpoint): fan-out can be safely re-run.
    UNIQUE (event_id, endpoint_id)
);
CREATE INDEX IF NOT EXISTS idx_deliveries_due ON deliveries (status, next_attempt_at);
"""


def db_path() -> str:
    return os.environ.get("DB_PATH", "webhooks.db")


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
