"""Encrypted KSeF certificates (for offline24 / batch signing) per client NIP."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models._mixins import TimestampsMixin, UUIDPkMixin


class KsefCert(UUIDPkMixin, TimestampsMixin, Base):
    __tablename__ = "ksef_certs"

    client_nip_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("client_nips.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    serial_number: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    cert_type: Mapped[str] = mapped_column(String(20), nullable=False)  # Authentication|Offline
    cert_pem_enc: Mapped[str] = mapped_column(String, nullable=False)
    private_key_enc: Mapped[str] = mapped_column(String, nullable=False)

    not_before: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    not_after: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
