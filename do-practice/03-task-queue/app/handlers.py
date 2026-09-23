"""Task handlers, keyed by task type.

Handlers must be idempotent: the queue gives at-least-once delivery, so a task
can run more than once if a worker crashes after doing the work but before
recording the result.
"""


class TaskError(Exception):
    """Raised by a handler to signal a retryable failure."""


def echo(payload: dict, attempt: int) -> dict:
    return {"echo": payload}


def add(payload: dict, attempt: int) -> dict:
    numbers = payload.get("numbers")
    if not isinstance(numbers, list) or not all(isinstance(n, (int, float)) for n in numbers):
        raise TaskError("payload.numbers must be a list of numbers")
    return {"sum": sum(numbers)}


def flaky(payload: dict, attempt: int) -> dict:
    """Fails until the given attempt number. Useful for demoing retries."""
    succeed_on = int(payload.get("succeed_on_attempt", 2))
    if attempt < succeed_on:
        raise TaskError(f"simulated failure on attempt {attempt}")
    return {"succeeded_on_attempt": attempt}


def fail(payload: dict, attempt: int) -> dict:
    """Always fails. Useful for demoing the dead-letter path."""
    raise TaskError("this task always fails")


HANDLERS = {"echo": echo, "add": add, "flaky": flaky, "fail": fail}
