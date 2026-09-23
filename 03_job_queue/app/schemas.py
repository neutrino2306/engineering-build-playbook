from typing import Any, Literal
from pydantic import BaseModel, Field

class JobCreate(BaseModel):
    task_type: Literal["echo", "sum", "fail"]
    payload: dict[str, Any] = {}
    max_attempts: int = Field(default=3, ge=1, le=10)

class JobResponse(BaseModel):
    id: str
    task_type: str
    payload: dict[str, Any]
    status: str
    attempts: int
    max_attempts: int
    result: Any | None
    last_error: str | None
    created_at: str
    updated_at: str
