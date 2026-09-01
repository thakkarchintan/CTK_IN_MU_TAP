"""seed build log entry for Plan B no-Docker devcontainer

Revision ID: 0004
Revises: 0003
Create Date: 2026-09-01

"""
import uuid

import sqlalchemy as sa
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None

build_logs = sa.table(
    "build_logs",
    sa.column("id", sa.String),
    sa.column("step", sa.String),
    sa.column("title", sa.String),
    sa.column("description", sa.Text),
)

TITLE = "Plan B: no-Docker Codespace fallback"


def upgrade() -> None:
    op.bulk_insert(
        build_logs,
        [
            {
                "id": str(uuid.uuid4()),
                "step": "Step 1",
                "title": TITLE,
                "description": (
                    "Added .devcontainer/plan-b/devcontainer.json as an alternate codespace "
                    "configuration that runs Python + Node directly (no docker-compose, no Docker at "
                    "all) against an external Postgres (e.g. Neon) instead of a local container. Added "
                    "for reliability after the default docker-compose devcontainer hit a transient "
                    "GitHub Codespaces host error (runc/setns) during container creation. Also made "
                    "frontend/vite.config.ts's dev-server API proxy target configurable via "
                    "API_PROXY_TARGET so the same frontend code works under both configurations."
                ),
            }
        ],
    )


def downgrade() -> None:
    op.execute(build_logs.delete().where(build_logs.c.title == TITLE))
