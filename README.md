# ksef-api

Multi-tenant KSeF API wrapper for Polish biura rachunkowe.

One REST API that abstracts the XML/certs/sessions/retries of Poland's Krajowy System e-Faktur (mandatory Apr 1, 2026), designed specifically for accounting offices managing 50–500 client NIPs.

## What this is

- **REST API** — `POST /v1/invoices` with JSON, get back `{ksef_number, upo_url, status}`
- **Multi-tenant** — one biuro account can manage many client NIPs under a flat plan, not per-NIP pricing
- **Dashboard** — per-client KSeF status, recent invoices, errors, cert expiry
- **Billing via Stripe** — Solo / Biuro / Biuro Pro plans
- Runs on Python 3.12 + FastAPI + Postgres + Redis, deploys to Fly.io

## Quickstart (local dev)

```bash
# 1. Clone + install
cd ksef-api
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env     # then fill in secrets

# 2. Infra
docker compose up -d     # Postgres + Redis

# 3. DB
alembic upgrade head

# 4. Run
uvicorn app.main:app --reload
# in another shell:
arq app.workers.WorkerSettings

# 5. Verify
curl http://localhost:8000/v1/health
```

## Structure

See `docs/ARCHITECTURE.md` (coming) or the plan file.

## Status

MVP in progress. Target: chargeable in 3 weeks, first paying biura before Apr 1, 2026.
