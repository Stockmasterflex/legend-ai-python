"""Add backtesting and portfolio tables

Revision ID: 004
Revises: 003
Create Date: 2025-11-29

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Portfolio tables
    op.create_table(
        'portfolios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True, index=True),
        sa.Column('name', sa.String(100), nullable=True),
        sa.Column('initial_capital', sa.Float(), nullable=True),
        sa.Column('cash_balance', sa.Float(), nullable=True),
        sa.Column('total_value', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_portfolios_user_id', 'portfolios', ['user_id'])

    op.create_table(
        'positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('portfolio_id', sa.Integer(), nullable=True, index=True),
        sa.Column('ticker_id', sa.Integer(), nullable=True, index=True),
        sa.Column('quantity', sa.Float(), nullable=True),
        sa.Column('avg_cost_basis', sa.Float(), nullable=True),
        sa.Column('total_cost', sa.Float(), nullable=True),
        sa.Column('current_price', sa.Float(), nullable=True),
        sa.Column('current_value', sa.Float(), nullable=True),
        sa.Column('unrealized_pnl', sa.Float(), nullable=True),
        sa.Column('unrealized_pnl_pct', sa.Float(), nullable=True),
        sa.Column('stop_loss', sa.Float(), nullable=True),
        sa.Column('target_price', sa.Float(), nullable=True),
        sa.Column('position_size_pct', sa.Float(), nullable=True),
        sa.Column('status', sa.String(20), server_default='open', nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('opened_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id']),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_positions_portfolio_id', 'positions', ['portfolio_id'])
    op.create_index('ix_positions_ticker_id', 'positions', ['ticker_id'])

    # Strategy templates (needs to exist before strategies due to foreign key)
    op.create_table(
        'strategy_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(50), nullable=True, index=True),
        sa.Column('strategy_type', sa.String(20), nullable=True),
        sa.Column('template_config', JSON, nullable=True),
        sa.Column('parameters_schema', JSON, nullable=True),
        sa.Column('default_parameters', JSON, nullable=True),
        sa.Column('risk_profile', sa.String(20), nullable=True),
        sa.Column('typical_win_rate', sa.Float(), nullable=True),
        sa.Column('typical_sharpe', sa.Float(), nullable=True),
        sa.Column('tags', JSON, nullable=True),
        sa.Column('is_public', sa.Boolean(), server_default='true', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_strategy_templates_category', 'strategy_templates', ['category'])

    # Strategies
    op.create_table(
        'strategies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('strategy_type', sa.String(20), nullable=False),
        sa.Column('yaml_config', sa.Text(), nullable=True),
        sa.Column('python_code', sa.Text(), nullable=True),
        sa.Column('visual_config', JSON, nullable=True),
        sa.Column('parameters', JSON, nullable=True),
        sa.Column('entry_rules', JSON, nullable=True),
        sa.Column('exit_rules', JSON, nullable=True),
        sa.Column('risk_management', JSON, nullable=True),
        sa.Column('template_id', sa.Integer(), nullable=True),
        sa.Column('version', sa.Integer(), server_default='1', nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['template_id'], ['strategy_templates.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Backtest runs
    op.create_table(
        'backtest_runs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('strategy_id', sa.Integer(), nullable=True, index=True),
        sa.Column('name', sa.String(100), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('initial_capital', sa.Float(), server_default='100000.0', nullable=True),
        sa.Column('universe', JSON, nullable=True),
        sa.Column('commission_model', JSON, nullable=True),
        sa.Column('slippage_model', JSON, nullable=True),
        sa.Column('market_impact_model', JSON, nullable=True),
        sa.Column('allow_partial_fills', sa.Boolean(), server_default='false', nullable=True),
        sa.Column('status', sa.String(20), server_default='pending', nullable=True),
        sa.Column('progress', sa.Float(), server_default='0.0', nullable=True),
        sa.Column('final_value', sa.Float(), nullable=True),
        sa.Column('total_return', sa.Float(), nullable=True),
        sa.Column('sharpe_ratio', sa.Float(), nullable=True),
        sa.Column('max_drawdown', sa.Float(), nullable=True),
        sa.Column('total_trades', sa.Integer(), nullable=True),
        sa.Column('win_rate', sa.Float(), nullable=True),
        sa.Column('profit_factor', sa.Float(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['strategy_id'], ['strategies.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_backtest_runs_strategy_id', 'backtest_runs', ['strategy_id'])

    # Backtest trades
    op.create_table(
        'backtest_trades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('backtest_run_id', sa.Integer(), nullable=True, index=True),
        sa.Column('ticker_id', sa.Integer(), nullable=True, index=True),
        sa.Column('entry_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('exit_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('entry_price', sa.Float(), nullable=True),
        sa.Column('exit_price', sa.Float(), nullable=True),
        sa.Column('position_size', sa.Float(), nullable=True),
        sa.Column('direction', sa.String(10), server_default='long', nullable=True),
        sa.Column('gross_profit_loss', sa.Float(), nullable=True),
        sa.Column('commission', sa.Float(), nullable=True),
        sa.Column('slippage', sa.Float(), nullable=True),
        sa.Column('net_profit_loss', sa.Float(), nullable=True),
        sa.Column('profit_loss_pct', sa.Float(), nullable=True),
        sa.Column('r_multiple', sa.Float(), nullable=True),
        sa.Column('days_held', sa.Integer(), nullable=True),
        sa.Column('exit_reason', sa.String(50), nullable=True),
        sa.Column('entry_signal', JSON, nullable=True),
        sa.Column('exit_signal', JSON, nullable=True),
        sa.ForeignKeyConstraint(['backtest_run_id'], ['backtest_runs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_backtest_trades_backtest_run_id', 'backtest_trades', ['backtest_run_id'])
    op.create_index('ix_backtest_trades_ticker_id', 'backtest_trades', ['ticker_id'])

    # Backtest metrics
    op.create_table(
        'backtest_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('backtest_run_id', sa.Integer(), nullable=True, unique=True),
        sa.Column('total_return', sa.Float(), nullable=True),
        sa.Column('annualized_return', sa.Float(), nullable=True),
        sa.Column('sharpe_ratio', sa.Float(), nullable=True),
        sa.Column('sortino_ratio', sa.Float(), nullable=True),
        sa.Column('calmar_ratio', sa.Float(), nullable=True),
        sa.Column('max_drawdown', sa.Float(), nullable=True),
        sa.Column('max_drawdown_duration_days', sa.Integer(), nullable=True),
        sa.Column('win_rate', sa.Float(), nullable=True),
        sa.Column('profit_factor', sa.Float(), nullable=True),
        sa.Column('avg_win', sa.Float(), nullable=True),
        sa.Column('avg_loss', sa.Float(), nullable=True),
        sa.Column('largest_win', sa.Float(), nullable=True),
        sa.Column('largest_loss', sa.Float(), nullable=True),
        sa.Column('avg_trade_duration_days', sa.Float(), nullable=True),
        sa.Column('total_trades', sa.Integer(), nullable=True),
        sa.Column('winning_trades', sa.Integer(), nullable=True),
        sa.Column('losing_trades', sa.Integer(), nullable=True),
        sa.Column('exposure_pct', sa.Float(), nullable=True),
        sa.Column('volatility', sa.Float(), nullable=True),
        sa.Column('beta', sa.Float(), nullable=True),
        sa.Column('alpha', sa.Float(), nullable=True),
        sa.Column('equity_curve', JSON, nullable=True),
        sa.Column('drawdown_curve', JSON, nullable=True),
        sa.Column('monthly_returns', JSON, nullable=True),
        sa.ForeignKeyConstraint(['backtest_run_id'], ['backtest_runs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Walk-forward runs
    op.create_table(
        'walk_forward_runs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('strategy_id', sa.Integer(), nullable=True, index=True),
        sa.Column('name', sa.String(100), nullable=True),
        sa.Column('total_start_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_end_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('in_sample_period_days', sa.Integer(), nullable=True),
        sa.Column('out_sample_period_days', sa.Integer(), nullable=True),
        sa.Column('step_size_days', sa.Integer(), nullable=True),
        sa.Column('parameter_ranges', JSON, nullable=True),
        sa.Column('optimization_metric', sa.String(50), nullable=True),
        sa.Column('n_trials', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(20), server_default='pending', nullable=True),
        sa.Column('progress', sa.Float(), server_default='0.0', nullable=True),
        sa.Column('n_windows', sa.Integer(), nullable=True),
        sa.Column('completed_windows', sa.Integer(), nullable=True),
        sa.Column('combined_oos_return', sa.Float(), nullable=True),
        sa.Column('combined_oos_sharpe', sa.Float(), nullable=True),
        sa.Column('robustness_score', sa.Float(), nullable=True),
        sa.Column('window_results', JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['strategy_id'], ['strategies.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_walk_forward_runs_strategy_id', 'walk_forward_runs', ['strategy_id'])

    # Monte Carlo runs
    op.create_table(
        'monte_carlo_runs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('backtest_run_id', sa.Integer(), nullable=True, index=True),
        sa.Column('name', sa.String(100), nullable=True),
        sa.Column('n_simulations', sa.Integer(), nullable=True),
        sa.Column('simulation_types', JSON, nullable=True),
        sa.Column('entry_delay_range', JSON, nullable=True),
        sa.Column('position_size_variation_pct', sa.Float(), nullable=True),
        sa.Column('include_regime_changes', sa.Boolean(), server_default='false', nullable=True),
        sa.Column('status', sa.String(20), server_default='pending', nullable=True),
        sa.Column('progress', sa.Float(), server_default='0.0', nullable=True),
        sa.Column('baseline_return', sa.Float(), nullable=True),
        sa.Column('mean_return', sa.Float(), nullable=True),
        sa.Column('median_return', sa.Float(), nullable=True),
        sa.Column('return_std', sa.Float(), nullable=True),
        sa.Column('percentile_5', sa.Float(), nullable=True),
        sa.Column('percentile_95', sa.Float(), nullable=True),
        sa.Column('probability_of_profit', sa.Float(), nullable=True),
        sa.Column('value_at_risk_95', sa.Float(), nullable=True),
        sa.Column('return_distribution', JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['backtest_run_id'], ['backtest_runs.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_monte_carlo_runs_backtest_run_id', 'monte_carlo_runs', ['backtest_run_id'])

    # Hyperparameter optimizations
    op.create_table(
        'hyperparameter_optimizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('strategy_id', sa.Integer(), nullable=True, index=True),
        sa.Column('model_type', sa.String(50), nullable=True),
        sa.Column('parameter_space', JSON, nullable=True),
        sa.Column('optimization_type', sa.String(20), nullable=True),
        sa.Column('n_trials', sa.Integer(), nullable=True),
        sa.Column('objective_metric', sa.String(50), nullable=True),
        sa.Column('status', sa.String(20), server_default='pending', nullable=True),
        sa.Column('progress', sa.Float(), server_default='0.0', nullable=True),
        sa.Column('best_params', JSON, nullable=True),
        sa.Column('best_score', sa.Float(), nullable=True),
        sa.Column('all_results', JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['strategy_id'], ['strategies.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_hyperparameter_optimizations_strategy_id', 'hyperparameter_optimizations', ['strategy_id'])


def downgrade():
    op.drop_index('ix_hyperparameter_optimizations_strategy_id', 'hyperparameter_optimizations')
    op.drop_table('hyperparameter_optimizations')
    
    op.drop_index('ix_monte_carlo_runs_backtest_run_id', 'monte_carlo_runs')
    op.drop_table('monte_carlo_runs')
    
    op.drop_index('ix_walk_forward_runs_strategy_id', 'walk_forward_runs')
    op.drop_table('walk_forward_runs')
    
    op.drop_table('backtest_metrics')
    
    op.drop_index('ix_backtest_trades_ticker_id', 'backtest_trades')
    op.drop_index('ix_backtest_trades_backtest_run_id', 'backtest_trades')
    op.drop_table('backtest_trades')
    
    op.drop_index('ix_backtest_runs_strategy_id', 'backtest_runs')
    op.drop_table('backtest_runs')
    
    op.drop_table('strategies')
    
    op.drop_index('ix_strategy_templates_category', 'strategy_templates')
    op.drop_table('strategy_templates')
    
    op.drop_index('ix_positions_ticker_id', 'positions')
    op.drop_index('ix_positions_portfolio_id', 'positions')
    op.drop_table('positions')
    
    op.drop_index('ix_portfolios_user_id', 'portfolios')
    op.drop_table('portfolios')
