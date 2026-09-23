from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class EndpointIn(BaseModel):
    url: HttpUrl
    event_types: list[str] = Field(default=["*"], min_length=1)
    secret: str | None = Field(default=None, min_length=16,
                               description="Optional; generated if omitted")


class EndpointOut(BaseModel):
    id: str
    url: str
    event_types: list[str]
    active: bool
    created_at: int


class EndpointCreated(EndpointOut):
    secret: str  # returned once, at creation time only


class EventIn(BaseModel):
    type: str = Field(min_length=1, max_length=128)
    payload: dict[str, Any] = Field(default_factory=dict)


class EventOut(BaseModel):
    id: str
    type: str
    payload: dict[str, Any]
    created_at: int
    deliveries_created: int


class DeliveryOut(BaseModel):
    id: str
    event_id: str
    endpoint_id: str
    status: str
    attempts: int
    max_attempts: int
    next_attempt_at: int
    last_status_code: int | None
    last_error: str | None


class DispatchResult(BaseModel):
    attempted: int
    succeeded: list[str]
    retrying: list[str]
    dead: list[str]
