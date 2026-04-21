"""Redis client factory shared by FastAPI and arq workers."""

from redis.asyncio import Redis, from_url

from app.core.config import get_settings


def get_redis() -> Redis:
    settings = get_settings()
    return from_url(str(settings.redis_url), decode_responses=True)
