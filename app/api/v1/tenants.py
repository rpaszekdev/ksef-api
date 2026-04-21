"""Tenant (biuro rachunkowe) endpoints: signup, me, API keys."""

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import ApiKeyCreated, TenantPublic, TenantSignupRequest
from app.core.db import get_db
from app.core.security import AuthedTenant, generate_api_key, require_api_key
from app.models import ApiKey, Tenant

router = APIRouter()

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup", response_model=ApiKeyCreated, status_code=status.HTTP_201_CREATED)
async def signup(
    body: TenantSignupRequest,
    db: AsyncSession = Depends(get_db),
) -> ApiKeyCreated:
    existing = await db.execute(select(Tenant).where(Tenant.email == body.email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered.",
        )

    tenant = Tenant(
        email=body.email,
        password_hash=_pwd.hash(body.password),
        company_name=body.company_name,
        nip=body.nip,
    )
    db.add(tenant)
    await db.flush()

    raw_key, prefix, key_hash = generate_api_key()
    api_key = ApiKey(
        tenant_id=tenant.id,
        prefix=prefix,
        key_hash=key_hash,
        label="default",
    )
    db.add(api_key)
    await db.commit()

    return ApiKeyCreated(prefix=prefix, key=raw_key, label="default")


@router.get("/me", response_model=TenantPublic)
async def get_me(auth: AuthedTenant = Depends(require_api_key)) -> Tenant:
    return auth.tenant
