"""seed admin user and step 1 build log entry

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-01

"""
import uuid

import sqlalchemy as sa
from alembic import op

from app.core.config import settings
from app.core.security import hash_password

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

users = sa.table(
    "users",
    sa.column("id", sa.String),
    sa.column("email", sa.String),
    sa.column("password_hash", sa.String),
)

build_logs = sa.table(
    "build_logs",
    sa.column("id", sa.String),
    sa.column("step", sa.String),
    sa.column("title", sa.String),
    sa.column("description", sa.Text),
)


def upgrade() -> None:
    op.bulk_insert(
        users,
        [
            {
                "id": str(uuid.uuid4()),
                "email": settings.admin_email,
                "password_hash": hash_password(settings.admin_password),
            }
        ],
    )
    op.bulk_insert(
        build_logs,
        [
            {
                "id": str(uuid.uuid4()),
                "step": "Step 1",
                "title": "Application shell, database schema, and authentication",
                "description": (
                    "Set up the modular-monolith backend (FastAPI + SQLAlchemy + Alembic) and frontend "
                    "(React + TypeScript + Vite + Tailwind) scaffold, Docker Compose environment "
                    "(Postgres + backend + frontend), single-admin JWT authentication, and the initial "
                    "schema for all 13 core tables plus this Build Log. Every subsequent build step will "
                    "add an entry here automatically."
                ),
            }
        ],
    )


def downgrade() -> None:
    op.execute(build_logs.delete().where(build_logs.c.step == "Step 1"))
    op.execute(users.delete().where(users.c.email == settings.admin_email))
