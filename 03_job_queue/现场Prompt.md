# 现场 Prompt

> 先不要写代码。请把这个 job queue / async task 题压成 3 小时 MVP。
>
> 我使用 Python + FastAPI + SQLite + pytest。
>
> 优先设计：
> - Job 状态机
> - attempts / max attempts
> - submit / get status / retry
> - worker 与 API 的最小边界
>
> 不要一开始引入 Redis/Celery/Kafka。
> Production queue、visibility timeout、DLQ、idempotency 留到 code review。
