"""A client NIP managed under a biuro (tenant)."""

from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models._mixins import TimestampsMixin, UUIDPkMixin


class ClientNip(UUIDPkMixin, TimestampsMixin, Base):
    __tablename__ = "client_nips"
    __table_args__ = (
        UniqueConstraint("tenant_id", "nip", name="uq_client_nip_per_tenant"),
    )

    tenant_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nip: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Connection status to KSeF for this NIP
    # pending | connected | error | revoked
    ksef_status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    ksef_last_error: Mapped[str | None] = mapped_column(String(500), nullable=True)
