import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "metrics.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL UNIQUE,
                source TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                ts TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS alert_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                operator TEXT NOT NULL,
                threshold REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id INTEGER NOT NULL,
                metric_id INTEGER NOT NULL,
                triggered_at TEXT NOT NULL,
                message TEXT NOT NULL
            );
            """
        )
        conn.commit()

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
