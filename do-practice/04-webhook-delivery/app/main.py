import json
from collections import deque
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Request

from . import service, signing
from .db import init_db
from .models import (
    DeliveryOut, DispatchResult, EndpointCreated, EndpointIn, EndpointOut,
    EventIn, EventOut,
)

# Demo-only: the last requests accepted by the built-in receiver.
RECEIVED = deque(maxlen=50)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Webhook Delivery Service",
    description="Registers endpoints, fans out events, and delivers them with signed, retried requests.",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/endpoints", response_model=EndpointCreated, status_code=201)
def create_endpoint(body: EndpointIn):
    return service.create_endpoint(str(body.url), body.event_types, body.secret)


@app.get("/endpoints", response_model=list[EndpointOut])
def list_endpoints():
    return service.list_endpoints()


@app.delete("/endpoints/{endpoint_id}", response_model=EndpointOut)
def deactivate_endpoint(endpoint_id: str):
    try:
        return service.deactivate_endpoint(endpoint_id)
    except service.EndpointNotFound:
        raise HTTPException(404, detail="Endpoint not found")


@app.post("/events", response_model=EventOut, status_code=201)
def publish_event(body: EventIn):
    return service.publish_event(body.type, body.payload)


@app.get("/events/{event_id}/deliveries", response_model=list[DeliveryOut])
def list_deliveries(event_id: str):
    return service.list_deliveries(event_id)


@app.post("/deliveries/{delivery_id}/retry", response_model=DeliveryOut)
def retry_delivery(delivery_id: str):
    try:
        return service.retry_delivery(delivery_id)
    except service.DeliveryNotFound:
        raise HTTPException(404, detail="Delivery not found")
    except service.InvalidTransition as e:
        raise HTTPException(409, detail=str(e))


@app.post("/dispatcher/run-once", response_model=DispatchResult)
def dispatch_once(now: int | None = None, batch_size: int = Query(default=20, ge=1, le=200)):
    return service.dispatch_once(now, batch_size)


@app.post("/receiver")
async def receiver(request: Request):
    """A demo receiver that verifies signatures.

    Register this app's own /receiver URL as an endpoint to demo the full
    sign, deliver, verify loop on a single deployment.
    """
    body = await request.body()
    endpoint_id = request.headers.get("x-webhook-endpoint-id", "")
    signature = request.headers.get("x-webhook-signature", "")
    try:
        timestamp = int(request.headers.get("x-webhook-timestamp", ""))
    except ValueError:
        raise HTTPException(400, detail="Missing or invalid timestamp")

    secret = service.get_secret(endpoint_id)
    if secret is None or not signing.verify(secret, timestamp, body, signature):
        raise HTTPException(401, detail="Invalid signature")

    RECEIVED.appendleft({"webhook_id": request.headers.get("x-webhook-id"),
                         "event": json.loads(body)})
    return {"received": True}


@app.get("/receiver/log")
def receiver_log():
    return list(RECEIVED)
