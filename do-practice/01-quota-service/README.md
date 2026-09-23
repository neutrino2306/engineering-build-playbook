# Quota Service

Enforces per-tenant resource quotas with atomic reservations.

## Features

- Set and update quota limits per tenant and resource type
- Reserve and release resource units
- **Concurrency-safe**: limits cannot be exceeded under concurrent requests
- **Idempotent reservations** via the `Idempotency-Key` header
- Idempotent release (releasing twice does not refund twice)

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# Interactive docs: http://127.0.0.1:8000/docs
```

## Tests

```bash
pytest -v
```

Includes a concurrency test: 50 concurrent reservations against a limit of 10, asserting exactly 10 succeed.

## API

```bash
# Set a limit
curl -X PUT localhost:8000/tenants/acme/quotas/droplets \
  -H 'Content-Type: application/json' -d '{"limit": 5}'

# Reserve (with idempotency)
curl -X POST localhost:8000/tenants/acme/reservations \
  -H 'Content-Type: application/json' -H 'Idempotency-Key: req-123' \
  -d '{"resource": "droplets", "amount": 2}'

# Release
curl -X DELETE localhost:8000/reservations/req-123
```

| Status | Meaning |
|---|---|
| 201 | Reservation created |
| 200 | Idempotent replay of an existing reservation |
| 404 | No quota configured for this resource |
| 409 | Quota would be exceeded |
| 422 | Idempotency key reused with a different body |

## Design Decisions

- **Conditional UPDATE for atomicity.** The limit check lives inside the UPDATE statement, so the database enforces it atomically. This holds across multiple app instances once storage is shared, unlike an in-process lock.
- **`used` stored as a counter** so each reservation touches one row. Trade-off: it can drift from the reservations table, which a reconciliation job would catch.
- **Lowering a limit below usage** blocks new reservations but does not revoke existing ones. Revocation is a product decision.

## Known Limitations

- SQLite on App Platform is ephemeral; data is lost on redeploy. Production would use Managed PostgreSQL.
- Single instance only; state is not shared across instances.
- No authentication or tenant isolation.
- Reservations never expire, so a crashed client leaks quota.
- No audit log of limit changes.

## Production Improvements

- Managed PostgreSQL with connection pooling
- Reservation TTL with a background sweeper, or a two-phase reserve/confirm flow
- Authentication, with tenant_id derived from the caller's identity
- Periodic reconciliation between `used` and active reservations
- Metrics on rejection rate per tenant and resource
