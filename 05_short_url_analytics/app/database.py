import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "shortlinks.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS links (
                code TEXT PRIMARY KEY,
                target_url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                click_count INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                clicked_at TEXT NOT NULL,
                user_agent TEXT,
                referrer TEXT
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
