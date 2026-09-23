import math
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class MetricPoint(BaseModel):
    resource_id: str = Field(min_length=1, max_length=128)
    name: str = Field(min_length=1, max_length=64)
    value: float
    ts: int | None = Field(default=None, description="Unix seconds; defaults to server time")

    @field_validator("value")
    @classmethod
    def value_must_be_finite(cls, v: float) -> float:
        # NaN and infinity would silently poison every average they touch.
        if not math.isfinite(v):
            raise ValueError("value must be a finite number")
        return v


class MetricBatch(BaseModel):
    points: list[MetricPoint] = Field(min_length=1, max_length=1000)


class IngestResult(BaseModel):
    accepted: int
    rejected: int
    errors: list[str]


class Bucket(BaseModel):
    bucket_start: int
    value: float
    count: int


class AlertRuleIn(BaseModel):
    resource_id: str = Field(min_length=1, max_length=128)
    metric_name: str = Field(min_length=1, max_length=64)
    comparator: Literal["gt", "lt"]
    threshold: float
    window_seconds: int = Field(gt=0, le=86400)


class AlertRuleOut(AlertRuleIn):
    id: int
    created_at: int


class AlertOut(BaseModel):
    id: int
    rule_id: int
    state: str
    value: float
    started_at: int
    resolved_at: int | None


class EvaluationResult(BaseModel):
    evaluated: int
    fired: list[int]
    resolved: list[int]
    no_data: list[int]
