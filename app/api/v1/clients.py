"""Managed client NIPs under a tenant."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import ClientCreateRequest, ClientPublic
from app.core.db import get_db
from app.core.security import AuthedTenant, require_api_key
from app.models import ClientNip, Plan

router = APIRouter()


_NIP_LIMITS: dict[Plan, int] = {
    Plan.START: 1,
    Plan.SOLO: 5,
    Plan.BIURO: 50,
    Plan.BIURO_PRO: 200,
    Plan.CUSTOM: 10_000,
}


@router.post("", response_model=ClientPublic, status_code=status.HTTP_201_CREATED)
async def add_client(
    body: ClientCreateRequest,
    auth: AuthedTenant = Depends(require_api_key),
    db: AsyncSession = Depends(get_db),
) -> ClientNip:
    count_q = await db.execute(
        select(ClientNip).where(ClientNip.tenant_id == auth.tenant.id)
    )
    count = len(count_q.scalars().all())
    limit = _NIP_LIMITS.get(auth.tenant.plan, 1)
    if count >= limit:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Plan '{auth.tenant.plan}' allows {limit} NIPs. Upgrade to add more.",
        )

    client = ClientNip(
        tenant_id=auth.tenant.id,
        nip=body.nip,
        display_name=body.display_name,
    )
    db.add(client)
    try:
        await db.commit()
    except IntegrityError as err:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This NIP is already managed under your account.",
        ) from err
    await db.refresh(client)
    return client


@router.get("", response_model=list[ClientPublic])
async def list_clients(
    auth: AuthedTenant = Depends(require_api_key),
    db: AsyncSession = Depends(get_db),
) -> list[ClientNip]:
    result = await db.execute(
        select(ClientNip)
        .where(ClientNip.tenant_id == auth.tenant.id)
        .order_by(ClientNip.created_at.desc())
    )
    return list(result.scalars().all())


@router.delete("/{nip}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    nip: str,
    auth: AuthedTenant = Depends(require_api_key),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(ClientNip).where(
            ClientNip.tenant_id == auth.tenant.id,
            ClientNip.nip == nip,
        )
    )
    client = result.scalar_one_or_none()
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")
    await db.delete(client)
    await db.commit()
