import enum
import uuid

from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Numeric,
    DateTime,
    ForeignKey,
    Enum,
    JSON,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Environment(str, enum.Enum):
    SIMULATION = "SIMULATION"
    PAPER = "PAPER"
    LIVE = "LIVE"


class DeploymentStatus(str, enum.Enum):
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    ERROR = "ERROR"


class Direction(str, enum.Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class BacktestStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    instrument = Column(String(64), nullable=False)
    timeframe = Column(String(16), nullable=False)
    created_by = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    versions = relationship("StrategyVersion", back_populates="strategy", order_by="StrategyVersion.version_no")


class StrategyVersion(Base):
    __tablename__ = "strategy_versions"
    __table_args__ = (
        UniqueConstraint("strategy_id", "version_no", name="uq_strategy_version"),
        Index("ix_strategy_versions_strategy_id", "strategy_id"),
    )

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    strategy_id = Column(UUID(as_uuid=False), ForeignKey("strategies.id"), nullable=False)
    version_no = Column(Integer, nullable=False)
    params = Column(JSONB, nullable=False, default=dict)
    entry_logic = Column(JSONB, nullable=False, default=dict)
    exit_logic = Column(JSONB, nullable=False, default=dict)
    risk_params = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)

    strategy = relationship("Strategy", back_populates="versions")


class Backtest(Base):
    __tablename__ = "backtests"
    __table_args__ = (Index("ix_backtests_strategy_version_id", "strategy_version_id"),)

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    strategy_version_id = Column(UUID(as_uuid=False), ForeignKey("strategy_versions.id"), nullable=False)
    instrument = Column(String(64), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    timeframe = Column(String(16), nullable=False)
    initial_capital = Column(Numeric(18, 2), nullable=False)
    status = Column(Enum(BacktestStatus), nullable=False, default=BacktestStatus.PENDING)
    results = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    strategy_version = relationship("StrategyVersion")
    trades = relationship("BacktestTrade", back_populates="backtest")


class BacktestTrade(Base):
    __tablename__ = "backtest_trades"
    __table_args__ = (Index("ix_backtest_trades_backtest_id", "backtest_id"),)

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    backtest_id = Column(UUID(as_uuid=False), ForeignKey("backtests.id"), nullable=False)
    entry_time = Column(DateTime(timezone=True), nullable=False)
    entry_price = Column(Numeric(18, 4), nullable=False)
    exit_time = Column(DateTime(timezone=True), nullable=True)
    exit_price = Column(Numeric(18, 4), nullable=True)
    qty = Column(Integer, nullable=False)
    direction = Column(Enum(Direction), nullable=False)
    pnl = Column(Numeric(18, 2), nullable=True)
    entry_reason = Column(Text, nullable=True)
    exit_reason = Column(Text, nullable=True)

    backtest = relationship("Backtest", back_populates="trades")


class BrokerAccount(Base):
    __tablename__ = "broker_accounts"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    broker_name = Column(String(64), nullable=False, default="ZERODHA")
    api_key = Column(String(255), nullable=True)
    encrypted_access_token = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Deployment(Base):
    __tablename__ = "deployments"
    __table_args__ = (Index("ix_deployments_strategy_version_id", "strategy_version_id"),)

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    strategy_version_id = Column(UUID(as_uuid=False), ForeignKey("strategy_versions.id"), nullable=False)
    environment = Column(Enum(Environment), nullable=False)
    status = Column(Enum(DeploymentStatus), nullable=False, default=DeploymentStatus.STOPPED)
    capital_allocated = Column(Numeric(18, 2), nullable=False)
    broker_account_id = Column(UUID(as_uuid=False), ForeignKey("broker_accounts.id"), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    stopped_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    strategy_version = relationship("StrategyVersion")
    orders = relationship("Order", back_populates="deployment")
    trades = relationship("Trade", back_populates="deployment")
    positions = relationship("Position", back_populates="deployment")


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (Index("ix_orders_deployment_id", "deployment_id"),)

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    deployment_id = Column(UUID(as_uuid=False), ForeignKey("deployments.id"), nullable=False)
    broker_order_id = Column(String(128), nullable=True)
    instrument = Column(String(64), nullable=False)
    direction = Column(Enum(Direction), nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Numeric(18, 4), nullable=True)
    order_type = Column(String(32), nullable=False, default="MARKET")
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    deployment = relationship("Deployment", back_populates="orders")


class Trade(Base):
    __tablename__ = "trades"
    __table_args__ = (Index("ix_trades_deployment_id_executed_at", "deployment_id", "executed_at"),)

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    deployment_id = Column(UUID(as_uuid=False), ForeignKey("deployments.id"), nullable=False)
    order_id = Column(UUID(as_uuid=False), ForeignKey("orders.id"), nullable=True)
    instrument = Column(String(64), nullable=False)
    direction = Column(Enum(Direction), nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Numeric(18, 4), nullable=False)
    pnl = Column(Numeric(18, 2), nullable=True)
    executed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    deployment = relationship("Deployment", back_populates="trades")


class Position(Base):
    __tablename__ = "positions"
    __table_args__ = (Index("ix_positions_deployment_id", "deployment_id"),)

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    deployment_id = Column(UUID(as_uuid=False), ForeignKey("deployments.id"), nullable=False)
    instrument = Column(String(64), nullable=False)
    qty = Column(Integer, nullable=False, default=0)
    avg_price = Column(Numeric(18, 4), nullable=True)
    unrealized_pnl = Column(Numeric(18, 2), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    deployment = relationship("Deployment", back_populates="positions")


class AuditLog(Base):
    """Immutable system event log (spec section 11) — application code must never update or delete rows here."""

    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_logs_timestamp", "timestamp"),)

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    strategy_id = Column(UUID(as_uuid=False), ForeignKey("strategies.id"), nullable=True)
    deployment_id = Column(UUID(as_uuid=False), ForeignKey("deployments.id"), nullable=True)
    event_type = Column(String(64), nullable=False)
    description = Column(Text, nullable=False)


class ChangeLog(Base):
    """Auto-generated on every strategy/deployment config mutation (spec section 12)."""

    __tablename__ = "change_logs"
    __table_args__ = (Index("ix_change_logs_timestamp", "timestamp"),)

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    strategy_id = Column(UUID(as_uuid=False), ForeignKey("strategies.id"), nullable=False)
    strategy_version_id = Column(UUID(as_uuid=False), ForeignKey("strategy_versions.id"), nullable=True)
    field_changed = Column(String(255), nullable=False)
    previous_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    environment = Column(Enum(Environment), nullable=True)


class BuildLog(Base):
    """Development build log — records each build step/change delivered to this app, shown on the Build Log
    screen so progress is visible in the UI rather than only in chat/git history. Distinct from ChangeLog,
    which tracks strategy/deployment configuration edits made by end users at runtime."""

    __tablename__ = "build_logs"
    __table_args__ = (Index("ix_build_logs_timestamp", "timestamp"),)

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    step = Column(String(32), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
