# ksef-api

[![Python](https://img.shields.io/badge/python-3.12-3776ab?logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Postgres](https://img.shields.io/badge/Postgres-asyncpg-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![licence](https://img.shields.io/badge/licence-MIT-blue)](LICENSE)

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

```
app/
  api/v1/      tenants, clients, invoices, webhooks, health
  core/        config, db, cache (Redis), security, logging
  models/      SQLAlchemy: tenant, client_nip, invoice, ksef_token, ksef_cert, api_key, audit_log
  services/    ksef/ (auth, session, invoice, certificate, environments, errors), crypto, passwords
  workers/     arq jobs — poll_upo, refresh_tokens
  web/static/  zero-dependency HTML playground served at /
alembic/       migrations
tests/         unit + integration
```

Certificates and tokens are encrypted at rest with Fernet; every KSeF
environment (test / demo / prod) is derived from one `KSEF_ENV` setting rather
than scattered URLs.

## Status

**Prototype — built against the KSeF mandate, deployed to Fly.io, since idled.**
It is not running today and never took a paying customer. Published as a
portfolio piece, not as a service you can sign up for.

What works: tenant signup and API keys, client-NIP management, invoice submission
with UPO polling, Fernet-encrypted certificate storage, Stripe plan scaffolding,
and a browser playground that renders submissions as Polish FAKTURA VAT documents
with real QR codes.

What was never finished: production KSeF credentials were never exercised at
volume, and `mypy` runs in CI with `continue-on-error` from the warm-up period.
