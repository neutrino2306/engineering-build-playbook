from pydantic import BaseModel, Field


class QuotaIn(BaseModel):
    limit: int = Field(ge=0, description="Maximum units of this resource the tenant may hold")


class QuotaOut(BaseModel):
    tenant_id: str
    resource: str
    limit: int
    used: int
    available: int


class ReservationIn(BaseModel):
    resource: str = Field(min_length=1, max_length=64)
    amount: int = Field(gt=0, le=1_000_000)


class ReservationOut(BaseModel):
    id: str
    tenant_id: str
    resource: str
    amount: int
    status: str
    created_at: str
    released_at: str | None = None
