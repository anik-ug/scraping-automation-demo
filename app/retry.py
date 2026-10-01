import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def with_retry(
    operation: Callable[[], Awaitable[T]],
    max_retries: int,
    worker_id: int,
    task_id: int,
) -> T:
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[Worker-{worker_id}] Task-{task_id} attempt {attempt}/{max_retries}")
            return await operation()
        except Exception as exc:
            last_error = exc

            if attempt == max_retries:
                break

            delay = 2 ** (attempt - 1)
            print(
                f"[Worker-{worker_id}] Task-{task_id} failed: {exc}. "
                f"Retrying in {delay}s..."
            )
            await asyncio.sleep(delay)

    raise last_error
