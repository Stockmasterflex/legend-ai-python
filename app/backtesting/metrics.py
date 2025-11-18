"""
Performance Metrics
Comprehensive performance analytics for backtest results
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from scipy import stats


@dataclass
class PerformanceMetrics:
    """Complete performance metrics for a backtest"""

    # Returns
    total_return: float
    annualized_return: float
    cumulative_return: float

    # Risk-adjusted returns
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    omega_ratio: float

    # Risk metrics
    max_drawdown: float
    max_drawdown_duration: int
    volatility: float
    downside_deviation: float
    var_95: float  # Value at Risk
    cvar_95: float  # Conditional VaR

    # Trade statistics
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float

    # Profit metrics
    profit_factor: float
    average_win: float
    average_loss: float
    largest_win: float
    largest_loss: float
    expectancy: float

    # Position metrics
    avg_bars_held: float
    avg_days_held: float

    # R-multiples
    avg_r_multiple: Optional[float] = None

    # Relative metrics
    alpha: Optional[float] = None
    beta: Optional[float] = None

    # Additional metrics
    recovery_factor: Optional[float] = None
    payoff_ratio: Optional[float] = None
    kelly_criterion: Optional[float] = None


def calculate_metrics(
    equity_curve: pd.DataFrame,
    trades: pd.DataFrame,
    initial_capital: float,
    benchmark_returns: Optional[pd.Series] = None,
    risk_free_rate: float = 0.02,  # 2% annual
) -> PerformanceMetrics:
    """
    Calculate comprehensive performance metrics

    Args:
        equity_curve: DataFrame with columns [timestamp, total_value, ...]
        trades: DataFrame with trade details
        initial_capital: Starting capital
        benchmark_returns: Optional benchmark returns for alpha/beta
        risk_free_rate: Annual risk-free rate for Sharpe calculation

    Returns:
        PerformanceMetrics object
    """
    # Calculate returns
    returns = equity_curve["total_value"].pct_change().dropna()
    cumulative_returns = (equity_curve["total_value"] / initial_capital) - 1

    # Total and annualized returns
    total_return = ((equity_curve["total_value"].iloc[-1] / initial_capital) - 1) * 100
    days = len(equity_curve)
    years = days / 252  # Trading days
    annualized_return = (((equity_curve["total_value"].iloc[-1] / initial_capital) ** (1 / years)) - 1) * 100 if years > 0 else 0

    # Volatility
    volatility = returns.std() * np.sqrt(252) * 100  # Annualized

    # Sharpe Ratio
    excess_returns = returns - (risk_free_rate / 252)
    sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252) if excess_returns.std() > 0 else 0

    # Sortino Ratio (using downside deviation)
    downside_returns = returns[returns < 0]
    downside_deviation = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0.0001
    sortino_ratio = (excess_returns.mean() / downside_returns.std()) * np.sqrt(252) if len(downside_returns) > 0 and downside_returns.std() > 0 else 0

    # Drawdown calculations
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max * 100
    max_drawdown = abs(drawdown.min())

    # Max drawdown duration
    is_drawdown = drawdown < 0
    drawdown_periods = is_drawdown.astype(int).groupby((~is_drawdown).cumsum()).sum()
    max_drawdown_duration = drawdown_periods.max() if len(drawdown_periods) > 0 else 0

    # Calmar Ratio
    calmar_ratio = abs(annualized_return / max_drawdown) if max_drawdown > 0 else 0

    # Omega Ratio (probability-weighted ratio of gains vs losses)
    threshold = risk_free_rate / 252
    gains = returns[returns > threshold] - threshold
    losses = threshold - returns[returns < threshold]
    omega_ratio = gains.sum() / losses.sum() if losses.sum() > 0 else 0

    # Value at Risk (VaR) - 95% confidence
    var_95 = np.percentile(returns, 5) * 100

    # Conditional VaR (CVaR) - expected loss beyond VaR
    cvar_95 = returns[returns <= np.percentile(returns, 5)].mean() * 100 if len(returns[returns <= np.percentile(returns, 5)]) > 0 else 0

    # Trade statistics
    if len(trades) > 0:
        winning_trades_df = trades[trades["net_pnl"] > 0]
        losing_trades_df = trades[trades["net_pnl"] < 0]

        total_trades = len(trades)
        winning_trades = len(winning_trades_df)
        losing_trades = len(losing_trades_df)
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

        # Profit metrics
        average_win = winning_trades_df["net_pnl"].mean() if winning_trades > 0 else 0
        average_loss = losing_trades_df["net_pnl"].mean() if losing_trades > 0 else 0
        largest_win = trades["net_pnl"].max()
        largest_loss = trades["net_pnl"].min()

        # Profit factor
        gross_profit = winning_trades_df["net_pnl"].sum() if winning_trades > 0 else 0
        gross_loss = abs(losing_trades_df["net_pnl"].sum()) if losing_trades > 0 else 0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0

        # Expectancy
        expectancy = (win_rate / 100 * average_win) - ((100 - win_rate) / 100 * abs(average_loss))

        # Position metrics
        avg_bars_held = trades["bars_held"].mean() if "bars_held" in trades.columns else 0
        avg_days_held = trades["days_held"].mean() if "days_held" in trades.columns else 0

        # R-multiples
        r_multiples = trades["r_multiple"].dropna()
        avg_r_multiple = r_multiples.mean() if len(r_multiples) > 0 else None

        # Payoff ratio
        payoff_ratio = abs(average_win / average_loss) if average_loss != 0 else 0

        # Kelly Criterion
        if average_loss != 0:
            kelly_criterion = (win_rate / 100) - ((100 - win_rate) / 100) / payoff_ratio
        else:
            kelly_criterion = None

    else:
        # No trades
        total_trades = 0
        winning_trades = 0
        losing_trades = 0
        win_rate = 0
        profit_factor = 0
        average_win = 0
        average_loss = 0
        largest_win = 0
        largest_loss = 0
        expectancy = 0
        avg_bars_held = 0
        avg_days_held = 0
        avg_r_multiple = None
        payoff_ratio = None
        kelly_criterion = None

    # Alpha and Beta (if benchmark provided)
    alpha = None
    beta = None
    if benchmark_returns is not None and len(benchmark_returns) > 0:
        # Align returns
        aligned_returns = pd.DataFrame({"strategy": returns, "benchmark": benchmark_returns})
        aligned_returns = aligned_returns.dropna()

        if len(aligned_returns) > 1:
            # Beta: covariance(strategy, benchmark) / variance(benchmark)
            covariance = aligned_returns["strategy"].cov(aligned_returns["benchmark"])
            benchmark_var = aligned_returns["benchmark"].var()
            beta = covariance / benchmark_var if benchmark_var > 0 else None

            # Alpha: strategy return - (risk_free + beta * (benchmark - risk_free))
            if beta is not None:
                strategy_return = aligned_returns["strategy"].mean() * 252
                benchmark_return = aligned_returns["benchmark"].mean() * 252
                alpha = strategy_return - (risk_free_rate + beta * (benchmark_return - risk_free_rate))

    # Recovery factor
    net_profit = equity_curve["total_value"].iloc[-1] - initial_capital
    recovery_factor = net_profit / (initial_capital * (max_drawdown / 100)) if max_drawdown > 0 else None

    return PerformanceMetrics(
        total_return=total_return,
        annualized_return=annualized_return,
        cumulative_return=cumulative_returns.iloc[-1] * 100 if len(cumulative_returns) > 0 else 0,
        sharpe_ratio=sharpe_ratio,
        sortino_ratio=sortino_ratio,
        calmar_ratio=calmar_ratio,
        omega_ratio=omega_ratio,
        max_drawdown=max_drawdown,
        max_drawdown_duration=int(max_drawdown_duration),
        volatility=volatility,
        downside_deviation=downside_deviation,
        var_95=var_95,
        cvar_95=cvar_95,
        total_trades=total_trades,
        winning_trades=winning_trades,
        losing_trades=losing_trades,
        win_rate=win_rate,
        profit_factor=profit_factor,
        average_win=average_win,
        average_loss=average_loss,
        largest_win=largest_win,
        largest_loss=largest_loss,
        expectancy=expectancy,
        avg_bars_held=avg_bars_held,
        avg_days_held=avg_days_held,
        avg_r_multiple=avg_r_multiple,
        alpha=alpha,
        beta=beta,
        recovery_factor=recovery_factor,
        payoff_ratio=payoff_ratio,
        kelly_criterion=kelly_criterion,
    )


def calculate_rolling_metrics(
    equity_curve: pd.DataFrame,
    window: int = 30,
) -> pd.DataFrame:
    """
    Calculate rolling performance metrics

    Args:
        equity_curve: DataFrame with equity curve
        window: Rolling window size in days

    Returns:
        DataFrame with rolling metrics
    """
    returns = equity_curve["total_value"].pct_change()

    rolling_sharpe = (
        returns.rolling(window).mean() / returns.rolling(window).std() * np.sqrt(252)
    )

    rolling_volatility = returns.rolling(window).std() * np.sqrt(252) * 100

    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.rolling(window).max()
    rolling_drawdown = ((cumulative - rolling_max) / rolling_max * 100).abs()

    rolling_metrics = pd.DataFrame({
        "sharpe": rolling_sharpe,
        "volatility": rolling_volatility,
        "drawdown": rolling_drawdown,
    })

    return rolling_metrics


def monte_carlo_confidence_bands(
    simulations: List[pd.Series],
    confidence_levels: List[float] = [0.05, 0.25, 0.50, 0.75, 0.95],
) -> pd.DataFrame:
    """
    Calculate confidence bands from Monte Carlo simulations

    Args:
        simulations: List of equity curves from simulations
        confidence_levels: Percentiles to calculate

    Returns:
        DataFrame with confidence bands
    """
    # Stack all simulations
    all_sims = pd.DataFrame(simulations).T

    # Calculate percentiles
    bands = {}
    for level in confidence_levels:
        bands[f"p{int(level*100)}"] = all_sims.quantile(level, axis=1)

    return pd.DataFrame(bands)


def calculate_trade_analysis(trades: pd.DataFrame) -> Dict:
    """
    Detailed trade analysis

    Args:
        trades: DataFrame with trade details

    Returns:
        Dictionary with trade analysis
    """
    if len(trades) == 0:
        return {}

    analysis = {}

    # Win/Loss streaks
    trades_sorted = trades.sort_values("entry_date")
    is_winner = (trades_sorted["net_pnl"] > 0).astype(int)
    streaks = is_winner.groupby((is_winner != is_winner.shift()).cumsum()).cumsum()

    win_streaks = streaks[is_winner == 1]
    loss_streaks = streaks[is_winner == 0]

    analysis["max_win_streak"] = win_streaks.max() if len(win_streaks) > 0 else 0
    analysis["max_loss_streak"] = loss_streaks.max() if len(loss_streaks) > 0 else 0

    # MAE/MFE analysis
    if "mae" in trades.columns and "mfe" in trades.columns:
        winning_trades = trades[trades["net_pnl"] > 0]
        losing_trades = trades[trades["net_pnl"] < 0]

        analysis["avg_mae"] = trades["mae"].mean()
        analysis["avg_mfe"] = trades["mfe"].mean()

        if len(winning_trades) > 0:
            analysis["avg_mae_winners"] = winning_trades["mae"].mean()
            analysis["avg_mfe_winners"] = winning_trades["mfe"].mean()

        if len(losing_trades) > 0:
            analysis["avg_mae_losers"] = losing_trades["mae"].mean()
            analysis["avg_mfe_losers"] = losing_trades["mfe"].mean()

    # Trade duration analysis
    if "days_held" in trades.columns:
        winning_trades = trades[trades["net_pnl"] > 0]
        losing_trades = trades[trades["net_pnl"] < 0]

        analysis["avg_hold_time_winners"] = winning_trades["days_held"].mean() if len(winning_trades) > 0 else 0
        analysis["avg_hold_time_losers"] = losing_trades["days_held"].mean() if len(losing_trades) > 0 else 0

    # Exit reason analysis
    if "exit_reason" in trades.columns:
        exit_reasons = trades["exit_reason"].value_counts().to_dict()
        analysis["exit_reasons"] = exit_reasons

    # Pattern performance
    if "pattern_type" in trades.columns:
        pattern_performance = {}
        for pattern in trades["pattern_type"].unique():
            if pd.notna(pattern):
                pattern_trades = trades[trades["pattern_type"] == pattern]
                pattern_performance[pattern] = {
                    "total_trades": len(pattern_trades),
                    "win_rate": (len(pattern_trades[pattern_trades["net_pnl"] > 0]) / len(pattern_trades)) * 100,
                    "avg_pnl": pattern_trades["net_pnl"].mean(),
                    "total_pnl": pattern_trades["net_pnl"].sum(),
                }
        analysis["pattern_performance"] = pattern_performance

    # Monthly/Quarterly analysis
    if "entry_date" in trades.columns:
        trades_with_date = trades.copy()
        trades_with_date["entry_date"] = pd.to_datetime(trades_with_date["entry_date"])
        trades_with_date["month"] = trades_with_date["entry_date"].dt.to_period("M")
        trades_with_date["quarter"] = trades_with_date["entry_date"].dt.to_period("Q")

        monthly_pnl = trades_with_date.groupby("month")["net_pnl"].sum().to_dict()
        quarterly_pnl = trades_with_date.groupby("quarter")["net_pnl"].sum().to_dict()

        analysis["monthly_pnl"] = {str(k): v for k, v in monthly_pnl.items()}
        analysis["quarterly_pnl"] = {str(k): v for k, v in quarterly_pnl.items()}

    return analysis


def overfitting_score(
    in_sample_sharpe: float,
    out_sample_sharpe: float,
    in_sample_return: float,
    out_sample_return: float,
    n_parameters: int,
) -> float:
    """
    Calculate overfitting score

    Args:
        in_sample_sharpe: In-sample Sharpe ratio
        out_sample_sharpe: Out-of-sample Sharpe ratio
        in_sample_return: In-sample return
        out_sample_return: Out-of-sample return
        n_parameters: Number of optimized parameters

    Returns:
        Overfitting score (0-1, higher = more overfit)
    """
    # Sharpe degradation
    sharpe_degradation = (in_sample_sharpe - out_sample_sharpe) / in_sample_sharpe if in_sample_sharpe > 0 else 1.0

    # Return degradation
    return_degradation = (in_sample_return - out_sample_return) / in_sample_return if in_sample_return > 0 else 1.0

    # Parameter penalty (more parameters = higher risk of overfitting)
    parameter_penalty = min(n_parameters / 10, 1.0)  # Cap at 1.0

    # Combined score
    overfitting_score = (sharpe_degradation * 0.4 + return_degradation * 0.4 + parameter_penalty * 0.2)

    return max(0.0, min(1.0, overfitting_score))  # Clamp to [0, 1]
