"""Webhook receivers — Stripe subscription lifecycle."""

from fastapi import APIRouter, Header, HTTPException, Request, status

from app.core.config import get_settings
from app.core.logging import get_logger

router = APIRouter()
log = get_logger(__name__)


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"),
) -> dict[str, str]:
    """Stripe webhook — verifies signature, updates tenant plan/status.

    Full implementation lands Week 3 days 15-16 once Stripe products exist.
    """
    settings = get_settings()
    if not settings.stripe_webhook_secret:
        log.warning("stripe.webhook.no_secret_configured")
        return {"received": "ignored"}

    if stripe_signature is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing signature.")

    payload = await request.body()
    log.info("stripe.webhook.received", size=len(payload))
    # TODO week 3: stripe.Webhook.construct_event(...) + dispatch by event['type']
    return {"received": "ok"}
