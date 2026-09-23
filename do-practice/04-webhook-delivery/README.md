# Webhook Delivery Service

Registers customer endpoints, fans out events to subscribers, and delivers them with signed, retried HTTP requests.

## Features

- Register endpoints with event-type filters (`["*"]` matches all)
- Fan-out: one event, one independent delivery per matching endpoint
- **HMAC-SHA256 signatures** with timestamps for **replay protection**
- **Retries with exponential backoff**; non-retryable 4xx fail fast
- Idempotent fan-out via `UNIQUE(event_id, endpoint_id)`
- **Built-in verifying receiver** for demoing the full loop on one deployment

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest -v
```

## Demo the Full Loop

```bash
# 1. Register this app's own receiver as an endpoint
curl -X POST localhost:8000/endpoints -H 'Content-Type: application/json' \
  -d '{"url":"http://localhost:8000/receiver","event_types":["droplet.created"]}'

# 2. Publish an event
curl -X POST localhost:8000/events -H 'Content-Type: application/json' \
  -d '{"type":"droplet.created","payload":{"droplet_id":123}}'

# 3. Deliver, then check what the receiver verified
curl -X POST localhost:8000/dispatcher/run-once
curl localhost:8000/receiver/log
```

## Signature Scheme

```
X-Webhook-Timestamp: 1700000000
X-Webhook-Signature: v1=<hex HMAC-SHA256(secret, "<timestamp>.<body>")>
X-Webhook-Id:        evt_...   (dedupe key for receivers)
```

Receivers reject timestamps older than 5 minutes and compare with `hmac.compare_digest`.

## Retry Policy

| Response | Action |
|---|---|
| 2xx | Succeeded |
| 408, 429, 5xx, network error | Retry with backoff |
| Other 4xx | Dead immediately |

## Design Decisions

- **Asynchronous delivery.** A slow or failing endpoint never blocks event publishing or other customers.
- **Timestamp inside the signature**, so it cannot be altered on a captured request.
- **Constant-time comparison** to prevent timing attacks.
- **At-least-once delivery.** Receivers dedupe on `X-Webhook-Id`.
- **Event and deliveries written in one transaction**; HTTP calls happen outside transactions.

## Known Limitations

- SQLite is ephemeral on App Platform.
- Dispatch is triggered externally; no background loop.
- Secrets stored in plaintext; no rotation support.
- No ordering guarantee; no per-endpoint circuit breaker.

## Production Improvements

- Background dispatcher as a separate worker component
- Secrets encrypted with a KMS; dual-secret rotation window
- Auto-disable endpoints with sustained failure rates
- Per-endpoint concurrency limits
