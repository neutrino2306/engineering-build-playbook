import logging
import os
import threading
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Query

from . import service
from .db import init_db
from .models import RunResult, TaskIn, TaskOut

log = logging.getLogger("task-queue")
POLL_INTERVAL_SECONDS = float(os.environ.get("POLL_INTERVAL_SECONDS", "1"))


def _worker_loop(stop: threading.Event) -> None:
    while not stop.is_set():
        try:
            service.run_once()
        except Exception:
            # Never let one bad iteration kill the worker thread.
            log.exception("worker iteration failed")
        stop.wait(POLL_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    stop = threading.Event()
    worker = None
    # In-process worker for the prototype. Tests disable it and drive the
    # queue through /worker/run-once so behaviour is deterministic.
    if os.environ.get("ENABLE_WORKER", "true").lower() == "true":
        worker = threading.Thread(target=_worker_loop, args=(stop,), daemon=True)
        worker.start()
    yield
    stop.set()
    if worker:
        worker.join(timeout=5)


app = FastAPI(
    title="Task Queue",
    description="Durable task queue with leases, retries, backoff, and dead-lettering.",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskOut, status_code=201)
def enqueue(body: TaskIn):
    try:
        return service.enqueue(body.type, body.payload, body.max_attempts)
    except service.UnknownTaskType:
        raise HTTPException(422, detail=f"Unknown task type: {body.type}")


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: str):
    try:
        return service.get_task(task_id)
    except service.TaskNotFound:
        raise HTTPException(404, detail="Task not found")


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(
    status: Literal["queued", "running", "succeeded", "dead"] | None = None,
    limit: int = Query(default=100, ge=1, le=1000),
):
    return service.list_tasks(status, limit)


@app.post("/tasks/{task_id}/retry", response_model=TaskOut)
def retry(task_id: str):
    try:
        return service.retry_dead(task_id)
    except service.TaskNotFound:
        raise HTTPException(404, detail="Task not found")
    except service.InvalidTransition as e:
        raise HTTPException(409, detail=str(e))


@app.post("/worker/run-once", response_model=RunResult)
def run_once(now: int | None = None, batch_size: int = Query(default=10, ge=1, le=100)):
    """Process due tasks once. Used for tests and demos; production uses the loop."""
    return service.run_once(now, batch_size)
