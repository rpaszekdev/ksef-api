"""KSeF session management (online + batch).

Week 1 days 5-7 fills in real logic against ksef-client.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class OnlineSession:
    reference_number: str
    symmetric_key: bytes          # AES-256 used to encrypt invoice payloads
    iv: bytes
    encrypted_key_b64: str        # RSA-OAEP(MF public key, symmetric_key)


async def open_online_session(access_token: str, environment: str = "test") -> OnlineSession:
    """Opens a new interactive session. Max 10_000 invoices / 12h TTL."""
    raise NotImplementedError("Wired in Week 1 day 5-7.")


async def close_online_session(
    access_token: str,
    reference_number: str,
    environment: str = "test",
) -> None:
    """Finalizes a session; UPO generation is async after close."""
    raise NotImplementedError("Wired in Week 1 day 5-7.")
