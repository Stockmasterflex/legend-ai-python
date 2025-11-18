"""Add tax optimization tables

Revision ID: 001_tax_optimization
Revises:
Create Date: 2024-11-18

Adds tables for:
- TaxLot: Individual tax lot tracking
- CapitalGain: Realized capital gains/losses
- WashSale: Wash sale violation tracking
- TaxHarvestLog: Tax loss harvesting log
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '001_tax_optimization'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create tax optimization tables"""

    # Create holding_period enum
    op.execute("""
        CREATE TYPE holdingperiodenum AS ENUM ('short_term', 'long_term')
    """)

    # Create wash_sale_status enum
    op.execute("""
        CREATE TYPE washsalestatusenum AS ENUM ('clean', 'violation', 'pending')
    """)

    # Create tax_lots table
    op.create_table(
        'tax_lots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('ticker_id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('remaining_quantity', sa.Float(), nullable=False),
        sa.Column('cost_basis', sa.Float(), nullable=False),
        sa.Column('price_per_share', sa.Float(), nullable=False),
        sa.Column('purchase_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('holding_period', postgresql.ENUM('short_term', 'long_term', name='holdingperiodenum', create_type=False), nullable=True),
        sa.Column('wash_sale_disallowed', sa.Float(), nullable=True, server_default='0'),
        sa.Column('adjusted_cost_basis', sa.Float(), nullable=False),
        sa.Column('trade_id', sa.String(length=100), nullable=True),
        sa.Column('is_closed', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tax_lots_id'), 'tax_lots', ['id'])
    op.create_index(op.f('ix_tax_lots_user_id'), 'tax_lots', ['user_id'])
    op.create_index(op.f('ix_tax_lots_ticker_id'), 'tax_lots', ['ticker_id'])
    op.create_index(op.f('ix_tax_lots_symbol'), 'tax_lots', ['symbol'])
    op.create_index(op.f('ix_tax_lots_purchase_date'), 'tax_lots', ['purchase_date'])
    op.create_index(op.f('ix_tax_lots_trade_id'), 'tax_lots', ['trade_id'])
    op.create_index(op.f('ix_tax_lots_is_closed'), 'tax_lots', ['is_closed'])

    # Create capital_gains table
    op.create_table(
        'capital_gains',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('ticker_id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('tax_lot_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('sale_price', sa.Float(), nullable=False),
        sa.Column('sale_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('proceeds', sa.Float(), nullable=False),
        sa.Column('cost_basis', sa.Float(), nullable=False),
        sa.Column('adjusted_cost_basis', sa.Float(), nullable=False),
        sa.Column('gain_loss', sa.Float(), nullable=False),
        sa.Column('holding_period', postgresql.ENUM('short_term', 'long_term', name='holdingperiodenum', create_type=False), nullable=False),
        sa.Column('wash_sale_loss_disallowed', sa.Float(), nullable=True, server_default='0'),
        sa.Column('tax_year', sa.Integer(), nullable=False),
        sa.Column('trade_id', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.ForeignKeyConstraint(['tax_lot_id'], ['tax_lots.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_capital_gains_id'), 'capital_gains', ['id'])
    op.create_index(op.f('ix_capital_gains_user_id'), 'capital_gains', ['user_id'])
    op.create_index(op.f('ix_capital_gains_ticker_id'), 'capital_gains', ['ticker_id'])
    op.create_index(op.f('ix_capital_gains_symbol'), 'capital_gains', ['symbol'])
    op.create_index(op.f('ix_capital_gains_tax_lot_id'), 'capital_gains', ['tax_lot_id'])
    op.create_index(op.f('ix_capital_gains_sale_date'), 'capital_gains', ['sale_date'])
    op.create_index(op.f('ix_capital_gains_tax_year'), 'capital_gains', ['tax_year'])
    op.create_index(op.f('ix_capital_gains_trade_id'), 'capital_gains', ['trade_id'])

    # Create wash_sales table
    op.create_table(
        'wash_sales',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('loss_sale_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('loss_amount', sa.Float(), nullable=False),
        sa.Column('loss_quantity', sa.Float(), nullable=False),
        sa.Column('loss_tax_lot_id', sa.Integer(), nullable=False),
        sa.Column('replacement_purchase_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('replacement_quantity', sa.Float(), nullable=True),
        sa.Column('replacement_tax_lot_id', sa.Integer(), nullable=True),
        sa.Column('status', postgresql.ENUM('clean', 'violation', 'pending', name='washsalestatusenum', create_type=False), nullable=False, server_default='pending'),
        sa.Column('days_between', sa.Integer(), nullable=True),
        sa.Column('disallowed_loss', sa.Float(), nullable=True, server_default='0'),
        sa.Column('suggested_alternatives', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['loss_tax_lot_id'], ['tax_lots.id'], ),
        sa.ForeignKeyConstraint(['replacement_tax_lot_id'], ['tax_lots.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wash_sales_id'), 'wash_sales', ['id'])
    op.create_index(op.f('ix_wash_sales_user_id'), 'wash_sales', ['user_id'])
    op.create_index(op.f('ix_wash_sales_symbol'), 'wash_sales', ['symbol'])
    op.create_index(op.f('ix_wash_sales_loss_sale_date'), 'wash_sales', ['loss_sale_date'])
    op.create_index(op.f('ix_wash_sales_replacement_purchase_date'), 'wash_sales', ['replacement_purchase_date'])

    # Create tax_harvest_logs table
    op.create_table(
        'tax_harvest_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=False),
        sa.Column('tax_lot_id', sa.Integer(), nullable=False),
        sa.Column('unrealized_loss', sa.Float(), nullable=False),
        sa.Column('current_price', sa.Float(), nullable=False),
        sa.Column('cost_basis', sa.Float(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('estimated_tax_savings', sa.Float(), nullable=False),
        sa.Column('tax_bracket', sa.Float(), nullable=True),
        sa.Column('action_taken', sa.String(length=50), nullable=True),
        sa.Column('harvest_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('replacement_symbol', sa.String(length=10), nullable=True),
        sa.Column('replacement_similarity_score', sa.Float(), nullable=True),
        sa.Column('identified_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.ForeignKeyConstraint(['tax_lot_id'], ['tax_lots.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tax_harvest_logs_id'), 'tax_harvest_logs', ['id'])
    op.create_index(op.f('ix_tax_harvest_logs_user_id'), 'tax_harvest_logs', ['user_id'])
    op.create_index(op.f('ix_tax_harvest_logs_symbol'), 'tax_harvest_logs', ['symbol'])
    op.create_index(op.f('ix_tax_harvest_logs_ticker_id'), 'tax_harvest_logs', ['ticker_id'])
    op.create_index(op.f('ix_tax_harvest_logs_action_taken'), 'tax_harvest_logs', ['action_taken'])
    op.create_index(op.f('ix_tax_harvest_logs_identified_at'), 'tax_harvest_logs', ['identified_at'])


def downgrade() -> None:
    """Drop tax optimization tables"""

    op.drop_index(op.f('ix_tax_harvest_logs_identified_at'), table_name='tax_harvest_logs')
    op.drop_index(op.f('ix_tax_harvest_logs_action_taken'), table_name='tax_harvest_logs')
    op.drop_index(op.f('ix_tax_harvest_logs_ticker_id'), table_name='tax_harvest_logs')
    op.drop_index(op.f('ix_tax_harvest_logs_symbol'), table_name='tax_harvest_logs')
    op.drop_index(op.f('ix_tax_harvest_logs_user_id'), table_name='tax_harvest_logs')
    op.drop_index(op.f('ix_tax_harvest_logs_id'), table_name='tax_harvest_logs')
    op.drop_table('tax_harvest_logs')

    op.drop_index(op.f('ix_wash_sales_replacement_purchase_date'), table_name='wash_sales')
    op.drop_index(op.f('ix_wash_sales_loss_sale_date'), table_name='wash_sales')
    op.drop_index(op.f('ix_wash_sales_symbol'), table_name='wash_sales')
    op.drop_index(op.f('ix_wash_sales_user_id'), table_name='wash_sales')
    op.drop_index(op.f('ix_wash_sales_id'), table_name='wash_sales')
    op.drop_table('wash_sales')

    op.drop_index(op.f('ix_capital_gains_trade_id'), table_name='capital_gains')
    op.drop_index(op.f('ix_capital_gains_tax_year'), table_name='capital_gains')
    op.drop_index(op.f('ix_capital_gains_sale_date'), table_name='capital_gains')
    op.drop_index(op.f('ix_capital_gains_tax_lot_id'), table_name='capital_gains')
    op.drop_index(op.f('ix_capital_gains_symbol'), table_name='capital_gains')
    op.drop_index(op.f('ix_capital_gains_ticker_id'), table_name='capital_gains')
    op.drop_index(op.f('ix_capital_gains_user_id'), table_name='capital_gains')
    op.drop_index(op.f('ix_capital_gains_id'), table_name='capital_gains')
    op.drop_table('capital_gains')

    op.drop_index(op.f('ix_tax_lots_is_closed'), table_name='tax_lots')
    op.drop_index(op.f('ix_tax_lots_trade_id'), table_name='tax_lots')
    op.drop_index(op.f('ix_tax_lots_purchase_date'), table_name='tax_lots')
    op.drop_index(op.f('ix_tax_lots_symbol'), table_name='tax_lots')
    op.drop_index(op.f('ix_tax_lots_ticker_id'), table_name='tax_lots')
    op.drop_index(op.f('ix_tax_lots_user_id'), table_name='tax_lots')
    op.drop_index(op.f('ix_tax_lots_id'), table_name='tax_lots')
    op.drop_table('tax_lots')

    # Drop enums
    op.execute("DROP TYPE IF EXISTS washsalestatusenum")
    op.execute("DROP TYPE IF EXISTS holdingperiodenum")
