"""Invoices tracked through the KSeF lifecycle."""

from enum import StrEnum
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models._mixins import TimestampsMixin, UUIDPkMixin


class InvoiceDirection(StrEnum):
    OUTGOING = "outgoing"  # sprzedażowa
    INCOMING = "incoming"  # zakupowa


class InvoiceStatus(StrEnum):
    PENDING = "pending"
    SUBMITTED = "submitted"    # sent to KSeF, awaiting UPO
    ACCEPTED = "accepted"      # UPO received
    REJECTED = "rejected"
    ERROR = "error"


class Invoice(UUIDPkMixin, TimestampsMixin, Base):
    __tablename__ = "invoices"

    tenant_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    client_nip_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("client_nips.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    direction: Mapped[InvoiceDirection] = mapped_column(
        Enum(InvoiceDirection, name="invoice_direction", native_enum=False),
        nullable=False,
    )
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus, name="invoice_status", native_enum=False),
        default=InvoiceStatus.PENDING,
        nullable=False,
        index=True,
    )

    # KSeF references
    reference_number: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    ksef_number: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    upo_reference: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Raw XML we sent + received (large; may later move to blob storage)
    xml_sent: Mapped[str | None] = mapped_column(String, nullable=True)
    upo_xml: Mapped[str | None] = mapped_column(String, nullable=True)

    # Human readable error from KSeF if rejected
    error_code: Mapped[str | None] = mapped_column(String(16), nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Telemetry
    gross_total_cents: Mapped[int | None] = mapped_column(Integer, nullable=True)
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
