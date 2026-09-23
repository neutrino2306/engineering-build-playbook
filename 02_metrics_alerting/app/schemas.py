from datetime import datetime
from typing import Literal
from pydantic import BaseModel

class MetricIn(BaseModel):
    event_id: str
    source: str
    metric_name: str
    value: float
    timestamp: datetime

class RuleIn(BaseModel):
    metric_name: str
    operator: Literal["gt", "gte", "lt", "lte"]
    threshold: float

class MetricResponse(BaseModel):
    id: int
    event_id: str
    source: str
    metric_name: str
    value: float
    ts: str

class RuleResponse(BaseModel):
    id: int
    metric_name: str
    operator: str
    threshold: float

class AlertResponse(BaseModel):
    id: int
    rule_id: int
    metric_id: int
    triggered_at: str
    message: str
