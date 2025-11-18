"""Add portfolio management tables

Revision ID: 001_portfolio_mgmt
Revises:
Create Date: 2025-11-18

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_portfolio_mgmt'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create portfolios table
    op.create_table(
        'portfolios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('initial_capital', sa.Float(), nullable=False),
        sa.Column('cash_balance', sa.Float(), nullable=False),
        sa.Column('total_value', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolios_id'), 'portfolios', ['id'], unique=False)
    op.create_index(op.f('ix_portfolios_user_id'), 'portfolios', ['user_id'], unique=False)

    # Create positions table
    op.create_table(
        'positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('portfolio_id', sa.Integer(), nullable=True),
        sa.Column('ticker_id', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('avg_cost_basis', sa.Float(), nullable=False),
        sa.Column('current_price', sa.Float(), nullable=True),
        sa.Column('total_cost', sa.Float(), nullable=False),
        sa.Column('current_value', sa.Float(), nullable=True),
        sa.Column('unrealized_pnl', sa.Float(), nullable=True),
        sa.Column('unrealized_pnl_pct', sa.Float(), nullable=True),
        sa.Column('stop_loss', sa.Float(), nullable=True),
        sa.Column('target_price', sa.Float(), nullable=True),
        sa.Column('position_size_pct', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('opened_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_positions_id'), 'positions', ['id'], unique=False)
    op.create_index(op.f('ix_positions_portfolio_id'), 'positions', ['portfolio_id'], unique=False)
    op.create_index(op.f('ix_positions_ticker_id'), 'positions', ['ticker_id'], unique=False)
    op.create_index(op.f('ix_positions_status'), 'positions', ['status'], unique=False)
    op.create_index(op.f('ix_positions_opened_at'), 'positions', ['opened_at'], unique=False)

    # Create trade_journals table
    op.create_table(
        'trade_journals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('portfolio_id', sa.Integer(), nullable=True),
        sa.Column('position_id', sa.Integer(), nullable=True),
        sa.Column('ticker_id', sa.Integer(), nullable=True),
        sa.Column('trade_type', sa.String(length=20), nullable=True),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('entry_reason', sa.Text(), nullable=True),
        sa.Column('exit_reason', sa.Text(), nullable=True),
        sa.Column('setup_type', sa.String(length=100), nullable=True),
        sa.Column('screenshot_url', sa.Text(), nullable=True),
        sa.Column('lessons_learned', sa.Text(), nullable=True),
        sa.Column('emotions', sa.String(length=255), nullable=True),
        sa.Column('tags', sa.Text(), nullable=True),
        sa.Column('r_multiple', sa.Float(), nullable=True),
        sa.Column('profit_loss', sa.Float(), nullable=True),
        sa.Column('profit_loss_pct', sa.Float(), nullable=True),
        sa.Column('trade_grade', sa.String(length=5), nullable=True),
        sa.Column('mistakes_made', sa.Text(), nullable=True),
        sa.Column('what_went_well', sa.Text(), nullable=True),
        sa.Column('traded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ),
        sa.ForeignKeyConstraint(['position_id'], ['positions.id'], ),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trade_journals_id'), 'trade_journals', ['id'], unique=False)
    op.create_index(op.f('ix_trade_journals_portfolio_id'), 'trade_journals', ['portfolio_id'], unique=False)
    op.create_index(op.f('ix_trade_journals_position_id'), 'trade_journals', ['position_id'], unique=False)
    op.create_index(op.f('ix_trade_journals_ticker_id'), 'trade_journals', ['ticker_id'], unique=False)
    op.create_index(op.f('ix_trade_journals_trade_type'), 'trade_journals', ['trade_type'], unique=False)
    op.create_index(op.f('ix_trade_journals_traded_at'), 'trade_journals', ['traded_at'], unique=False)


def downgrade():
    # Drop trade_journals table
    op.drop_index(op.f('ix_trade_journals_traded_at'), table_name='trade_journals')
    op.drop_index(op.f('ix_trade_journals_trade_type'), table_name='trade_journals')
    op.drop_index(op.f('ix_trade_journals_ticker_id'), table_name='trade_journals')
    op.drop_index(op.f('ix_trade_journals_position_id'), table_name='trade_journals')
    op.drop_index(op.f('ix_trade_journals_portfolio_id'), table_name='trade_journals')
    op.drop_index(op.f('ix_trade_journals_id'), table_name='trade_journals')
    op.drop_table('trade_journals')

    # Drop positions table
    op.drop_index(op.f('ix_positions_opened_at'), table_name='positions')
    op.drop_index(op.f('ix_positions_status'), table_name='positions')
    op.drop_index(op.f('ix_positions_ticker_id'), table_name='positions')
    op.drop_index(op.f('ix_positions_portfolio_id'), table_name='positions')
    op.drop_index(op.f('ix_positions_id'), table_name='positions')
    op.drop_table('positions')

    # Drop portfolios table
    op.drop_index(op.f('ix_portfolios_user_id'), table_name='portfolios')
    op.drop_index(op.f('ix_portfolios_id'), table_name='portfolios')
    op.drop_table('portfolios')
