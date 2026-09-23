from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Response

from . import service
from .db import init_db
from .models import QuotaIn, QuotaOut, ReservationIn, ReservationOut


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Quota Service",
    description="Enforces per-tenant resource quotas with atomic reservations.",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.put("/tenants/{tenant_id}/quotas/{resource}", response_model=QuotaOut)
def set_quota(tenant_id: str, resource: str, body: QuotaIn):
    return service.set_quota(tenant_id, resource, body.limit)


@app.get("/tenants/{tenant_id}/quotas", response_model=list[QuotaOut])
def list_quotas(tenant_id: str):
    return service.list_quotas(tenant_id)


@app.post(
    "/tenants/{tenant_id}/reservations",
    response_model=ReservationOut,
    status_code=201,
)
def reserve(
    tenant_id: str,
    body: ReservationIn,
    response: Response,
    idempotency_key: str | None = Header(default=None),
):
    try:
        reservation, replayed = service.reserve(
            tenant_id, body.resource, body.amount, idempotency_key
        )
    except service.QuotaNotFound:
        raise HTTPException(404, detail=f"No quota configured for {body.resource}")
    except service.QuotaExceeded as e:
        raise HTTPException(
            409,
            detail={
                "error": "quota_exceeded",
                "limit": e.limit,
                "used": e.used,
                "requested": e.requested,
            },
        )
    except service.IdempotencyConflict:
        raise HTTPException(
            422, detail="Idempotency-Key was already used with a different request"
        )

    if replayed:
        response.status_code = 200
    return reservation


@app.delete("/reservations/{reservation_id}", response_model=ReservationOut)
def release(reservation_id: str):
    try:
        return service.release(reservation_id)
    except service.ReservationNotFound:
        raise HTTPException(404, detail="Reservation not found")
