from pydantic import BaseModel, Field

class QuotaSet(BaseModel):
    limit_amount: int = Field(gt=0)

class UsageChange(BaseModel):
    amount: int = Field(gt=0)

class QuotaResponse(BaseModel):
    subject_id: str
    resource: str
    limit_amount: int
    used: int
    remaining: int
