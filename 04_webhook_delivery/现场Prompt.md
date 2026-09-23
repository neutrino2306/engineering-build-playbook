# 现场 Prompt

> 先不要写代码。请把这个 webhook delivery 题压成严格 3 小时 MVP。
>
> 我使用 Python + FastAPI + SQLite + pytest + httpx。
>
> 先设计：
> - Subscription / Event / Delivery
> - event idempotency
> - pending → delivered/failed
> - timeout
> - manual retry
> - external client boundary
>
> 自动 backoff、queue、DLQ、HMAC signing 留到 production discussion。
