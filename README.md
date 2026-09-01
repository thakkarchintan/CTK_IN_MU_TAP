# V1 Trading Platform

Modular-monolith trading platform: FastAPI + PostgreSQL backend, React + TypeScript frontend, pluggable
broker layer (Zerodha Kite Connect first). See `Build Log` in the app UI for a running record of what has
been built at each step.

## Prerequisites

- Docker Desktop (with WSL2 backend on Windows)

## Running locally

1. Copy `.env.example` to `.env` if you haven't already, and fill in real values (a dev `.env` with
   placeholder auth values is already included for local use — do not reuse it anywhere real).
2. From the repo root:

   ```bash
   docker compose up --build
   ```

3. Backend API: http://localhost:8000 (docs at `/docs`)
4. Frontend: http://localhost:5173
5. Log in with the seeded admin user (`ADMIN_EMAIL` / `ADMIN_PASSWORD` from `.env`, defaults to
   `admin@example.com` / `changeme123`).

Migrations run automatically on `backend` container startup (`alembic upgrade head`). To run them manually:

```bash
docker compose exec backend alembic upgrade head
```

## Project structure

```
backend/app/
    api/            FastAPI routers
    core/           config, db session, security
    models/         SQLAlchemy models
    schemas/        Pydantic schemas
    services/       business logic
    strategies/      strategy logic (Step 2+)
    backtesting/     backtest engine (Step 3)
    execution/       execution engine / signal routing (Step 4)
    brokers/         broker adapters incl. KiteBroker (Step 3 data, Step 6 orders)
    logging/         audit log / change log helpers (Step 2)
frontend/src/
    pages/, layouts/, components/, services/, hooks/, types/
```

## Build steps

1. **Step 1 (this one)** — app shell, DB schema, Docker Compose, single-admin auth
2. Strategy management, versioning, Change Log, Audit Log
3. Backtesting engine + results UI
4. Execution engine, Simulation mode, Deployment dashboard
5. Paper trading
6. Zerodha Kite live integration
