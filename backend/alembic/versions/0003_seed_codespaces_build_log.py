"""seed build log entry for GitHub Codespaces devcontainer

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-01

"""
import uuid

import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

build_logs = sa.table(
    "build_logs",
    sa.column("id", sa.String),
    sa.column("step", sa.String),
    sa.column("title", sa.String),
    sa.column("description", sa.Text),
)

TITLE = "GitHub Codespaces dev environment"


def upgrade() -> None:
    op.bulk_insert(
        build_logs,
        [
            {
                "id": str(uuid.uuid4()),
                "step": "Step 1",
                "title": TITLE,
                "description": (
                    "Added .devcontainer/devcontainer.json so the docker-compose stack (Postgres, "
                    "backend, frontend) runs in GitHub Codespaces without any local Docker install. "
                    "Also made the backend's SECRET_KEY/ADMIN_EMAIL/ADMIN_PASSWORD/KITE_* settings "
                    "fall back to safe dev defaults via docker-compose variable substitution instead "
                    "of requiring a committed .env file, since Codespaces starts from a clean checkout."
                ),
            }
        ],
    )


def downgrade() -> None:
    op.execute(build_logs.delete().where(build_logs.c.title == TITLE))
