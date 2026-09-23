# Metrics & Alerting Service

Ingests time-series metrics from cloud resources and fires threshold alerts.

## Features

- Batch metric ingestion with partial success
- Time-bucketed queries with avg / max / min / sum / count
- Threshold alert rules over a trailing window
- **Alert deduplication**: a sustained breach produces one alert, not one per evaluation
- Automatic resolution when the metric recovers
- **Missing data does not resolve a firing alert**

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest -v
```

## Example

```bash
# Create a rule: alert if avg CPU > 80 over 5 minutes
curl -X POST localhost:8000/alert-rules -H 'Content-Type: application/json' \
  -d '{"resource_id":"droplet-1","metric_name":"cpu","comparator":"gt","threshold":80,"window_seconds":300}'

# Ingest metrics
curl -X POST localhost:8000/metrics -H 'Content-Type: application/json' \
  -d '{"points":[{"resource_id":"droplet-1","name":"cpu","value":92}]}'

# Evaluate rules, then list firing alerts
curl -X POST localhost:8000/alerts/evaluate
curl 'localhost:8000/alerts?state=firing'
```

## Design Decisions

- **Alerts as a state machine.** At most one firing alert per rule; new alerts are created only on the not-firing to firing transition.
- **Missing data leaves state unchanged.** A resource that stops reporting should not silently clear its own alert.
- **Scheduled evaluation, not write-triggered.** Keeps ingestion fast and is the only way to detect missing data.
- **Composite index `(resource_id, name, ts)`**: equality columns first, range column last.
- **Custom validation error handler.** FastAPI's default handler echoes rejected input; a NaN in that echo cannot be serialized, turning a 422 into a 500.

## Known Limitations

- SQLite is ephemeral on App Platform and not suited to time-series write volume.
- Evaluation must be triggered externally; no built-in scheduler.
- No notification delivery.
- Raw points grow without bound; no retention or downsampling.
- Average-based rules only; no percentiles.
- No dedicated absence alert for silent resources.

## Production Improvements

- TimescaleDB or Prometheus for storage
- Retention policy with downsampling to hourly and daily rollups
- Scheduled evaluation sharded across workers
- Notification queue for firing and resolved alerts
- Time-of-day aware baselines instead of fixed thresholds
