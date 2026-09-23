"""SQLite storage layer. See 01-quota-service/app/db.py for the rationale."""
import os
import sqlite3
from contextlib import contextmanager

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id           TEXT    PRIMARY KEY,
    type         TEXT    NOT NULL,
    payload      TEXT    NOT NULL,
    status       TEXT    NOT NULL
                 CHECK (status IN ('queued', 'running', 'succeeded', 'dead')),
    attempts     INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL CHECK (max_attempts >= 1),
    next_run_at  INTEGER NOT NULL,
    locked_until INTEGER,
    lease_token  TEXT,
    last_error   TEXT,
    result       TEXT,
    created_at   INTEGER NOT NULL,
    updated_at   INTEGER NOT NULL
);
-- The worker's hot query is "queued tasks due now, oldest first".
CREATE INDEX IF NOT EXISTS idx_tasks_ready ON tasks (status, next_run_at);
"""


def db_path() -> str:
    return os.environ.get("DB_PATH", "tasks.db")


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
