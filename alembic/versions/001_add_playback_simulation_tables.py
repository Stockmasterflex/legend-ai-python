"""Add historical playback and simulation tables

Revision ID: 001
Revises:
Create Date: 2025-11-18

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
    # Create historical_playbacks table
    op.create_table(
        'historical_playbacks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('current_position', sa.DateTime(timezone=True), nullable=False),
        sa.Column('playback_speed', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('interval', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_historical_playbacks_id'), 'historical_playbacks', ['id'], unique=False)
    op.create_index(op.f('ix_historical_playbacks_user_id'), 'historical_playbacks', ['user_id'], unique=False)
    op.create_index(op.f('ix_historical_playbacks_ticker_id'), 'historical_playbacks', ['ticker_id'], unique=False)
    op.create_index(op.f('ix_historical_playbacks_start_date'), 'historical_playbacks', ['start_date'], unique=False)
    op.create_index(op.f('ix_historical_playbacks_status'), 'historical_playbacks', ['status'], unique=False)
    op.create_index(op.f('ix_historical_playbacks_created_at'), 'historical_playbacks', ['created_at'], unique=False)

    # Create playback_annotations table
    op.create_table(
        'playback_annotations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('playback_id', sa.Integer(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('annotation_type', sa.String(length=50), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('price_level', sa.Float(), nullable=True),
        sa.Column('metadata', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['playback_id'], ['historical_playbacks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_playback_annotations_id'), 'playback_annotations', ['id'], unique=False)
    op.create_index(op.f('ix_playback_annotations_playback_id'), 'playback_annotations', ['playback_id'], unique=False)
    op.create_index(op.f('ix_playback_annotations_timestamp'), 'playback_annotations', ['timestamp'], unique=False)

    # Create simulation_accounts table
    op.create_table(
        'simulation_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('initial_balance', sa.Float(), nullable=False),
        sa.Column('current_balance', sa.Float(), nullable=False),
        sa.Column('cash_balance', sa.Float(), nullable=False),
        sa.Column('total_pnl', sa.Float(), nullable=True),
        sa.Column('total_pnl_pct', sa.Float(), nullable=True),
        sa.Column('total_trades', sa.Integer(), nullable=True),
        sa.Column('winning_trades', sa.Integer(), nullable=True),
        sa.Column('losing_trades', sa.Integer(), nullable=True),
        sa.Column('win_rate', sa.Float(), nullable=True),
        sa.Column('max_drawdown', sa.Float(), nullable=True),
        sa.Column('sharpe_ratio', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_simulation_accounts_id'), 'simulation_accounts', ['id'], unique=False)
    op.create_index(op.f('ix_simulation_accounts_user_id'), 'simulation_accounts', ['user_id'], unique=False)
    op.create_index(op.f('ix_simulation_accounts_status'), 'simulation_accounts', ['status'], unique=False)
    op.create_index(op.f('ix_simulation_accounts_created_at'), 'simulation_accounts', ['created_at'], unique=False)

    # Create simulation_trades table
    op.create_table(
        'simulation_trades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=True),
        sa.Column('ticker_id', sa.Integer(), nullable=True),
        sa.Column('trade_type', sa.String(length=20), nullable=False),
        sa.Column('entry_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('entry_price', sa.Float(), nullable=False),
        sa.Column('position_size', sa.Integer(), nullable=False),
        sa.Column('stop_loss', sa.Float(), nullable=True),
        sa.Column('target_price', sa.Float(), nullable=True),
        sa.Column('exit_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('exit_price', sa.Float(), nullable=True),
        sa.Column('exit_reason', sa.String(length=100), nullable=True),
        sa.Column('pnl', sa.Float(), nullable=True),
        sa.Column('pnl_pct', sa.Float(), nullable=True),
        sa.Column('r_multiple', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['simulation_accounts.id'], ),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_simulation_trades_id'), 'simulation_trades', ['id'], unique=False)
    op.create_index(op.f('ix_simulation_trades_account_id'), 'simulation_trades', ['account_id'], unique=False)
    op.create_index(op.f('ix_simulation_trades_ticker_id'), 'simulation_trades', ['ticker_id'], unique=False)
    op.create_index(op.f('ix_simulation_trades_entry_date'), 'simulation_trades', ['entry_date'], unique=False)
    op.create_index(op.f('ix_simulation_trades_status'), 'simulation_trades', ['status'], unique=False)

    # Create what_if_scenarios table
    op.create_table(
        'what_if_scenarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=True),
        sa.Column('scenario_name', sa.String(length=255), nullable=True),
        sa.Column('scenario_type', sa.String(length=50), nullable=True),
        sa.Column('base_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('base_price', sa.Float(), nullable=False),
        sa.Column('alternative_entry_price', sa.Float(), nullable=True),
        sa.Column('alternative_entry_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('alternative_exit_price', sa.Float(), nullable=True),
        sa.Column('alternative_exit_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('alternative_stop_loss', sa.Float(), nullable=True),
        sa.Column('alternative_position_size', sa.Integer(), nullable=True),
        sa.Column('base_pnl', sa.Float(), nullable=True),
        sa.Column('alternative_pnl', sa.Float(), nullable=True),
        sa.Column('pnl_difference', sa.Float(), nullable=True),
        sa.Column('pnl_difference_pct', sa.Float(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('results_data', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_what_if_scenarios_id'), 'what_if_scenarios', ['id'], unique=False)
    op.create_index(op.f('ix_what_if_scenarios_user_id'), 'what_if_scenarios', ['user_id'], unique=False)
    op.create_index(op.f('ix_what_if_scenarios_ticker_id'), 'what_if_scenarios', ['ticker_id'], unique=False)
    op.create_index(op.f('ix_what_if_scenarios_scenario_type'), 'what_if_scenarios', ['scenario_type'], unique=False)
    op.create_index(op.f('ix_what_if_scenarios_created_at'), 'what_if_scenarios', ['created_at'], unique=False)

    # Create pattern_quizzes table
    op.create_table(
        'pattern_quizzes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=True),
        sa.Column('quiz_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('pattern_type', sa.String(length=50), nullable=True),
        sa.Column('difficulty', sa.String(length=20), nullable=True),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('correct_answer', sa.String(length=100), nullable=False),
        sa.Column('answer_options', sa.Text(), nullable=True),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('chart_data', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pattern_quizzes_id'), 'pattern_quizzes', ['id'], unique=False)
    op.create_index(op.f('ix_pattern_quizzes_ticker_id'), 'pattern_quizzes', ['ticker_id'], unique=False)
    op.create_index(op.f('ix_pattern_quizzes_quiz_date'), 'pattern_quizzes', ['quiz_date'], unique=False)
    op.create_index(op.f('ix_pattern_quizzes_pattern_type'), 'pattern_quizzes', ['pattern_type'], unique=False)

    # Create quiz_attempts table
    op.create_table(
        'quiz_attempts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('quiz_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.String(length=100), nullable=False),
        sa.Column('user_answer', sa.String(length=100), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('time_taken_seconds', sa.Integer(), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('attempted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['quiz_id'], ['pattern_quizzes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quiz_attempts_id'), 'quiz_attempts', ['id'], unique=False)
    op.create_index(op.f('ix_quiz_attempts_quiz_id'), 'quiz_attempts', ['quiz_id'], unique=False)
    op.create_index(op.f('ix_quiz_attempts_user_id'), 'quiz_attempts', ['user_id'], unique=False)
    op.create_index(op.f('ix_quiz_attempts_attempted_at'), 'quiz_attempts', ['attempted_at'], unique=False)

    # Create replay_bookmarks table
    op.create_table(
        'replay_bookmarks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=False),
        sa.Column('playback_id', sa.Integer(), nullable=True),
        sa.Column('bookmark_name', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tags', sa.Text(), nullable=True),
        sa.Column('is_favorite', sa.Boolean(), nullable=True),
        sa.Column('view_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['playback_id'], ['historical_playbacks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_replay_bookmarks_id'), 'replay_bookmarks', ['id'], unique=False)
    op.create_index(op.f('ix_replay_bookmarks_user_id'), 'replay_bookmarks', ['user_id'], unique=False)
    op.create_index(op.f('ix_replay_bookmarks_playback_id'), 'replay_bookmarks', ['playback_id'], unique=False)
    op.create_index(op.f('ix_replay_bookmarks_created_at'), 'replay_bookmarks', ['created_at'], unique=False)

    # Create shared_replays table
    op.create_table(
        'shared_replays',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('playback_id', sa.Integer(), nullable=True),
        sa.Column('share_token', sa.String(length=64), nullable=False),
        sa.Column('shared_by', sa.String(length=100), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True),
        sa.Column('view_count', sa.Integer(), nullable=True),
        sa.Column('expiration_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['playback_id'], ['historical_playbacks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shared_replays_id'), 'shared_replays', ['id'], unique=False)
    op.create_index(op.f('ix_shared_replays_playback_id'), 'shared_replays', ['playback_id'], unique=False)
    op.create_index(op.f('ix_shared_replays_share_token'), 'shared_replays', ['share_token'], unique=True)
    op.create_index(op.f('ix_shared_replays_shared_by'), 'shared_replays', ['shared_by'], unique=False)
    op.create_index(op.f('ix_shared_replays_created_at'), 'shared_replays', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('shared_replays')
    op.drop_table('replay_bookmarks')
    op.drop_table('quiz_attempts')
    op.drop_table('pattern_quizzes')
    op.drop_table('what_if_scenarios')
    op.drop_table('simulation_trades')
    op.drop_table('simulation_accounts')
    op.drop_table('playback_annotations')
    op.drop_table('historical_playbacks')
