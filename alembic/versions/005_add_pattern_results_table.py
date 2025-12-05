"""add pattern_results table

Revision ID: 005
Revises: 004
Create Date: 2025-12-02

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add pattern_results table for daily batch scanner"""
    op.create_table(
        'pattern_results',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('date', sa.Date(), nullable=False, index=True),
        sa.Column('pattern_type', sa.String(50), nullable=False, index=True),
        sa.Column('ticker', sa.String(10), nullable=False, index=True),
        sa.Column('score', sa.Numeric(3, 1), nullable=False, index=True),
        sa.Column('entry_price', sa.Numeric(10, 2), nullable=True),
        sa.Column('stop_price', sa.Numeric(10, 2), nullable=True),
        sa.Column('target_price', sa.Numeric(10, 2), nullable=True),
        sa.Column('chart_url', sa.Text(), nullable=True),
        sa.Column('reasons', JSONB, nullable=True),
        sa.Column('indicators', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint('date', 'pattern_type', 'ticker', name='uq_pattern_result_date_type_ticker'),
    )

    # Create indexes for common queries
    op.create_index('idx_pattern_date', 'pattern_results', ['date', 'pattern_type'])
    op.create_index('idx_pattern_score_desc', 'pattern_results', ['score'], postgresql_using='btree',
                    postgresql_ops={'score': 'DESC'})


def downgrade() -> None:
    """Remove pattern_results table"""
    op.drop_index('idx_pattern_score_desc', 'pattern_results')
    op.drop_index('idx_pattern_date', 'pattern_results')
    op.drop_table('pattern_results')
