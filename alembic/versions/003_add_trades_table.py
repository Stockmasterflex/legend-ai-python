"""Add trades table for journal

Revision ID: 003
Revises: 002
Create Date: 2025-11-29

"""
from alembic import op
import sqlalchemy as sa

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'trades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker', sa.String(10), nullable=False, index=True),
        sa.Column('pattern', sa.String(50), nullable=True),
        sa.Column('entry_date', sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column('entry_price', sa.Float(), nullable=False),
        sa.Column('stop_price', sa.Float(), nullable=False),
        sa.Column('target_price', sa.Float(), nullable=True),
        sa.Column('exit_date', sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column('exit_price', sa.Float(), nullable=True),
        sa.Column('shares', sa.Integer(), nullable=False),
        sa.Column('profit_loss', sa.Float(), nullable=True),
        sa.Column('r_multiple', sa.Float(), nullable=True),
        sa.Column('status', sa.String(20), server_default='Open', nullable=True, index=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_trades_ticker', 'trades', ['ticker'])
    op.create_index('ix_trades_entry_date', 'trades', ['entry_date'])
    op.create_index('ix_trades_status', 'trades', ['status'])

def downgrade():
    op.drop_index('ix_trades_status', 'trades')
    op.drop_index('ix_trades_entry_date', 'trades')
    op.drop_index('ix_trades_ticker', 'trades')
    op.drop_table('trades')

