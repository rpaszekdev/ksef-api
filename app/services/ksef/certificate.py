"""MCU certificate enrollment per client NIP.

Week 2 day 10 fills in the real MCU flow.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class EnrolledCertificate:
    serial_number: str
    cert_pem: str
    private_key_pem: str
    not_before: datetime
    not_after: datetime


async def enroll(
    access_token: str,
    cert_type: str = "Authentication",
    environment: str = "test",
) -> EnrolledCertificate:
    """Generate CSR → submit to MCU → poll → download cert."""
    raise NotImplementedError("Wired in Week 2 day 10.")
