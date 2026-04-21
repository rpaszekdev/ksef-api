"""API key hashing/verification + FastAPI dependency for tenant-scoped requests."""

import hashlib
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models import ApiKey, Tenant

_API_KEY_PREFIX = "ksef_"
_API_KEY_BYTES = 32  # 256 bits


@dataclass(slots=True)
class AuthedTenant:
    tenant: Tenant
    api_key: ApiKey


def generate_api_key() -> tuple[str, str, str]:
    """Returns (raw_key, prefix, sha256_hash). Raw key is shown to user ONCE."""
    raw_suffix = secrets.token_urlsafe(_API_KEY_BYTES)
    raw_key = f"{_API_KEY_PREFIX}{raw_suffix}"
    prefix = raw_key[:12]
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    return raw_key, prefix, key_hash


def hash_api_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()


async def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    db: AsyncSession = Depends(get_db),
) -> AuthedTenant:
    """FastAPI dependency: validate X-API-Key and return tenant + api_key row."""
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header.",
        )

    hashed = hash_api_key(x_api_key)

    result = await db.execute(select(ApiKey).where(ApiKey.key_hash == hashed))
    api_key = result.scalar_one_or_none()
    if api_key is None or api_key.revoked_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked API key.",
        )

    tenant_result = await db.execute(select(Tenant).where(Tenant.id == api_key.tenant_id))
    tenant = tenant_result.scalar_one_or_none()
    if tenant is None or not tenant.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant is inactive.",
        )

    # update last_used_at (fire and forget semantics; commit on the request's session)
    api_key.last_used_at = datetime.now(UTC)
    await db.flush()

    return AuthedTenant(tenant=tenant, api_key=api_key)


async def tenant_owns_nip(
    db: AsyncSession, tenant_id: UUID, nip: str
) -> UUID | None:
    """Returns the client_nip.id if the tenant owns this NIP, else None."""
    from app.models import ClientNip  # avoid circular

    result = await db.execute(
        select(ClientNip.id).where(
            ClientNip.tenant_id == tenant_id,
            ClientNip.nip == nip,
        )
    )
    return result.scalar_one_or_none()
