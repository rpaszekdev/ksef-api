"""Poll KSeF for UPO of a submitted invoice."""

from app.core.logging import get_logger

log = get_logger(__name__)


async def poll_upo(ctx: dict, invoice_id: str) -> dict:
    """
    Enqueued after an invoice is submitted. Polls KSeF until UPO is ready
    or max retries exhausted, then updates the Invoice row.

    Real implementation lands in Week 1 days 5-7 once
    services/ksef/invoice.py is wired to ksef-client.
    """
    log.info("worker.poll_upo.stub", invoice_id=invoice_id)
    return {"invoice_id": invoice_id, "status": "stub"}
