"""Health + status endpoints."""

from fastapi import APIRouter

from app import __version__

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@router.get("/status")
async def status() -> dict[str, str]:
    # Week 3: extend with Postgres ping, Redis ping, KSeF environment status
    return {"status": "operational", "version": __version__}
