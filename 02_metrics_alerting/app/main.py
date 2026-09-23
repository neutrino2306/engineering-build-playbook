from fastapi import FastAPI, HTTPException, Query
from .database import init_db
from .schemas import MetricIn, RuleIn, MetricResponse, RuleResponse, AlertResponse
from . import service

init_db()
app = FastAPI(title="Metrics and Alerting Demo")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/rules", response_model=RuleResponse, status_code=201)
def create_rule(body: RuleIn):
    return service.create_rule(body.metric_name, body.operator, body.threshold)

@app.post("/metrics", response_model=MetricResponse, status_code=201)
def ingest_metric(body: MetricIn):
    try:
        return service.ingest_metric(
            body.event_id,
            body.source,
            body.metric_name,
            body.value,
            body.timestamp.isoformat(),
        )
    except service.DuplicateEvent:
        raise HTTPException(status_code=409, detail="duplicate event_id")

@app.get("/metrics", response_model=list[MetricResponse])
def list_metrics(
    metric_name: str | None = None,
    source: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
):
    return service.list_metrics(metric_name, source, limit)

@app.get("/alerts", response_model=list[AlertResponse])
def list_alerts(limit: int = Query(default=20, ge=1, le=100)):
    return service.list_alerts(limit)
