"""arq worker settings — KSeF polling, token refresh, incoming-invoice fetch."""

from typing import Any, ClassVar

from arq.connections import RedisSettings

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.workers.poll_upo import poll_upo
from app.workers.refresh_tokens import refresh_tokens

configure_logging()
log = get_logger(__name__)


async def startup(ctx: dict) -> None:
    log.info("worker.startup")


async def shutdown(ctx: dict) -> None:
    log.info("worker.shutdown")


class WorkerSettings:
    functions: ClassVar[list[Any]] = [poll_upo, refresh_tokens]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(str(get_settings().redis_url))
    # Run a token-refresh sweep every 10 minutes
    cron_jobs: ClassVar[list[Any]] = []
