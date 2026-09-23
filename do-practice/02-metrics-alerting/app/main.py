import time
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from . import service
from .db import init_db
from .models import (
    AlertOut, AlertRuleIn, AlertRuleOut, Bucket, EvaluationResult,
    IngestResult, MetricBatch,
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Metrics & Alerting Service",
    description="Ingests time-series metrics and fires threshold alerts.",
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_request: Request, exc: RequestValidationError):
    """Return 422 without echoing the rejected input.

    FastAPI's default handler includes the raw input in the error body. If that
    input is NaN or infinity it cannot be serialized to JSON, so a clean 422
    turns into a 500. Found by test_non_finite_value_rejected.
    """
    errors = [
        {"loc": list(e["loc"]), "msg": e["msg"], "type": e["type"]}
        for e in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"detail": errors})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/metrics", response_model=IngestResult, status_code=202)
def ingest(batch: MetricBatch):
    return service.ingest([p.model_dump() for p in batch.points])


@app.get("/metrics", response_model=list[Bucket])
def query(
    resource_id: str,
    name: str,
    start: int | None = None,
    end: int | None = None,
    bucket_seconds: int = Query(default=60, gt=0, le=86400),
    agg: Literal["avg", "max", "min", "sum", "count"] = "avg",
):
    end = end if end is not None else int(time.time()) + 1
    start = start if start is not None else end - 3600
    if start >= end:
        raise HTTPException(422, detail="start must be before end")
    if (end - start) / bucket_seconds > 10_000:
        raise HTTPException(422, detail="Too many buckets; widen bucket_seconds")
    return service.query(resource_id, name, start, end, bucket_seconds, agg)


@app.post("/alert-rules", response_model=AlertRuleOut, status_code=201)
def create_rule(rule: AlertRuleIn):
    return service.create_rule(rule.model_dump())


@app.get("/alert-rules", response_model=list[AlertRuleOut])
def list_rules():
    return service.list_rules()


@app.post("/alerts/evaluate", response_model=EvaluationResult)
def evaluate(now: int | None = None):
    """Evaluate all rules once.

    In production this runs on a schedule. Exposing it as an endpoint keeps
    the logic deterministic to test and easy to demo. `now` lets tests and
    demos evaluate at a fixed point in time.
    """
    return service.evaluate(now)


@app.get("/alerts", response_model=list[AlertOut])
def list_alerts(state: Literal["firing", "resolved"] | None = None):
    return service.list_alerts(state)
