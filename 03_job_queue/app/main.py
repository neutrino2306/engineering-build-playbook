from fastapi import FastAPI, HTTPException, BackgroundTasks
from .database import init_db
from .schemas import JobCreate, JobResponse
from . import service, worker

init_db()
app = FastAPI(title="Job Queue Demo")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/jobs", response_model=JobResponse, status_code=202)
def create_job(body: JobCreate, background_tasks: BackgroundTasks):
    job = service.create_job(body.task_type, body.payload, body.max_attempts)
    background_tasks.add_task(worker.execute_job, job["id"])
    return job

@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: str):
    try:
        return service.get_job(job_id)
    except service.JobNotFound:
        raise HTTPException(status_code=404, detail="job not found")

@app.post("/jobs/{job_id}/retry", response_model=JobResponse, status_code=202)
def retry_job(job_id: str, background_tasks: BackgroundTasks):
    try:
        job = service.retry_job(job_id)
    except service.JobNotFound:
        raise HTTPException(status_code=404, detail="job not found")
    except service.RetryNotAllowed:
        raise HTTPException(status_code=409, detail="retry not allowed")

    background_tasks.add_task(worker.execute_job, job_id)
    return job
