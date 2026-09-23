import uuid
from datetime import datetime, timezone
from .database import get_conn

class LinkNotFound(Exception):
    pass

def _now():
    return datetime.now(timezone.utc).isoformat()

def _generate_code():
    return uuid.uuid4().hex[:7]

def create_link(target_url):
    with get_conn() as conn:
        for _ in range(5):
            code = _generate_code()
            exists = conn.execute(
                "SELECT 1 FROM links WHERE code=?",
                (code,),
            ).fetchone()

            if not exists:
                conn.execute(
                    """
                    INSERT INTO links(code, target_url, created_at)
                    VALUES (?, ?, ?)
                    """,
                    (code, target_url, _now()),
                )
                conn.commit()
                return {
                    "code": code,
                    "target_url": target_url,
                    "short_path": f"/{code}",
                }

    raise RuntimeError("could not generate unique code")

def resolve_and_record(code, user_agent, referrer):
    with get_conn() as conn:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute(
            "SELECT * FROM links WHERE code=?",
            (code,),
        ).fetchone()

        if not row:
            conn.rollback()
            raise LinkNotFound()

        conn.execute(
            "UPDATE links SET click_count=click_count+1 WHERE code=?",
            (code,),
        )
        conn.execute(
            """
            INSERT INTO clicks(code, clicked_at, user_agent, referrer)
            VALUES (?, ?, ?, ?)
            """,
            (code, _now(), user_agent, referrer),
        )
        conn.commit()
        return row["target_url"]

def get_stats(code):
    with get_conn() as conn:
        link = conn.execute(
            "SELECT * FROM links WHERE code=?",
            (code,),
        ).fetchone()

        if not link:
            raise LinkNotFound()

        clicks = conn.execute(
            """
            SELECT clicked_at, user_agent, referrer
            FROM clicks
            WHERE code=?
            ORDER BY id DESC
            LIMIT 20
            """,
            (code,),
        ).fetchall()

        return {
            "code": link["code"],
            "target_url": link["target_url"],
            "click_count": link["click_count"],
            "recent_clicks": [dict(c) for c in clicks],
        }
