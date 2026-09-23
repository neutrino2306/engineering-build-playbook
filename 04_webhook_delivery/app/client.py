import httpx

def deliver(target_url: str, payload: dict) -> tuple[int, str | None]:
    if target_url == "mock://success":
        return 200, None

    if target_url == "mock://fail":
        return 500, "simulated receiver failure"

    try:
        response = httpx.post(target_url, json=payload, timeout=3.0)
        if 200 <= response.status_code < 300:
            return response.status_code, None
        return response.status_code, f"receiver returned {response.status_code}"
    except Exception as exc:
        return 0, str(exc)
