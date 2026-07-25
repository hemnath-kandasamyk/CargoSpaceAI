# Backend — AI Cargo Tracking Platform

FastAPI backend implementing auth, shipments, driver, warehouse, and admin modules with JWT auth and role-based access control (RBAC).

## Quick Start

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # then edit DATABASE_URL, JWT_SECRET

# Point .env at a real Postgres DB, then:
alembic revision --autogenerate -m "initial schema"
alembic upgrade head

python scripts/seed_data.py   # optional — creates 4 demo users + sample data
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`
Health check: `http://localhost:8000/health`

Full setup, architecture, schema, and API documentation live in [`../docs`](../docs).

## What's implemented

- **Auth**: register, login, JWT access + refresh tokens, bcrypt password hashing
- **RBAC**: `require_role(...)` dependency enforced on every protected route
- **Shipments**: create, track (with full append-only history), list (scoped per role)
- **Driver**: view assigned deliveries, update delivery status
- **Warehouse**: QR-code inventory scan (receive/dispatch), capacity lookup
- **Admin**: analytics summary, user listing
- **AI routes**: wired and RBAC-protected, returning a clear `MODEL_UNAVAILABLE` response until real models are trained in `/ml` and connected in `app/api/v1/ai.py`
- **Error handling**: every error response follows `{ error_code, message, details }` consistently across validation errors, HTTP errors, and unhandled exceptions
- **Seed script**: `scripts/seed_data.py` creates one user per role (`customer@example.com`, `driver@example.com`, `warehouse@example.com`, `admin@example.com`, all password `password123`) plus a sample warehouse, vehicle, driver, and in-transit shipment

## Verified working (tested against SQLite during development)

Register → login → create shipment → track shipment → RBAC rejection on wrong role → admin analytics → driver delivery update → warehouse scan 404 handling — all confirmed end-to-end before delivery.

## Next steps

1. Point `DATABASE_URL` at a real PostgreSQL instance and run the first Alembic migration
2. Train models in `/ml` per `docs/ml-models.md`, then replace `_placeholder_predict` in `app/api/v1/ai.py` with real inference calls
3. Add `pytest` test files under `backend/tests/` (structure is ready for it — services are already decoupled from route handlers for easy unit testing)
