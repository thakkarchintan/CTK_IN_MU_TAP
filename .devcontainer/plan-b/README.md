# Plan B: Codespace without Docker (cloud Postgres)

Use this only if the default `.devcontainer/devcontainer.json` (docker-compose based) keeps failing to
build. This config runs Python + Node directly in the codespace with no Docker at all, against an
external Postgres (e.g. a free Neon.tech project) instead of a local container.

## Setup

1. When creating the codespace, click the **branch/config picker** on the "Create codespace" screen and
   choose **"V1 Trading Platform (Plan B - no Docker, cloud Postgres)"** instead of the default config.
   (If you already have a codespace open, use Command Palette → "Codespaces: Add Dev Container
   Configuration Files" is not needed — just delete and recreate the codespace, picking this config.)
2. Wait for `postCreateCommand` to finish installing backend/frontend dependencies.
3. Create `backend/.env` (not the repo root `.env` — this one is read by the app directly) with:

   ```
   DATABASE_URL=postgresql+psycopg2://<user>:<password>@<neon-host>/<dbname>?sslmode=require
   SECRET_KEY=dev-only-secret-change-before-any-real-use
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=changeme123
   KITE_API_KEY=
   KITE_API_SECRET=
   KITE_ACCESS_TOKEN=
   ```

   Get the connection string from your Neon project dashboard — it gives you `postgresql://...`;
   just change the scheme to `postgresql+psycopg2://` and keep `?sslmode=require`.

4. In a terminal:

   ```bash
   cd backend
   alembic upgrade head
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. In a second terminal:

   ```bash
   cd frontend
   API_PROXY_TARGET=http://localhost:8000 npm run dev
   ```

6. Open the forwarded port `5173` URL. Log in with `admin@example.com` / `changeme123`.
