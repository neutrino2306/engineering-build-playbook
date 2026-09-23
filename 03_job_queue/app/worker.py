from . import service

def execute_job(job_id: str):
    job = service.get_job(job_id)
    service.mark_running(job_id)

    try:
        if job["task_type"] == "echo":
            result = {"message": job["payload"].get("message")}
        elif job["task_type"] == "sum":
            result = {"sum": sum(job["payload"].get("numbers", []))}
        elif job["task_type"] == "fail":
            raise RuntimeError("simulated task failure")
        else:
            raise RuntimeError("unsupported task type")

        service.mark_succeeded(job_id, result)
    except Exception as exc:
        service.mark_failed(job_id, str(exc))
