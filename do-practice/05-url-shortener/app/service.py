"""Short link creation, resolution, and click analytics."""
import secrets
import sqlite3
import string
import time
from urllib.parse import urlparse

from .db import get_conn, transaction

ALPHABET = string.ascii_letters + string.digits  # base62
CODE_LENGTH = 7  # 62**7 is about 3.5 trillion codes
MAX_GENERATION_ATTEMPTS = 5

# Paths the app itself serves. A custom code equal to one of these would be
# shadowed by the real route (or shadow it), so they are not allowed.
RESERVED_CODES = {"health", "links", "docs", "redoc", "openapi.json", "static", "api"}


class LinkNotFound(Exception):
    pass


class LinkExpired(Exception):
    pass


class CodeTaken(Exception):
    pass


class ReservedCode(Exception):
    pass


class SelfRedirect(Exception):
    pass


class CodeSpaceExhausted(Exception):
    pass


def _now() -> int:
    return int(time.time())


def generate_code() -> str:
    # secrets rather than random: codes should not be predictable, otherwise
    # someone can enumerate other users' links.
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


def _row_to_dict(row) -> dict:
    d = dict(row)
    d["is_custom"] = bool(d["is_custom"])
    return d


def create_link(target_url: str, service_host: str, custom_code: str | None = None,
                expires_in_seconds: int | None = None, now: int | None = None) -> dict:
    now = now if now is not None else _now()

    # A link pointing back at this service could create a redirect loop.
    if urlparse(target_url).hostname == service_host:
        raise SelfRedirect(target_url)

    expires_at = now + expires_in_seconds if expires_in_seconds else None

    if custom_code is not None:
        if custom_code.lower() in RESERVED_CODES:
            raise ReservedCode(custom_code)
        try:
            _insert(custom_code, target_url, True, now, expires_at)
        except sqlite3.IntegrityError:
            raise CodeTaken(custom_code)
        return get_link(custom_code)

    # Random codes: retry on the (rare) collision instead of checking first.
    # Check-then-insert would race; letting the PRIMARY KEY reject duplicates
    # is both simpler and correct under concurrency.
    for _ in range(MAX_GENERATION_ATTEMPTS):
        code = generate_code()
        try:
            _insert(code, target_url, False, now, expires_at)
            return get_link(code)
        except sqlite3.IntegrityError:
            continue
    raise CodeSpaceExhausted()


def _insert(code: str, target_url: str, is_custom: bool, now: int, expires_at: int | None):
    with transaction() as conn:
        conn.execute(
            "INSERT INTO links (code, target_url, is_custom, created_at, expires_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (code, target_url, int(is_custom), now, expires_at),
        )


def get_link(code: str) -> dict:
    conn = get_conn()
    try:
        row = conn.execute("SELECT * FROM links WHERE code = ?", (code,)).fetchone()
    finally:
        conn.close()
    if row is None:
        raise LinkNotFound(code)
    return _row_to_dict(row)


def resolve_and_record(code: str, referrer: str | None, user_agent: str | None,
                       now: int | None = None) -> str:
    """Return the target URL and record the click in one transaction.

    Recording synchronously adds a write to every redirect. That's fine for a
    prototype; at scale the click would go onto a queue so the redirect path
    stays read-only and fast.
    """
    now = now if now is not None else _now()
    with transaction(immediate=True) as conn:
        row = conn.execute(
            "SELECT target_url, expires_at FROM links WHERE code = ?", (code,)
        ).fetchone()
        if row is None:
            raise LinkNotFound(code)
        if row["expires_at"] is not None and now >= row["expires_at"]:
            raise LinkExpired(code)
        conn.execute("UPDATE links SET click_count = click_count + 1 WHERE code = ?", (code,))
        conn.execute(
            "INSERT INTO clicks (code, ts, referrer, user_agent) VALUES (?, ?, ?, ?)",
            (code, now, (referrer or None) and referrer[:512], (user_agent or None) and user_agent[:512]),
        )
    return row["target_url"]


def delete_link(code: str) -> None:
    with transaction(immediate=True) as conn:
        cur = conn.execute("DELETE FROM links WHERE code = ?", (code,))
        if cur.rowcount == 0:
            raise LinkNotFound(code)


def stats(code: str, days: int = 30, now: int | None = None) -> dict:
    now = now if now is not None else _now()
    link = get_link(code)  # raises LinkNotFound
    since = now - days * 86400
    conn = get_conn()
    try:
        by_day = conn.execute(
            """
            SELECT (ts / 86400) * 86400 AS day_start, COUNT(*) AS clicks
              FROM clicks WHERE code = ? AND ts >= ?
             GROUP BY day_start ORDER BY day_start
            """,
            (code, since),
        ).fetchall()
        referrers = conn.execute(
            """
            SELECT COALESCE(referrer, '(direct)') AS referrer, COUNT(*) AS clicks
              FROM clicks WHERE code = ? AND ts >= ?
             GROUP BY referrer ORDER BY clicks DESC, referrer LIMIT 5
            """,
            (code, since),
        ).fetchall()
    finally:
        conn.close()
    return {
        "code": code,
        "total_clicks": link["click_count"],
        "clicks_by_day": [dict(r) for r in by_day],
        "top_referrers": [dict(r) for r in referrers],
    }
