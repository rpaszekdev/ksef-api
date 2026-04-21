"""Encrypted KSeF auth tokens per client NIP."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models._mixins import TimestampsMixin, UUIDPkMixin


class KsefToken(UUIDPkMixin, TimestampsMixin, Base):
    __tablename__ = "ksef_tokens"

    client_nip_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("client_nips.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # All token values stored Fernet-encrypted.
    access_token_enc: Mapped[str] = mapped_column(String, nullable=False)
    refresh_token_enc: Mapped[str] = mapped_column(String, nullable=False)

    access_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    refresh_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    environment: Mapped[str] = mapped_column(String(10), nullable=False)  # test|demo|prod
