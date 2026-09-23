"""SQLite storage layer.

Each call to get_conn() opens a fresh connection, so the module is safe to use
from multiple threads. Transactions are managed explicitly (isolation_level=None
puts sqlite3 in autocommit mode, and we issue BEGIN/COMMIT ourselves).
"""
import os
import sqlite3
from contextlib import contextmanager

SCHEMA = """
CREATE TABLE IF NOT EXISTS quotas (
    tenant_id   TEXT    NOT NULL,
    resource    TEXT    NOT NULL,
    limit_value INTEGER NOT NULL CHECK (limit_value >= 0),
    used        INTEGER NOT NULL DEFAULT 0 CHECK (used >= 0),
    updated_at  TEXT    NOT NULL,
    PRIMARY KEY (tenant_id, resource)
);

CREATE TABLE IF NOT EXISTS reservations (
    id          TEXT    PRIMARY KEY,
    tenant_id   TEXT    NOT NULL,
    resource    TEXT    NOT NULL,
    amount      INTEGER NOT NULL CHECK (amount > 0),
    status      TEXT    NOT NULL CHECK (status IN ('active', 'released')),
    created_at  TEXT    NOT NULL,
    released_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_reservations_tenant
    ON reservations (tenant_id, resource, status);
"""


def db_path() -> str:
    # Read at call time so tests can point each run at a temporary file.
    return os.environ.get("DB_PATH", "quota.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path(), timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


@contextmanager
def transaction(immediate: bool = False):
    """Run a block inside a transaction.

    immediate=True takes the write lock at BEGIN, which serializes writers and
    prevents another transaction from slipping in between a read and a write.
    """
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
