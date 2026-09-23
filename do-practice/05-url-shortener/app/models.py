from pydantic import BaseModel, Field, HttpUrl


class LinkIn(BaseModel):
    url: HttpUrl  # only http and https schemes are accepted
    custom_code: str | None = Field(default=None, pattern=r"^[A-Za-z0-9_-]{3,32}$")
    expires_in_seconds: int | None = Field(default=None, gt=0, le=365 * 86400)


class LinkOut(BaseModel):
    code: str
    short_url: str
    target_url: str
    is_custom: bool
    created_at: int
    expires_at: int | None
    click_count: int


class DayCount(BaseModel):
    day_start: int
    clicks: int


class ReferrerCount(BaseModel):
    referrer: str
    clicks: int


class Stats(BaseModel):
    code: str
    total_clicks: int
    clicks_by_day: list[DayCount]
    top_referrers: list[ReferrerCount]
