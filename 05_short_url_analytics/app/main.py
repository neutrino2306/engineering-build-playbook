from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from .database import init_db
from .schemas import LinkCreate, LinkResponse, LinkStats
from . import service

init_db()
app = FastAPI(title="Short URL Analytics Demo")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/links", response_model=LinkResponse, status_code=201)
def create_link(body: LinkCreate):
    return service.create_link(str(body.target_url))

@app.get("/links/{code}/stats", response_model=LinkStats)
def stats(code: str):
    try:
        return service.get_stats(code)
    except service.LinkNotFound:
        raise HTTPException(status_code=404, detail="link not found")

@app.get("/{code}")
def redirect(code: str, request: Request):
    try:
        target = service.resolve_and_record(
            code,
            request.headers.get("user-agent"),
            request.headers.get("referer"),
        )
        return RedirectResponse(url=target, status_code=307)
    except service.LinkNotFound:
        raise HTTPException(status_code=404, detail="link not found")
