from typing import Any
from pydantic import BaseModel

class SubscriptionIn(BaseModel):
    event_type: str
    target_url: str

class EventIn(BaseModel):
    event_id: str
    event_type: str
    payload: dict[str, Any]

class SubscriptionResponse(BaseModel):
    id: int
    event_type: str
    target_url: str

class DeliveryResponse(BaseModel):
    id: int
    event_id: str
    subscription_id: int
    target_url: str
    status: str
    attempts: int
    response_code: int | None
    last_error: str | None
