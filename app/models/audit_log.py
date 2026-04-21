"""Append-only audit log scoped to a tenant."""

from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models._mixins import TimestampsMixin, UUIDPkMixin


class AuditLog(UUIDPkMixin, TimestampsMixin, Base):
    __tablename__ = "audit_logs"

    tenant_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # format: "api_key:<prefix>" or "user:<email>"
    actor: Mapped[str] = mapped_column(String(80), nullable=False)
    action: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    target_nip: Mapped[str | None] = mapped_column(String(10), nullable=True)
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
