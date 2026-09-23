import os
from contextlib import asynccontextmanager
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse

from . import service
from .db import init_db
from .models import LinkIn, LinkOut, Stats


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="URL Shortener",
    description="Creates short links, redirects, and tracks click analytics.",
    lifespan=lifespan,
)


def base_url(request: Request) -> str:
    """Public base URL for building short links.

    Set BASE_URL in production (e.g. https://my-app.ondigitalocean.app).
    Behind App Platform's proxy, request.base_url may report http rather than
    https, so the env var is the reliable source.
    """
    return os.environ.get("BASE_URL", str(request.base_url)).rstrip("/")


def with_short_url(link: dict, request: Request) -> dict:
    return {**link, "short_url": f"{base_url(request)}/{link['code']}"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/links", response_model=LinkOut, status_code=201)
def create_link(body: LinkIn, request: Request):
    service_host = urlparse(base_url(request)).hostname
    try:
        link = service.create_link(
            str(body.url), service_host, body.custom_code, body.expires_in_seconds
        )
    except service.ReservedCode:
        raise HTTPException(422, detail=f"'{body.custom_code}' is reserved")
    except service.CodeTaken:
        raise HTTPException(409, detail=f"'{body.custom_code}' is already taken")
    except service.SelfRedirect:
        raise HTTPException(422, detail="Cannot shorten a link to this service")
    except service.CodeSpaceExhausted:
        raise HTTPException(503, detail="Could not allocate a code, try again")
    return with_short_url(link, request)


@app.get("/links/{code}", response_model=LinkOut)
def get_link(code: str, request: Request):
    try:
        return with_short_url(service.get_link(code), request)
    except service.LinkNotFound:
        raise HTTPException(404, detail="Link not found")


@app.get("/links/{code}/stats", response_model=Stats)
def link_stats(code: str, days: int = 30):
    try:
        return service.stats(code, days)
    except service.LinkNotFound:
        raise HTTPException(404, detail="Link not found")


@app.delete("/links/{code}", status_code=204)
def delete_link(code: str):
    try:
        service.delete_link(code)
    except service.LinkNotFound:
        raise HTTPException(404, detail="Link not found")
    return Response(status_code=204)


# This catch-all MUST be registered last. FastAPI matches routes in order,
# so if it came first, GET /health would be treated as a short code.
@app.get("/{code}")
def redirect(code: str, request: Request):
    try:
        target = service.resolve_and_record(
            code, request.headers.get("referer"), request.headers.get("user-agent")
        )
    except service.LinkNotFound:
        raise HTTPException(404, detail="Link not found")
    except service.LinkExpired:
        raise HTTPException(410, detail="Link has expired")
    # 307, not 301: browsers cache 301 permanently, so later clicks would skip
    # this server entirely. Analytics would stop, and the link could never be
    # changed or deleted for anyone who had already visited it.
    return RedirectResponse(target, status_code=307)
