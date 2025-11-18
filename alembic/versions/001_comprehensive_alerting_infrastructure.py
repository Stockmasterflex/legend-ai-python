"""Comprehensive alerting infrastructure

Revision ID: 001
Revises:
Create Date: 2025-01-18

Adds comprehensive alerting infrastructure:
- AlertRule: User-defined alert rules with conditions
- AlertCondition: Individual alert conditions (deprecated, using JSON in AlertRule)
- AlertLog: Enhanced alert history tracking
- AlertDelivery: Multi-channel delivery tracking

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Upgrade database schema for comprehensive alerting
    """
    # Create alert_rules table
    op.create_table(
        'alert_rules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('ticker_id', sa.Integer(), nullable=True),
        sa.Column('alert_type', sa.String(length=50), nullable=False),
        sa.Column('condition_logic', sa.String(length=10), nullable=True),
        sa.Column('conditions', sa.JSON(), nullable=False),
        sa.Column('delivery_channels', sa.JSON(), nullable=False),
        sa.Column('delivery_config', sa.JSON(), nullable=True),
        sa.Column('is_enabled', sa.Boolean(), nullable=True),
        sa.Column('is_snoozed', sa.Boolean(), nullable=True),
        sa.Column('snoozed_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('check_frequency', sa.Integer(), nullable=True),
        sa.Column('cooldown_period', sa.Integer(), nullable=True),
        sa.Column('last_triggered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('trigger_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alert_rules_alert_type'), 'alert_rules', ['alert_type'], unique=False)
    op.create_index(op.f('ix_alert_rules_created_at'), 'alert_rules', ['created_at'], unique=False)
    op.create_index(op.f('ix_alert_rules_is_enabled'), 'alert_rules', ['is_enabled'], unique=False)
    op.create_index(op.f('ix_alert_rules_last_triggered_at'), 'alert_rules', ['last_triggered_at'], unique=False)
    op.create_index(op.f('ix_alert_rules_ticker_id'), 'alert_rules', ['ticker_id'], unique=False)
    op.create_index(op.f('ix_alert_rules_user_id'), 'alert_rules', ['user_id'], unique=False)

    # Create alert_conditions table (for granular condition tracking if needed)
    op.create_table(
        'alert_conditions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('rule_id', sa.Integer(), nullable=True),
        sa.Column('field', sa.String(length=100), nullable=False),
        sa.Column('operator', sa.String(length=20), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('value_type', sa.String(length=20), nullable=True),
        sa.Column('time_window', sa.Integer(), nullable=True),
        sa.Column('comparison_period', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['rule_id'], ['alert_rules.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alert_conditions_rule_id'), 'alert_conditions', ['rule_id'], unique=False)

    # Enhance alert_logs table (it already exists, so we add columns)
    op.add_column('alert_logs', sa.Column('rule_id', sa.Integer(), nullable=True))
    op.add_column('alert_logs', sa.Column('alert_title', sa.String(length=200), nullable=True))
    op.add_column('alert_logs', sa.Column('alert_message', sa.Text(), nullable=True))
    op.add_column('alert_logs', sa.Column('trigger_data', sa.JSON(), nullable=True))
    op.add_column('alert_logs', sa.Column('conditions_met', sa.JSON(), nullable=True))
    op.add_column('alert_logs', sa.Column('delivery_channels', sa.JSON(), nullable=True))
    op.add_column('alert_logs', sa.Column('delivery_status', sa.JSON(), nullable=True))
    op.add_column('alert_logs', sa.Column('acknowledged_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('alert_logs', sa.Column('dismissed_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('alert_logs', sa.Column('response_time_ms', sa.Integer(), nullable=True))
    op.add_column('alert_logs', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))

    # Add foreign key for rule_id
    op.create_foreign_key('fk_alert_logs_rule_id', 'alert_logs', 'alert_rules', ['rule_id'], ['id'], ondelete='SET NULL')
    op.create_index(op.f('ix_alert_logs_created_at'), 'alert_logs', ['created_at'], unique=False)
    op.create_index(op.f('ix_alert_logs_rule_id'), 'alert_logs', ['rule_id'], unique=False)
    op.create_index(op.f('ix_alert_logs_status'), 'alert_logs', ['status'], unique=False)

    # Create alert_deliveries table
    op.create_table(
        'alert_deliveries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('alert_log_id', sa.Integer(), nullable=True),
        sa.Column('channel', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('attempts', sa.Integer(), nullable=True),
        sa.Column('max_attempts', sa.Integer(), nullable=True),
        sa.Column('last_attempt_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('next_retry_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('delivered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('failed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('external_id', sa.String(length=200), nullable=True),
        sa.Column('channel_metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['alert_log_id'], ['alert_logs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alert_deliveries_alert_log_id'), 'alert_deliveries', ['alert_log_id'], unique=False)
    op.create_index(op.f('ix_alert_deliveries_channel'), 'alert_deliveries', ['channel'], unique=False)
    op.create_index(op.f('ix_alert_deliveries_created_at'), 'alert_deliveries', ['created_at'], unique=False)


def downgrade() -> None:
    """
    Downgrade database schema - remove alerting tables
    """
    # Drop alert_deliveries
    op.drop_index(op.f('ix_alert_deliveries_created_at'), table_name='alert_deliveries')
    op.drop_index(op.f('ix_alert_deliveries_channel'), table_name='alert_deliveries')
    op.drop_index(op.f('ix_alert_deliveries_alert_log_id'), table_name='alert_deliveries')
    op.drop_table('alert_deliveries')

    # Drop alert_logs enhancements
    op.drop_index(op.f('ix_alert_logs_status'), table_name='alert_logs')
    op.drop_index(op.f('ix_alert_logs_rule_id'), table_name='alert_logs')
    op.drop_index(op.f('ix_alert_logs_created_at'), table_name='alert_logs')
    op.drop_constraint('fk_alert_logs_rule_id', 'alert_logs', type_='foreignkey')
    op.drop_column('alert_logs', 'created_at')
    op.drop_column('alert_logs', 'response_time_ms')
    op.drop_column('alert_logs', 'dismissed_at')
    op.drop_column('alert_logs', 'acknowledged_at')
    op.drop_column('alert_logs', 'delivery_status')
    op.drop_column('alert_logs', 'delivery_channels')
    op.drop_column('alert_logs', 'conditions_met')
    op.drop_column('alert_logs', 'trigger_data')
    op.drop_column('alert_logs', 'alert_message')
    op.drop_column('alert_logs', 'alert_title')
    op.drop_column('alert_logs', 'rule_id')

    # Drop alert_conditions
    op.drop_index(op.f('ix_alert_conditions_rule_id'), table_name='alert_conditions')
    op.drop_table('alert_conditions')

    # Drop alert_rules
    op.drop_index(op.f('ix_alert_rules_user_id'), table_name='alert_rules')
    op.drop_index(op.f('ix_alert_rules_ticker_id'), table_name='alert_rules')
    op.drop_index(op.f('ix_alert_rules_last_triggered_at'), table_name='alert_rules')
    op.drop_index(op.f('ix_alert_rules_is_enabled'), table_name='alert_rules')
    op.drop_index(op.f('ix_alert_rules_created_at'), table_name='alert_rules')
    op.drop_index(op.f('ix_alert_rules_alert_type'), table_name='alert_rules')
    op.drop_table('alert_rules')
