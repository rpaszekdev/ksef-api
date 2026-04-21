"""Invoice endpoints. Real KSeF integration lands Week 1 days 5-7."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import (
    InvoiceCreateRequest,
    InvoiceListResponse,
    InvoicePublic,
)
from app.core.db import get_db
from app.core.security import AuthedTenant, require_api_key, tenant_owns_nip
from app.models import ClientNip, Invoice, InvoiceDirection, InvoiceStatus

router = APIRouter()


@router.post("", response_model=InvoicePublic, status_code=status.HTTP_202_ACCEPTED)
async def create_invoice(
    body: InvoiceCreateRequest,
    auth: AuthedTenant = Depends(require_api_key),
    db: AsyncSession = Depends(get_db),
) -> Invoice:
    client_nip_id = await tenant_owns_nip(db, auth.tenant.id, body.seller_nip)
    if client_nip_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"NIP {body.seller_nip} not managed under this tenant. "
                "Add it via POST /v1/clients first."
            ),
        )

    # Persist in PENDING. Week 1 day 5-7: enqueue arq job to build FA(3),
    # open session, submit, update status.
    invoice = Invoice(
        tenant_id=auth.tenant.id,
        client_nip_id=client_nip_id,
        direction=InvoiceDirection.OUTGOING,
        status=InvoiceStatus.PENDING,
        currency=body.currency,
    )
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return invoice


@router.get("", response_model=InvoiceListResponse)
async def list_invoices(
    nip: str | None = Query(default=None, pattern=r"^\d{10}$"),
    direction: InvoiceDirection | None = None,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    auth: AuthedTenant = Depends(require_api_key),
    db: AsyncSession = Depends(get_db),
) -> InvoiceListResponse:
    stmt = select(Invoice).where(Invoice.tenant_id == auth.tenant.id)
    if nip:
        sub = select(ClientNip.id).where(
            ClientNip.tenant_id == auth.tenant.id,
            ClientNip.nip == nip,
        )
        stmt = stmt.where(Invoice.client_nip_id.in_(sub))
    if direction:
        stmt = stmt.where(Invoice.direction == direction)

    total_res = await db.execute(stmt)
    total = len(total_res.scalars().all())

    page_res = await db.execute(
        stmt.order_by(Invoice.created_at.desc()).offset(offset).limit(limit)
    )
    items = list(page_res.scalars().all())
    return InvoiceListResponse(items=items, total=total)


@router.get("/{invoice_id}", response_model=InvoicePublic)
async def get_invoice(
    invoice_id: str,
    auth: AuthedTenant = Depends(require_api_key),
    db: AsyncSession = Depends(get_db),
) -> Invoice:
    result = await db.execute(
        select(Invoice).where(
            Invoice.id == invoice_id,
            Invoice.tenant_id == auth.tenant.id,
        )
    )
    invoice = result.scalar_one_or_none()
    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found.",
        )
    return invoice
