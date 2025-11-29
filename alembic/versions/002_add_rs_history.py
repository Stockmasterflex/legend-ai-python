"""Add RS History tracking table

Revision ID: 002_add_rs_history
Revises: 001
Create Date: 2025-11-29 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_add_rs_history'
down_revision = '001'  # Update this to match your latest migration
branch_labels = None
depends_on = None


def upgrade():
    # Create rs_history table for tracking RS ratings over time
    op.create_table(
        'rs_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=False),
        sa.Column('rs_rating', sa.Integer(), nullable=False),
        sa.Column('raw_score', sa.Float(), nullable=True),
        sa.Column('q1_performance', sa.Float(), nullable=True),
        sa.Column('q2_performance', sa.Float(), nullable=True),
        sa.Column('q3_performance', sa.Float(), nullable=True),
        sa.Column('q4_performance', sa.Float(), nullable=True),
        sa.Column('one_year_performance', sa.Float(), nullable=True),
        sa.Column('percentile', sa.Float(), nullable=True),
        sa.Column('universe_rank', sa.Integer(), nullable=True),
        sa.Column('universe_size', sa.Integer(), nullable=True),
        sa.Column('calculated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for efficient queries
    op.create_index('ix_rs_history_ticker_id', 'rs_history', ['ticker_id'])
    op.create_index('ix_rs_history_calculated_at', 'rs_history', ['calculated_at'])
    op.create_index('ix_rs_history_rs_rating', 'rs_history', ['rs_rating'])
    op.create_index('ix_rs_history_ticker_date', 'rs_history', ['ticker_id', 'calculated_at'])


def downgrade():
    # Drop indexes first
    op.drop_index('ix_rs_history_ticker_date', table_name='rs_history')
    op.drop_index('ix_rs_history_rs_rating', table_name='rs_history')
    op.drop_index('ix_rs_history_calculated_at', table_name='rs_history')
    op.drop_index('ix_rs_history_ticker_id', table_name='rs_history')
    
    # Drop table
    op.drop_table('rs_history')

