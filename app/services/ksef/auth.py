"""KSeF authentication — wraps ksef-client's challenge → sign → token flow.

Week 1 days 3-4 fills in the real calls. This module stubs the interface so
the rest of the app can be wired up and tested.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class AuthTokens:
    access_token: str
    refresh_token: str
    access_expires_at: datetime
    refresh_expires_at: datetime


async def authenticate_with_ksef_token(
    nip: str,
    ksef_token: str,
    environment: str = "test",
) -> AuthTokens:
    """Exchange a user-provided KSeF token for access+refresh tokens.

    Real impl: uses ksef-client `AuthClient.ksef_token(...)` under the hood.
    """
    raise NotImplementedError("Wired in Week 1 day 3-4.")


async def refresh(refresh_token: str, environment: str = "test") -> AuthTokens:
    """Exchange a refresh token for fresh access+refresh tokens."""
    raise NotImplementedError("Wired in Week 1 day 3-4.")
