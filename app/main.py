"""FastAPI entry point. Phase 0 only exposes a health check."""
import psycopg
import redis
from fastapi import FastAPI

from app.config import get_settings

app = FastAPI(title="FSRA RAG Assistant", version="0.1.0")


def check_db(url: str) -> bool:
    try:
        with psycopg.connect(url, connect_timeout=2) as conn:
            conn.execute("SELECT 1")
        return True
    except psycopg.Error:
        return False


def check_redis(url: str) -> bool:
    try:
        return bool(redis.Redis.from_url(url, socket_connect_timeout=2).ping())
    except redis.RedisError:
        return False


@app.get("/health")
def health() -> dict:
    """Reports each dependency separately, so a failure points at the culprit."""
    s = get_settings()
    components = {"database": check_db(s.database_url), "redis": check_redis(s.redis_url)}
    return {
        "status": "ok" if all(components.values()) else "degraded",
        "components": components,
    }
