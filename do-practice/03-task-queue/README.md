# Task Queue

A durable background task queue with leases, retries, exponential backoff, and dead-lettering.

## Features

- Submit tasks and poll their status
- Asynchronous processing by a background worker
- **Retries with exponential backoff and jitter**
- **Dead-letter state** after `max_attempts`, with manual retry
- **Leases**: tasks held by a crashed worker are reclaimed
- **Fencing tokens**: a worker that lost its lease cannot overwrite the new owner's result

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload     # background worker runs automatically
pytest -v                         # tests disable the worker for determinism
```

## Example

```bash
# Submit a task that fails once, then succeeds
curl -X POST localhost:8000/tasks -H 'Content-Type: application/json' \
  -d '{"type":"flaky","payload":{"succeed_on_attempt":2},"max_attempts":3}'

# Check status
curl localhost:8000/tasks/<id>

# List dead tasks
curl 'localhost:8000/tasks?status=dead'
```

Built-in task types: `echo`, `add`, `flaky`, `fail`.

## State Machine

```
queued -> running -> succeeded
             |-> queued (retry after backoff, attempts left)
             |-> dead   (no attempts left)
running -> queued       (lease expired: worker crashed)
dead -> queued          (manual retry)
```

## Design Decisions

- **At-least-once delivery.** A worker can finish work and crash before recording it, so handlers must be idempotent. Exactly-once is not achievable across two separate steps.
- **Attempts counted at claim time**, not failure time, so a task that crashes its worker still reaches the dead state.
- **Handlers run outside transactions.** Holding SQLite's write lock during a long task would block every other writer.
- **Fencing tokens** on completion, so a stalled worker whose lease expired cannot overwrite a newer result.
- **Database as queue** to avoid an extra component, with the option of transactional outbox semantics.

## Known Limitations

- SQLite is ephemeral on App Platform; tasks are lost on redeploy.
- Worker runs in the API process and cannot scale independently.
- Polling adds up to one interval of latency.
- No priorities; no retention for completed tasks.

## Production Improvements

- Separate worker component on App Platform
- PostgreSQL with `SELECT ... FOR UPDATE SKIP LOCKED` for parallel claims
- `LISTEN/NOTIFY` instead of polling
- Priority column and retention policy
