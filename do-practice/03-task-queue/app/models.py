from typing import Any

from pydantic import BaseModel, Field


class TaskIn(BaseModel):
    type: str = Field(min_length=1, max_length=64)
    payload: dict[str, Any] = Field(default_factory=dict)
    max_attempts: int = Field(default=3, ge=1, le=20)


class TaskOut(BaseModel):
    id: str
    type: str
    payload: dict[str, Any]
    status: str
    attempts: int
    max_attempts: int
    next_run_at: int
    last_error: str | None
    result: Any | None
    created_at: int
    updated_at: int


class RunResult(BaseModel):
    reclaimed: int
    processed: int
    succeeded: list[str]
    retried: list[str]
    dead: list[str]
    lost_lease: list[str]
