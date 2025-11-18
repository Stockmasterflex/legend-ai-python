"""Add trade plan tables

Revision ID: 001
Revises:
Create Date: 2024-11-18 03:51:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create trade plan tables"""

    # Create trade_plans table
    op.create_table(
        'trade_plans',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('ticker_id', sa.Integer(), sa.ForeignKey('tickers.id'), index=True),
        sa.Column('user_id', sa.String(100), index=True, default='default'),

        # Pattern Analysis
        sa.Column('pattern_type', sa.String(50), index=True),
        sa.Column('pattern_score', sa.Float()),
        sa.Column('current_price', sa.Float()),

        # Entry Zones
        sa.Column('entry_zone_low', sa.Float()),
        sa.Column('entry_zone_high', sa.Float()),
        sa.Column('optimal_entry', sa.Float()),

        # Stop Levels
        sa.Column('initial_stop', sa.Float()),
        sa.Column('trailing_stop', sa.Float(), nullable=True),
        sa.Column('invalidation_price', sa.Float()),

        # Multi-Scenario Targets
        sa.Column('best_case_target', sa.Float()),
        sa.Column('best_case_rr', sa.Float()),
        sa.Column('base_case_target', sa.Float()),
        sa.Column('base_case_rr', sa.Float()),
        sa.Column('worst_case_target', sa.Float(), nullable=True),
        sa.Column('worst_case_rr', sa.Float(), nullable=True),

        # Position Sizing
        sa.Column('account_size', sa.Float()),
        sa.Column('risk_percentage', sa.Float(), default=2.0),
        sa.Column('position_size', sa.Integer()),
        sa.Column('position_value', sa.Float()),
        sa.Column('risk_amount', sa.Float()),

        # Plan Details
        sa.Column('timeframe', sa.String(20)),
        sa.Column('strategy', sa.String(50)),
        sa.Column('notes', sa.Text()),
        sa.Column('checklist', sa.Text()),
        sa.Column('alerts_config', sa.Text()),

        # Trade Execution Tracking
        sa.Column('status', sa.String(20), default='planned', index=True),
        sa.Column('entry_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('exit_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('entry_price_actual', sa.Float(), nullable=True),
        sa.Column('exit_price_actual', sa.Float(), nullable=True),

        # Outcome Tracking
        sa.Column('outcome', sa.String(20), nullable=True, index=True),
        sa.Column('pnl_amount', sa.Float(), nullable=True),
        sa.Column('pnl_percentage', sa.Float(), nullable=True),
        sa.Column('target_hit', sa.String(20), nullable=True),
        sa.Column('lessons_learned', sa.Text(), nullable=True),

        # PDF Export
        sa.Column('pdf_path', sa.String(255), nullable=True),
        sa.Column('chart_url', sa.Text(), nullable=True),

        # Metadata
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), index=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now()),
    )

    # Create trade_plan_alerts table
    op.create_table(
        'trade_plan_alerts',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('trade_plan_id', sa.Integer(), sa.ForeignKey('trade_plans.id'), index=True),
        sa.Column('alert_type', sa.String(50), index=True),
        sa.Column('trigger_price', sa.Float()),
        sa.Column('is_triggered', sa.Boolean(), default=False, index=True),
        sa.Column('triggered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notification_sent', sa.Boolean(), default=False),
        sa.Column('notification_sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
    )

    # Create indexes for better query performance
    op.create_index('idx_trade_plans_user_status', 'trade_plans', ['user_id', 'status'])
    op.create_index('idx_trade_plans_pattern_type', 'trade_plans', ['pattern_type'])
    op.create_index('idx_trade_plan_alerts_triggered', 'trade_plan_alerts', ['is_triggered', 'alert_type'])


def downgrade():
    """Drop trade plan tables"""

    # Drop indexes
    op.drop_index('idx_trade_plan_alerts_triggered', 'trade_plan_alerts')
    op.drop_index('idx_trade_plans_pattern_type', 'trade_plans')
    op.drop_index('idx_trade_plans_user_status', 'trade_plans')

    # Drop tables
    op.drop_table('trade_plan_alerts')
    op.drop_table('trade_plans')
