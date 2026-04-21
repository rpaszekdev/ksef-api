"""Send an FA(3) invoice through KSeF and fetch its UPO.

Week 1 days 5-7 fills in real logic against ksef-client.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SubmitResult:
    reference_number: str
    ksef_number: str | None  # assigned only after acceptance
    status_code: int         # 0 pending, 200 accepted, 4xx rejected


async def submit(
    access_token: str,
    session: "Any",              # OnlineSession from session.py
    invoice_json: dict[str, Any],
    environment: str = "test",
) -> SubmitResult:
    """Accepts a Pydantic-validated JSON invoice, emits FA(3) XML,
    encrypts with AES-256, submits to KSeF, returns the reference number.
    """
    raise NotImplementedError("Wired in Week 1 day 5-7.")


async def fetch_upo(
    access_token: str,
    session_reference: str,
    invoice_reference: str,
    environment: str = "test",
) -> str | None:
    """Poll for UPO XML. Returns XML string once status_code == 200.
    Returns None if still pending; raises on terminal error.
    """
    raise NotImplementedError("Wired in Week 1 day 5-7.")
