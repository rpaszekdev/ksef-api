"""Tenant = biuro rachunkowe account (one subscription, many managed client NIPs)."""

from enum import StrEnum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models._mixins import TimestampsMixin, UUIDPkMixin


class Plan(StrEnum):
    START = "start"        # 1 NIP, 20 inv/mo (trial)
    SOLO = "solo"          # 5 NIPs, 300 inv/mo, 79 PLN
    BIURO = "biuro"        # 50 NIPs, 3000 inv/mo, 299 PLN (primary target)
    BIURO_PRO = "biuro_pro"  # 200 NIPs, 20k inv/mo, 799 PLN
    CUSTOM = "custom"


class Tenant(UUIDPkMixin, TimestampsMixin, Base):
    __tablename__ = "tenants"

    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nip: Mapped[str | None] = mapped_column(String(10), nullable=True)  # biuro's own NIP

    plan: Mapped[Plan] = mapped_column(
        Enum(Plan, name="plan_enum", native_enum=False),
        default=Plan.START,
        nullable=False,
    )
    stripe_customer_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    stripe_subscription_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Tenant {self.email} plan={self.plan}>"
