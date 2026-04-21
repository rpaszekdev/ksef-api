"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-22 00:00:00

"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("company_name", sa.String(255)),
        sa.Column("nip", sa.String(10)),
        sa.Column(
            "plan",
            sa.String(20),
            nullable=False,
            server_default="start",
        ),
        sa.Column("stripe_customer_id", sa.String(64)),
        sa.Column("stripe_subscription_id", sa.String(64)),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("email", name="uq_tenants_email"),
    )
    op.create_index("ix_tenants_email", "tenants", ["email"])
    op.create_index("ix_tenants_stripe_customer", "tenants", ["stripe_customer_id"])

    op.create_table(
        "api_keys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "tenant_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("prefix", sa.String(12), nullable=False),
        sa.Column("key_hash", sa.String(64), nullable=False),
        sa.Column("label", sa.String(80)),
        sa.Column("last_used_at", sa.DateTime(timezone=True)),
        sa.Column("revoked_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("key_hash", name="uq_api_keys_hash"),
    )
    op.create_index("ix_api_keys_tenant", "api_keys", ["tenant_id"])
    op.create_index("ix_api_keys_prefix", "api_keys", ["prefix"])

    op.create_table(
        "client_nips",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "tenant_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("nip", sa.String(10), nullable=False),
        sa.Column("display_name", sa.String(255)),
        sa.Column("ksef_status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("ksef_last_error", sa.String(500)),
        sa.UniqueConstraint("tenant_id", "nip", name="uq_client_nip_per_tenant"),
    )
    op.create_index("ix_client_nips_tenant", "client_nips", ["tenant_id"])
    op.create_index("ix_client_nips_nip", "client_nips", ["nip"])

    op.create_table(
        "ksef_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "client_nip_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("client_nips.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("access_token_enc", sa.Text, nullable=False),
        sa.Column("refresh_token_enc", sa.Text, nullable=False),
        sa.Column("access_expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("refresh_expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("environment", sa.String(10), nullable=False),
    )
    op.create_index("ix_ksef_tokens_client", "ksef_tokens", ["client_nip_id"])

    op.create_table(
        "ksef_certs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "client_nip_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("client_nips.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("serial_number", sa.String(64), nullable=False),
        sa.Column("cert_type", sa.String(20), nullable=False),
        sa.Column("cert_pem_enc", sa.Text, nullable=False),
        sa.Column("private_key_enc", sa.Text, nullable=False),
        sa.Column("not_before", sa.DateTime(timezone=True), nullable=False),
        sa.Column("not_after", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_ksef_certs_client", "ksef_certs", ["client_nip_id"])
    op.create_index("ix_ksef_certs_serial", "ksef_certs", ["serial_number"])

    op.create_table(
        "invoices",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "tenant_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "client_nip_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("client_nips.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("direction", sa.String(10), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("reference_number", sa.String(64)),
        sa.Column("ksef_number", sa.String(64)),
        sa.Column("upo_reference", sa.String(64)),
        sa.Column("xml_sent", sa.Text),
        sa.Column("upo_xml", sa.Text),
        sa.Column("error_code", sa.String(16)),
        sa.Column("error_message", sa.String(500)),
        sa.Column("gross_total_cents", sa.Integer),
        sa.Column("currency", sa.String(3)),
    )
    op.create_index("ix_invoices_tenant", "invoices", ["tenant_id"])
    op.create_index("ix_invoices_client", "invoices", ["client_nip_id"])
    op.create_index("ix_invoices_status", "invoices", ["status"])
    op.create_index("ix_invoices_reference", "invoices", ["reference_number"])
    op.create_index("ix_invoices_ksef_number", "invoices", ["ksef_number"])

    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "tenant_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("actor", sa.String(80), nullable=False),
        sa.Column("action", sa.String(80), nullable=False),
        sa.Column("target_nip", sa.String(10)),
        sa.Column("payload", postgresql.JSONB),
    )
    op.create_index("ix_audit_tenant", "audit_logs", ["tenant_id"])
    op.create_index("ix_audit_action", "audit_logs", ["action"])


def downgrade() -> None:
    op.drop_index("ix_audit_action", table_name="audit_logs")
    op.drop_index("ix_audit_tenant", table_name="audit_logs")
    op.drop_table("audit_logs")

    op.drop_index("ix_invoices_ksef_number", table_name="invoices")
    op.drop_index("ix_invoices_reference", table_name="invoices")
    op.drop_index("ix_invoices_status", table_name="invoices")
    op.drop_index("ix_invoices_client", table_name="invoices")
    op.drop_index("ix_invoices_tenant", table_name="invoices")
    op.drop_table("invoices")

    op.drop_index("ix_ksef_certs_serial", table_name="ksef_certs")
    op.drop_index("ix_ksef_certs_client", table_name="ksef_certs")
    op.drop_table("ksef_certs")

    op.drop_index("ix_ksef_tokens_client", table_name="ksef_tokens")
    op.drop_table("ksef_tokens")

    op.drop_index("ix_client_nips_nip", table_name="client_nips")
    op.drop_index("ix_client_nips_tenant", table_name="client_nips")
    op.drop_table("client_nips")

    op.drop_index("ix_api_keys_prefix", table_name="api_keys")
    op.drop_index("ix_api_keys_tenant", table_name="api_keys")
    op.drop_table("api_keys")

    op.drop_index("ix_tenants_stripe_customer", table_name="tenants")
    op.drop_index("ix_tenants_email", table_name="tenants")
    op.drop_table("tenants")
