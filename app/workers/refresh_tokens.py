"""Refresh KSeF access tokens nearing expiry."""

from app.core.logging import get_logger

log = get_logger(__name__)


async def refresh_tokens(ctx: dict) -> dict:
    """Sweep ksef_tokens rows whose access_expires_at is < now + 5min; refresh."""
    log.info("worker.refresh_tokens.stub")
    return {"status": "stub"}
