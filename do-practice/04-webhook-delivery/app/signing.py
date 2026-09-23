"""HMAC request signing, in the style used by Stripe and GitHub webhooks.

The signature covers the timestamp as well as the body. Without the
timestamp, an attacker who captured one valid request could replay it
forever; with it, the receiver rejects anything outside a short window.
"""
import hashlib
import hmac
import secrets
import time

SIGNATURE_VERSION = "v1"
DEFAULT_TOLERANCE_SECONDS = 300


def generate_secret() -> str:
    return "whsec_" + secrets.token_urlsafe(32)


def sign(secret: str, timestamp: int, body: bytes) -> str:
    signed = f"{timestamp}.".encode() + body
    digest = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    return f"{SIGNATURE_VERSION}={digest}"


def verify(secret: str, timestamp: int, body: bytes, signature: str,
           now: int | None = None, tolerance: int = DEFAULT_TOLERANCE_SECONDS) -> bool:
    now = now if now is not None else int(time.time())
    if abs(now - timestamp) > tolerance:
        return False
    expected = sign(secret, timestamp, body)
    # compare_digest runs in constant time, so response timing does not leak
    # how many leading characters of a forged signature were correct.
    return hmac.compare_digest(expected, signature)
