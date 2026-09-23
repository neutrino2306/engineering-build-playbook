from fastapi import FastAPI, HTTPException
from .database import init_db
from .schemas import (
    SubscriptionIn,
    EventIn,
    SubscriptionResponse,
    DeliveryResponse,
)
from . import service

init_db()
app = FastAPI(title="Webhook Delivery Demo")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/subscriptions", response_model=SubscriptionResponse, status_code=201)
def create_subscription(body: SubscriptionIn):
    return service.create_subscription(body.event_type, body.target_url)

@app.post("/events", response_model=list[DeliveryResponse], status_code=201)
def dispatch_event(body: EventIn):
    try:
        return service.dispatch_event(
            body.event_id,
            body.event_type,
            body.payload,
        )
    except service.DuplicateEvent:
        raise HTTPException(status_code=409, detail="duplicate event_id")

@app.get("/deliveries", response_model=list[DeliveryResponse])
def list_deliveries(event_id: str | None = None):
    return service.list_deliveries(event_id)

@app.post("/deliveries/{delivery_id}/retry", response_model=DeliveryResponse)
def retry_delivery(delivery_id: int):
    try:
        return service.retry_delivery(delivery_id)
    except service.DeliveryNotFound:
        raise HTTPException(status_code=404, detail="delivery not found")
    except service.RetryNotAllowed:
        raise HTTPException(status_code=409, detail="retry not allowed")
