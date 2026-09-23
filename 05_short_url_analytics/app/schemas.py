from pydantic import BaseModel, HttpUrl

class LinkCreate(BaseModel):
    target_url: HttpUrl

class LinkResponse(BaseModel):
    code: str
    target_url: str
    short_path: str

class ClickResponse(BaseModel):
    clicked_at: str
    user_agent: str | None
    referrer: str | None

class LinkStats(BaseModel):
    code: str
    target_url: str
    click_count: int
    recent_clicks: list[ClickResponse]
