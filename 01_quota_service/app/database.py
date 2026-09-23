import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "quota.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS quotas (
                subject_id TEXT NOT NULL,
                resource TEXT NOT NULL,
                limit_amount INTEGER NOT NULL,
                used INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (subject_id, resource)
            )
            """
        )
        conn.commit()

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
