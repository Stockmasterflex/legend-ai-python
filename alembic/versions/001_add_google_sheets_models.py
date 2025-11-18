"""Add Google Sheets integration models

Revision ID: 001_sheets_integration
Revises:
Create Date: 2025-01-15 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_sheets_integration'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create trades table
    op.create_table(
        'trades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('trade_id', sa.String(length=50), nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('entry_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('entry_price', sa.Float(), nullable=False),
        sa.Column('stop_loss', sa.Float(), nullable=False),
        sa.Column('target_price', sa.Float(), nullable=False),
        sa.Column('position_size', sa.Integer(), nullable=False),
        sa.Column('risk_amount', sa.Float(), nullable=False),
        sa.Column('reward_amount', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('exit_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('exit_price', sa.Float(), nullable=True),
        sa.Column('profit_loss', sa.Float(), nullable=True),
        sa.Column('profit_loss_pct', sa.Float(), nullable=True),
        sa.Column('r_multiple', sa.Float(), nullable=True),
        sa.Column('win', sa.Boolean(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trades_id'), 'trades', ['id'], unique=False)
    op.create_index(op.f('ix_trades_trade_id'), 'trades', ['trade_id'], unique=True)
    op.create_index(op.f('ix_trades_ticker_id'), 'trades', ['ticker_id'], unique=False)
    op.create_index(op.f('ix_trades_user_id'), 'trades', ['user_id'], unique=False)
    op.create_index(op.f('ix_trades_status'), 'trades', ['status'], unique=False)

    # Create portfolios table
    op.create_table(
        'portfolios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('ticker_id', sa.Integer(), nullable=True),
        sa.Column('shares', sa.Integer(), nullable=False),
        sa.Column('avg_cost', sa.Float(), nullable=False),
        sa.Column('current_price', sa.Float(), nullable=True),
        sa.Column('market_value', sa.Float(), nullable=True),
        sa.Column('cost_basis', sa.Float(), nullable=False),
        sa.Column('unrealized_pnl', sa.Float(), nullable=True),
        sa.Column('unrealized_pnl_pct', sa.Float(), nullable=True),
        sa.Column('position_size_pct', sa.Float(), nullable=True),
        sa.Column('risk_amount', sa.Float(), nullable=True),
        sa.Column('stop_loss', sa.Float(), nullable=True),
        sa.Column('target_price', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('acquired_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolios_id'), 'portfolios', ['id'], unique=False)
    op.create_index(op.f('ix_portfolios_user_id'), 'portfolios', ['user_id'], unique=False)
    op.create_index(op.f('ix_portfolios_ticker_id'), 'portfolios', ['ticker_id'], unique=False)

    # Create sheet_syncs table
    op.create_table(
        'sheet_syncs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sheet_type', sa.String(length=50), nullable=True),
        sa.Column('sheet_id', sa.String(length=255), nullable=False),
        sa.Column('sheet_name', sa.String(length=100), nullable=True),
        sa.Column('last_sync_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_sync_direction', sa.String(length=20), nullable=True),
        sa.Column('records_synced', sa.Integer(), nullable=True),
        sa.Column('sync_status', sa.String(length=20), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sheet_syncs_id'), 'sheet_syncs', ['id'], unique=False)
    op.create_index(op.f('ix_sheet_syncs_sheet_type'), 'sheet_syncs', ['sheet_type'], unique=False)
    op.create_index(op.f('ix_sheet_syncs_last_sync_at'), 'sheet_syncs', ['last_sync_at'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_sheet_syncs_last_sync_at'), table_name='sheet_syncs')
    op.drop_index(op.f('ix_sheet_syncs_sheet_type'), table_name='sheet_syncs')
    op.drop_index(op.f('ix_sheet_syncs_id'), table_name='sheet_syncs')
    op.drop_table('sheet_syncs')

    op.drop_index(op.f('ix_portfolios_ticker_id'), table_name='portfolios')
    op.drop_index(op.f('ix_portfolios_user_id'), table_name='portfolios')
    op.drop_index(op.f('ix_portfolios_id'), table_name='portfolios')
    op.drop_table('portfolios')

    op.drop_index(op.f('ix_trades_status'), table_name='trades')
    op.drop_index(op.f('ix_trades_user_id'), table_name='trades')
    op.drop_index(op.f('ix_trades_ticker_id'), table_name='trades')
    op.drop_index(op.f('ix_trades_trade_id'), table_name='trades')
    op.drop_index(op.f('ix_trades_id'), table_name='trades')
    op.drop_table('trades')
