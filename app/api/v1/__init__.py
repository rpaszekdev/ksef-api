"""API v1 router assembly."""

from fastapi import APIRouter

from app.api.v1 import clients, health, invoices, tenants, webhooks

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
router.include_router(clients.router, prefix="/clients", tags=["clients"])
router.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
