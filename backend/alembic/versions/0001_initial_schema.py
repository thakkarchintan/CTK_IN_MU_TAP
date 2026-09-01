"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

environment_enum = sa.Enum("SIMULATION", "PAPER", "LIVE", name="environment")
deployment_status_enum = sa.Enum("STOPPED", "RUNNING", "PAUSED", "ERROR", name="deploymentstatus")
direction_enum = sa.Enum("LONG", "SHORT", name="direction")
backtest_status_enum = sa.Enum("PENDING", "RUNNING", "COMPLETED", "FAILED", name="backteststatus")
order_status_enum = sa.Enum(
    "PENDING", "SUBMITTED", "FILLED", "PARTIALLY_FILLED", "REJECTED", "CANCELLED", name="orderstatus"
)


def upgrade() -> None:
    bind = op.get_bind()
    environment_enum.create(bind, checkfirst=True)
    deployment_status_enum.create(bind, checkfirst=True)
    direction_enum.create(bind, checkfirst=True)
    backtest_status_enum.create(bind, checkfirst=True)
    order_status_enum.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "strategies",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("instrument", sa.String(64), nullable=False),
        sa.Column("timeframe", sa.String(16), nullable=False),
        sa.Column("created_by", UUID(as_uuid=False), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_strategies_name", "strategies", ["name"])

    op.create_table(
        "strategy_versions",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("strategy_id", UUID(as_uuid=False), sa.ForeignKey("strategies.id"), nullable=False),
        sa.Column("version_no", sa.Integer(), nullable=False),
        sa.Column("params", JSONB, nullable=False),
        sa.Column("entry_logic", JSONB, nullable=False),
        sa.Column("exit_logic", JSONB, nullable=False),
        sa.Column("risk_params", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", UUID(as_uuid=False), sa.ForeignKey("users.id"), nullable=True),
        sa.UniqueConstraint("strategy_id", "version_no", name="uq_strategy_version"),
    )
    op.create_index("ix_strategy_versions_strategy_id", "strategy_versions", ["strategy_id"])

    op.create_table(
        "backtests",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "strategy_version_id", UUID(as_uuid=False), sa.ForeignKey("strategy_versions.id"), nullable=False
        ),
        sa.Column("instrument", sa.String(64), nullable=False),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("timeframe", sa.String(16), nullable=False),
        sa.Column("initial_capital", sa.Numeric(18, 2), nullable=False),
        sa.Column("status", backtest_status_enum, nullable=False, server_default="PENDING"),
        sa.Column("results", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_backtests_strategy_version_id", "backtests", ["strategy_version_id"])

    op.create_table(
        "backtest_trades",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("backtest_id", UUID(as_uuid=False), sa.ForeignKey("backtests.id"), nullable=False),
        sa.Column("entry_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("entry_price", sa.Numeric(18, 4), nullable=False),
        sa.Column("exit_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("exit_price", sa.Numeric(18, 4), nullable=True),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.Column("direction", direction_enum, nullable=False),
        sa.Column("pnl", sa.Numeric(18, 2), nullable=True),
        sa.Column("entry_reason", sa.Text(), nullable=True),
        sa.Column("exit_reason", sa.Text(), nullable=True),
    )
    op.create_index("ix_backtest_trades_backtest_id", "backtest_trades", ["backtest_id"])

    op.create_table(
        "broker_accounts",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=False), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("broker_name", sa.String(64), nullable=False, server_default="ZERODHA"),
        sa.Column("api_key", sa.String(255), nullable=True),
        sa.Column("encrypted_access_token", sa.Text(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "deployments",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "strategy_version_id", UUID(as_uuid=False), sa.ForeignKey("strategy_versions.id"), nullable=False
        ),
        sa.Column("environment", environment_enum, nullable=False),
        sa.Column("status", deployment_status_enum, nullable=False, server_default="STOPPED"),
        sa.Column("capital_allocated", sa.Numeric(18, 2), nullable=False),
        sa.Column("broker_account_id", UUID(as_uuid=False), sa.ForeignKey("broker_accounts.id"), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("stopped_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_deployments_strategy_version_id", "deployments", ["strategy_version_id"])

    op.create_table(
        "orders",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("deployment_id", UUID(as_uuid=False), sa.ForeignKey("deployments.id"), nullable=False),
        sa.Column("broker_order_id", sa.String(128), nullable=True),
        sa.Column("instrument", sa.String(64), nullable=False),
        sa.Column("direction", direction_enum, nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(18, 4), nullable=True),
        sa.Column("order_type", sa.String(32), nullable=False, server_default="MARKET"),
        sa.Column("status", order_status_enum, nullable=False, server_default="PENDING"),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_orders_deployment_id", "orders", ["deployment_id"])

    op.create_table(
        "trades",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("deployment_id", UUID(as_uuid=False), sa.ForeignKey("deployments.id"), nullable=False),
        sa.Column("order_id", UUID(as_uuid=False), sa.ForeignKey("orders.id"), nullable=True),
        sa.Column("instrument", sa.String(64), nullable=False),
        sa.Column("direction", direction_enum, nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(18, 4), nullable=False),
        sa.Column("pnl", sa.Numeric(18, 2), nullable=True),
        sa.Column("executed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_trades_deployment_id_executed_at", "trades", ["deployment_id", "executed_at"])

    op.create_table(
        "positions",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("deployment_id", UUID(as_uuid=False), sa.ForeignKey("deployments.id"), nullable=False),
        sa.Column("instrument", sa.String(64), nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("avg_price", sa.Numeric(18, 4), nullable=True),
        sa.Column("unrealized_pnl", sa.Numeric(18, 2), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_positions_deployment_id", "positions", ["deployment_id"])

    op.create_table(
        "audit_logs",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("user_id", UUID(as_uuid=False), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("strategy_id", UUID(as_uuid=False), sa.ForeignKey("strategies.id"), nullable=True),
        sa.Column("deployment_id", UUID(as_uuid=False), sa.ForeignKey("deployments.id"), nullable=True),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
    )
    op.create_index("ix_audit_logs_timestamp", "audit_logs", ["timestamp"])

    op.create_table(
        "change_logs",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("user_id", UUID(as_uuid=False), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("strategy_id", UUID(as_uuid=False), sa.ForeignKey("strategies.id"), nullable=False),
        sa.Column(
            "strategy_version_id", UUID(as_uuid=False), sa.ForeignKey("strategy_versions.id"), nullable=True
        ),
        sa.Column("field_changed", sa.String(255), nullable=False),
        sa.Column("previous_value", sa.Text(), nullable=True),
        sa.Column("new_value", sa.Text(), nullable=True),
        sa.Column("environment", environment_enum, nullable=True),
    )
    op.create_index("ix_change_logs_timestamp", "change_logs", ["timestamp"])

    op.create_table(
        "build_logs",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("step", sa.String(32), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
    )
    op.create_index("ix_build_logs_timestamp", "build_logs", ["timestamp"])


def downgrade() -> None:
    op.drop_table("build_logs")
    op.drop_table("change_logs")
    op.drop_table("audit_logs")
    op.drop_table("positions")
    op.drop_table("trades")
    op.drop_table("orders")
    op.drop_table("deployments")
    op.drop_table("broker_accounts")
    op.drop_table("backtest_trades")
    op.drop_table("backtests")
    op.drop_table("strategy_versions")
    op.drop_table("strategies")
    op.drop_table("users")

    bind = op.get_bind()
    order_status_enum.drop(bind, checkfirst=True)
    backtest_status_enum.drop(bind, checkfirst=True)
    direction_enum.drop(bind, checkfirst=True)
    deployment_status_enum.drop(bind, checkfirst=True)
    environment_enum.drop(bind, checkfirst=True)
