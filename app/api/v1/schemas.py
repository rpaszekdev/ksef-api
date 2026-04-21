"""Pydantic request/response schemas for API v1."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# --- Tenants ---


class TenantSignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    company_name: str | None = None
    nip: str | None = Field(default=None, pattern=r"^\d{10}$")


class TenantPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: EmailStr
    company_name: str | None
    plan: str
    is_active: bool


class ApiKeyCreated(BaseModel):
    prefix: str
    key: str  # full raw key, shown once
    label: str | None


# --- Clients (managed NIPs) ---


class ClientCreateRequest(BaseModel):
    nip: str = Field(pattern=r"^\d{10}$")
    display_name: str | None = None


class ClientPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nip: str
    display_name: str | None
    ksef_status: str
    ksef_last_error: str | None
    created_at: datetime


class ClientConnectRequest(BaseModel):
    """Step to onboard a client: accept their KSeF token to provision tokens."""
    ksef_token: str = Field(min_length=10)


# --- Invoices ---


class InvoicePartyIn(BaseModel):
    nip: str = Field(pattern=r"^\d{10}$")
    name: str | None = None
    # Extend with address fields as FA(3) requires — expanded in Week 1 day 5-7.


class InvoiceItemIn(BaseModel):
    name: str
    quantity: Decimal = Field(gt=0)
    unit_price_net: Decimal = Field(ge=0)
    vat_rate: Decimal  # 0, 5, 8, 23, "zw", "np" — TODO tighten in day 5-7


class InvoiceCreateRequest(BaseModel):
    seller_nip: str = Field(pattern=r"^\d{10}$")
    buyer: InvoicePartyIn
    items: list[InvoiceItemIn]
    issue_date: datetime
    currency: str = Field(default="PLN", pattern=r"^[A-Z]{3}$")
    external_reference: str | None = None  # your own ID for idempotency


class InvoicePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    direction: str
    status: str
    reference_number: str | None
    ksef_number: str | None
    upo_reference: str | None
    error_code: str | None
    error_message: str | None
    created_at: datetime


class InvoiceListResponse(BaseModel):
    items: list[InvoicePublic]
    total: int


# --- Errors ---


class ErrorResponse(BaseModel):
    detail: str
