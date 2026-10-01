from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    target_url: str = "http://127.0.0.1:8000/products"
    workers: int = 5
    max_retries: int = 3
    timeout_ms: int = 10_000
    rate_limit_seconds: float = 0.15


SETTINGS = Settings()
