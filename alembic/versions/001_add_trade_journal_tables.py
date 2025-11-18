"""Add trade journal tables

Revision ID: 001
Revises:
Create Date: 2024-11-18 00:00:00.000000

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
    """Create trade journal tables"""

    # Create trade_journals table
    op.create_table(
        'trade_journals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(100), nullable=True, index=True),
        sa.Column('ticker_id', sa.Integer(), nullable=True),
        sa.Column('pattern_scan_id', sa.Integer(), nullable=True),
        sa.Column('trade_id', sa.String(50), nullable=True),
        sa.Column('status', sa.Enum('PLANNED', 'OPEN', 'CLOSED', 'CANCELLED', name='tradestatus'), nullable=True),

        # Pre-Trade Planning
        sa.Column('pattern_identified', sa.String(100), nullable=True),
        sa.Column('thesis', sa.Text(), nullable=True),
        sa.Column('planned_entry', sa.Float(), nullable=True),
        sa.Column('planned_stop', sa.Float(), nullable=True),
        sa.Column('planned_target', sa.Float(), nullable=True),
        sa.Column('planned_position_size', sa.Integer(), nullable=True),
        sa.Column('planned_risk_amount', sa.Float(), nullable=True),
        sa.Column('planned_risk_reward', sa.Float(), nullable=True),
        sa.Column('checklist_completed', sa.Boolean(), nullable=True),
        sa.Column('checklist_data', sa.JSON(), nullable=True),
        sa.Column('screenshot_url', sa.Text(), nullable=True),

        # Actual Execution
        sa.Column('actual_entry_price', sa.Float(), nullable=True),
        sa.Column('actual_stop_price', sa.Float(), nullable=True),
        sa.Column('actual_target_price', sa.Float(), nullable=True),
        sa.Column('actual_position_size', sa.Integer(), nullable=True),
        sa.Column('entry_timestamp', sa.DateTime(timezone=True), nullable=True),
        sa.Column('exit_timestamp', sa.DateTime(timezone=True), nullable=True),

        # Slippage Tracking
        sa.Column('entry_slippage', sa.Float(), nullable=True),
        sa.Column('exit_slippage', sa.Float(), nullable=True),
        sa.Column('slippage_cost', sa.Float(), nullable=True),

        # Exit Details
        sa.Column('exit_price', sa.Float(), nullable=True),
        sa.Column('exit_reason', sa.String(100), nullable=True),
        sa.Column('partial_exits', sa.JSON(), nullable=True),

        # Performance Metrics
        sa.Column('gross_pnl', sa.Float(), nullable=True),
        sa.Column('net_pnl', sa.Float(), nullable=True),
        sa.Column('r_multiple', sa.Float(), nullable=True),
        sa.Column('fees_paid', sa.Float(), nullable=True),
        sa.Column('holding_period_hours', sa.Float(), nullable=True),
        sa.Column('mae', sa.Float(), nullable=True),
        sa.Column('mfe', sa.Float(), nullable=True),

        # Emotional & Market Context
        sa.Column('emotional_state_entry', sa.Enum('CONFIDENT', 'FEARFUL', 'GREEDY', 'NEUTRAL', 'ANXIOUS', 'DISCIPLINED', 'IMPULSIVE', name='emotionalstate'), nullable=True),
        sa.Column('emotional_state_exit', sa.Enum('CONFIDENT', 'FEARFUL', 'GREEDY', 'NEUTRAL', 'ANXIOUS', 'DISCIPLINED', 'IMPULSIVE', name='emotionalstate'), nullable=True),
        sa.Column('market_condition', sa.Enum('TRENDING_UP', 'TRENDING_DOWN', 'CONSOLIDATING', 'VOLATILE', 'QUIET', name='marketcondition'), nullable=True),
        sa.Column('market_context', sa.Text(), nullable=True),

        # Follow-through & Notes
        sa.Column('follow_through_notes', sa.Text(), nullable=True),
        sa.Column('what_went_well', sa.Text(), nullable=True),
        sa.Column('what_went_wrong', sa.Text(), nullable=True),
        sa.Column('lessons_learned', sa.Text(), nullable=True),

        # Metadata
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id']),
        sa.ForeignKeyConstraint(['pattern_scan_id'], ['pattern_scans.id'])
    )

    # Create indexes
    op.create_index('ix_trade_journals_user_id', 'trade_journals', ['user_id'])
    op.create_index('ix_trade_journals_ticker_id', 'trade_journals', ['ticker_id'])
    op.create_index('ix_trade_journals_pattern_scan_id', 'trade_journals', ['pattern_scan_id'])
    op.create_index('ix_trade_journals_trade_id', 'trade_journals', ['trade_id'], unique=True)
    op.create_index('ix_trade_journals_status', 'trade_journals', ['status'])
    op.create_index('ix_trade_journals_entry_timestamp', 'trade_journals', ['entry_timestamp'])
    op.create_index('ix_trade_journals_exit_timestamp', 'trade_journals', ['exit_timestamp'])
    op.create_index('ix_trade_journals_created_at', 'trade_journals', ['created_at'])

    # Create trade_tags table
    op.create_table(
        'trade_tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('trade_journal_id', sa.Integer(), nullable=True),
        sa.Column('tag', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['trade_journal_id'], ['trade_journals.id'])
    )
    op.create_index('ix_trade_tags_trade_journal_id', 'trade_tags', ['trade_journal_id'])
    op.create_index('ix_trade_tags_tag', 'trade_tags', ['tag'])

    # Create trade_mistakes table
    op.create_table(
        'trade_mistakes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('trade_journal_id', sa.Integer(), nullable=True),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('mistake_type', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('impact', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['trade_journal_id'], ['trade_journals.id'])
    )
    op.create_index('ix_trade_mistakes_trade_journal_id', 'trade_mistakes', ['trade_journal_id'])
    op.create_index('ix_trade_mistakes_category', 'trade_mistakes', ['category'])

    # Create playbooks table
    op.create_table(
        'playbooks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(100), nullable=True),
        sa.Column('name', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('pattern_type', sa.String(50), nullable=True),
        sa.Column('entry_criteria', sa.JSON(), nullable=True),
        sa.Column('exit_criteria', sa.JSON(), nullable=True),
        sa.Column('risk_management', sa.JSON(), nullable=True),
        sa.Column('success_rate', sa.Float(), nullable=True),
        sa.Column('avg_r_multiple', sa.Float(), nullable=True),
        sa.Column('total_trades', sa.Integer(), nullable=True),
        sa.Column('winning_trades', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_playbooks_user_id', 'playbooks', ['user_id'])
    op.create_index('ix_playbooks_name', 'playbooks', ['name'])
    op.create_index('ix_playbooks_pattern_type', 'playbooks', ['pattern_type'])

    # Create trade_lessons table
    op.create_table(
        'trade_lessons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(100), nullable=True),
        sa.Column('title', sa.String(200), nullable=True),
        sa.Column('lesson', sa.Text(), nullable=True),
        sa.Column('pattern_type', sa.String(50), nullable=True),
        sa.Column('importance', sa.String(20), nullable=True),
        sa.Column('trades_count', sa.Integer(), nullable=True),
        sa.Column('last_occurred', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_trade_lessons_user_id', 'trade_lessons', ['user_id'])
    op.create_index('ix_trade_lessons_pattern_type', 'trade_lessons', ['pattern_type'])

    # Create trade_reviews table
    op.create_table(
        'trade_reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(100), nullable=True),
        sa.Column('review_period', sa.String(20), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_trades', sa.Integer(), nullable=True),
        sa.Column('winning_trades', sa.Integer(), nullable=True),
        sa.Column('losing_trades', sa.Integer(), nullable=True),
        sa.Column('win_rate', sa.Float(), nullable=True),
        sa.Column('avg_win', sa.Float(), nullable=True),
        sa.Column('avg_loss', sa.Float(), nullable=True),
        sa.Column('total_pnl', sa.Float(), nullable=True),
        sa.Column('best_trade_id', sa.String(50), nullable=True),
        sa.Column('worst_trade_id', sa.String(50), nullable=True),
        sa.Column('review_notes', sa.Text(), nullable=True),
        sa.Column('improvement_areas', sa.JSON(), nullable=True),
        sa.Column('goals_next_period', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_trade_reviews_user_id', 'trade_reviews', ['user_id'])
    op.create_index('ix_trade_reviews_start_date', 'trade_reviews', ['start_date'])
    op.create_index('ix_trade_reviews_end_date', 'trade_reviews', ['end_date'])


def downgrade() -> None:
    """Drop trade journal tables"""

    op.drop_table('trade_reviews')
    op.drop_table('trade_lessons')
    op.drop_table('playbooks')
    op.drop_table('trade_mistakes')
    op.drop_table('trade_tags')
    op.drop_table('trade_journals')

    # Drop enums
    op.execute('DROP TYPE IF EXISTS tradestatus')
    op.execute('DROP TYPE IF EXISTS emotionalstate')
    op.execute('DROP TYPE IF EXISTS marketcondition')
