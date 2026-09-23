from fastapi import FastAPI, HTTPException
from .database import init_db
from .schemas import QuotaSet, UsageChange, QuotaResponse
from . import service

init_db()
app = FastAPI(title="Quota Service")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.put("/quotas/{subject_id}/{resource}", response_model=QuotaResponse)
def set_quota(subject_id: str, resource: str, body: QuotaSet):
    try:
        return service.set_quota(subject_id, resource, body.limit_amount)
    except service.InvalidQuotaChange as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@app.get("/quotas/{subject_id}/{resource}", response_model=QuotaResponse)
def get_quota(subject_id: str, resource: str):
    try:
        return service.get_quota(subject_id, resource)
    except service.QuotaNotFound:
        raise HTTPException(status_code=404, detail="quota not found")

@app.post("/quotas/{subject_id}/{resource}/consume", response_model=QuotaResponse)
def consume(subject_id: str, resource: str, body: UsageChange):
    try:
        return service.consume(subject_id, resource, body.amount)
    except service.QuotaNotFound:
        raise HTTPException(status_code=404, detail="quota not found")
    except service.QuotaExceeded:
        raise HTTPException(status_code=429, detail="quota exceeded")

@app.post("/quotas/{subject_id}/{resource}/release", response_model=QuotaResponse)
def release(subject_id: str, resource: str, body: UsageChange):
    try:
        return service.release(subject_id, resource, body.amount)
    except service.QuotaNotFound:
        raise HTTPException(status_code=404, detail="quota not found")
