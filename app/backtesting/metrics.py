"""
Performance Metrics Calculator
Calculates comprehensive trading performance metrics
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PerformanceMetrics:
    """
    Comprehensive performance metrics for backtesting results
    """
    # Return metrics
    initial_capital: float
    final_capital: float
    total_return: float
    total_return_pct: float
    cagr: float  # Compound Annual Growth Rate

    # Risk metrics
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    max_drawdown: float
    max_drawdown_pct: float
    avg_drawdown: float
    max_drawdown_duration_days: int

    # Trade statistics
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    loss_rate: float

    # Profit/Loss metrics
    avg_win: float
    avg_loss: float
    avg_win_pct: float
    avg_loss_pct: float
    largest_win: float
    largest_loss: float
    largest_win_pct: float
    largest_loss_pct: float

    # Risk/Reward metrics
    profit_factor: float  # Gross profit / Gross loss
    expectancy: float  # Average $ expected per trade
    expectancy_pct: float  # Average % expected per trade

    # Consistency metrics
    avg_trade_duration_days: float
    avg_bars_in_trade: float
    max_consecutive_wins: int
    max_consecutive_losses: int

    # R-Multiple statistics
    avg_r_multiple: float
    median_r_multiple: float

    # Time-based metrics
    start_date: datetime
    end_date: datetime
    total_days: int
    trading_days: int

    # Volatility metrics
    daily_volatility: float
    annual_volatility: float
    downside_deviation: float

    # Additional metrics
    recovery_factor: float  # Net profit / Max drawdown
    ulcer_index: float  # Measure of downside volatility

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary"""
        return {
            "returns": {
                "initial_capital": self.initial_capital,
                "final_capital": self.final_capital,
                "total_return": self.total_return,
                "total_return_pct": self.total_return_pct,
                "cagr": self.cagr,
            },
            "risk": {
                "sharpe_ratio": self.sharpe_ratio,
                "sortino_ratio": self.sortino_ratio,
                "calmar_ratio": self.calmar_ratio,
                "max_drawdown": self.max_drawdown,
                "max_drawdown_pct": self.max_drawdown_pct,
                "avg_drawdown": self.avg_drawdown,
                "max_drawdown_duration_days": self.max_drawdown_duration_days,
                "daily_volatility": self.daily_volatility,
                "annual_volatility": self.annual_volatility,
            },
            "trades": {
                "total_trades": self.total_trades,
                "winning_trades": self.winning_trades,
                "losing_trades": self.losing_trades,
                "win_rate": self.win_rate,
                "loss_rate": self.loss_rate,
                "avg_trade_duration_days": self.avg_trade_duration_days,
            },
            "profit_loss": {
                "avg_win": self.avg_win,
                "avg_loss": self.avg_loss,
                "avg_win_pct": self.avg_win_pct,
                "avg_loss_pct": self.avg_loss_pct,
                "largest_win": self.largest_win,
                "largest_loss": self.largest_loss,
                "profit_factor": self.profit_factor,
                "expectancy": self.expectancy,
                "expectancy_pct": self.expectancy_pct,
            },
            "consistency": {
                "max_consecutive_wins": self.max_consecutive_wins,
                "max_consecutive_losses": self.max_consecutive_losses,
                "avg_r_multiple": self.avg_r_multiple,
            }
        }


class MetricsCalculator:
    """
    Calculates performance metrics from equity curve and trade history
    """

    @staticmethod
    def calculate_all_metrics(
        equity_curve: pd.Series,
        trades: List[Dict[str, Any]],
        initial_capital: float,
        risk_free_rate: float = 0.02  # 2% annual risk-free rate
    ) -> PerformanceMetrics:
        """
        Calculate comprehensive performance metrics

        Args:
            equity_curve: Time series of portfolio values
            trades: List of trade dictionaries
            initial_capital: Starting capital
            risk_free_rate: Annual risk-free rate for Sharpe calculation

        Returns:
            PerformanceMetrics object with all calculated metrics
        """
        if len(equity_curve) == 0:
            return MetricsCalculator._empty_metrics(initial_capital)

        final_capital = equity_curve.iloc[-1]

        # Return metrics
        total_return = final_capital - initial_capital
        total_return_pct = (total_return / initial_capital) * 100

        # Calculate CAGR
        start_date = equity_curve.index[0]
        end_date = equity_curve.index[-1]
        total_days = (end_date - start_date).days
        years = total_days / 365.25
        cagr = ((final_capital / initial_capital) ** (1 / years) - 1) * 100 if years > 0 else 0

        # Calculate returns for volatility metrics
        returns = equity_curve.pct_change().dropna()
        daily_volatility = returns.std() if len(returns) > 1 else 0
        annual_volatility = daily_volatility * np.sqrt(252)  # Assuming 252 trading days

        # Sharpe Ratio
        daily_rf = risk_free_rate / 252
        excess_returns = returns - daily_rf
        sharpe_ratio = (excess_returns.mean() / excess_returns.std() * np.sqrt(252)) if excess_returns.std() > 0 else 0

        # Sortino Ratio (using downside deviation)
        downside_returns = returns[returns < 0]
        downside_deviation = downside_returns.std() if len(downside_returns) > 1 else 0
        sortino_ratio = (excess_returns.mean() / downside_deviation * np.sqrt(252)) if downside_deviation > 0 else 0

        # Drawdown metrics
        dd_metrics = MetricsCalculator._calculate_drawdown_metrics(equity_curve)

        # Calmar Ratio
        calmar_ratio = (cagr / abs(dd_metrics["max_drawdown_pct"])) if dd_metrics["max_drawdown_pct"] != 0 else 0

        # Trade statistics
        trade_metrics = MetricsCalculator._calculate_trade_metrics(trades)

        # Recovery factor
        recovery_factor = total_return / abs(dd_metrics["max_drawdown"]) if dd_metrics["max_drawdown"] != 0 else 0

        # Ulcer Index (measure of downside volatility)
        ulcer_index = MetricsCalculator._calculate_ulcer_index(equity_curve)

        return PerformanceMetrics(
            initial_capital=initial_capital,
            final_capital=final_capital,
            total_return=total_return,
            total_return_pct=total_return_pct,
            cagr=cagr,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            max_drawdown=dd_metrics["max_drawdown"],
            max_drawdown_pct=dd_metrics["max_drawdown_pct"],
            avg_drawdown=dd_metrics["avg_drawdown"],
            max_drawdown_duration_days=dd_metrics["max_drawdown_duration"],
            total_trades=trade_metrics["total_trades"],
            winning_trades=trade_metrics["winning_trades"],
            losing_trades=trade_metrics["losing_trades"],
            win_rate=trade_metrics["win_rate"],
            loss_rate=trade_metrics["loss_rate"],
            avg_win=trade_metrics["avg_win"],
            avg_loss=trade_metrics["avg_loss"],
            avg_win_pct=trade_metrics["avg_win_pct"],
            avg_loss_pct=trade_metrics["avg_loss_pct"],
            largest_win=trade_metrics["largest_win"],
            largest_loss=trade_metrics["largest_loss"],
            largest_win_pct=trade_metrics["largest_win_pct"],
            largest_loss_pct=trade_metrics["largest_loss_pct"],
            profit_factor=trade_metrics["profit_factor"],
            expectancy=trade_metrics["expectancy"],
            expectancy_pct=trade_metrics["expectancy_pct"],
            avg_trade_duration_days=trade_metrics["avg_duration"],
            avg_bars_in_trade=trade_metrics["avg_bars"],
            max_consecutive_wins=trade_metrics["max_consecutive_wins"],
            max_consecutive_losses=trade_metrics["max_consecutive_losses"],
            avg_r_multiple=trade_metrics["avg_r_multiple"],
            median_r_multiple=trade_metrics["median_r_multiple"],
            start_date=start_date,
            end_date=end_date,
            total_days=total_days,
            trading_days=len(equity_curve),
            daily_volatility=daily_volatility,
            annual_volatility=annual_volatility,
            downside_deviation=downside_deviation,
            recovery_factor=recovery_factor,
            ulcer_index=ulcer_index
        )

    @staticmethod
    def _calculate_drawdown_metrics(equity_curve: pd.Series) -> Dict[str, float]:
        """Calculate drawdown-related metrics"""
        # Calculate running maximum
        running_max = equity_curve.expanding().max()

        # Calculate drawdown
        drawdown = equity_curve - running_max
        drawdown_pct = (drawdown / running_max) * 100

        # Maximum drawdown
        max_drawdown = drawdown.min()
        max_drawdown_pct = drawdown_pct.min()

        # Average drawdown (only count periods in drawdown)
        dd_periods = drawdown[drawdown < 0]
        avg_drawdown = dd_periods.mean() if len(dd_periods) > 0 else 0

        # Maximum drawdown duration
        in_drawdown = drawdown < 0
        drawdown_periods = []
        current_period = 0

        for is_dd in in_drawdown:
            if is_dd:
                current_period += 1
            else:
                if current_period > 0:
                    drawdown_periods.append(current_period)
                current_period = 0

        max_drawdown_duration = max(drawdown_periods) if drawdown_periods else 0

        return {
            "max_drawdown": max_drawdown,
            "max_drawdown_pct": max_drawdown_pct,
            "avg_drawdown": avg_drawdown,
            "max_drawdown_duration": max_drawdown_duration
        }

    @staticmethod
    def _calculate_trade_metrics(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate trade-based performance metrics"""
        if not trades:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0,
                "loss_rate": 0,
                "avg_win": 0,
                "avg_loss": 0,
                "avg_win_pct": 0,
                "avg_loss_pct": 0,
                "largest_win": 0,
                "largest_loss": 0,
                "largest_win_pct": 0,
                "largest_loss_pct": 0,
                "profit_factor": 0,
                "expectancy": 0,
                "expectancy_pct": 0,
                "avg_duration": 0,
                "avg_bars": 0,
                "max_consecutive_wins": 0,
                "max_consecutive_losses": 0,
                "avg_r_multiple": 0,
                "median_r_multiple": 0
            }

        # Filter closed trades
        closed_trades = [t for t in trades if t.get("status") == "closed"]
        total_trades = len(closed_trades)

        if total_trades == 0:
            return MetricsCalculator._empty_trade_metrics()

        # Separate wins and losses
        wins = [t for t in closed_trades if t.get("profit_loss", 0) > 0]
        losses = [t for t in closed_trades if t.get("profit_loss", 0) <= 0]

        winning_trades = len(wins)
        losing_trades = len(losses)

        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        loss_rate = (losing_trades / total_trades) * 100 if total_trades > 0 else 0

        # Win/Loss amounts
        win_amounts = [t["profit_loss"] for t in wins] if wins else [0]
        loss_amounts = [abs(t["profit_loss"]) for t in losses] if losses else [0]

        avg_win = np.mean(win_amounts)
        avg_loss = np.mean(loss_amounts)
        largest_win = max(win_amounts)
        largest_loss = max(loss_amounts)

        # Win/Loss percentages
        win_pcts = [t.get("profit_loss_pct", 0) for t in wins] if wins else [0]
        loss_pcts = [abs(t.get("profit_loss_pct", 0)) for t in losses] if losses else [0]

        avg_win_pct = np.mean(win_pcts)
        avg_loss_pct = np.mean(loss_pcts)
        largest_win_pct = max(win_pcts)
        largest_loss_pct = max(loss_pcts)

        # Profit factor
        total_wins = sum(win_amounts)
        total_losses = sum(loss_amounts)
        profit_factor = total_wins / total_losses if total_losses > 0 else 0

        # Expectancy
        expectancy = (avg_win * winning_trades - avg_loss * losing_trades) / total_trades if total_trades > 0 else 0
        expectancy_pct = (avg_win_pct * win_rate / 100 - avg_loss_pct * loss_rate / 100) if total_trades > 0 else 0

        # Trade duration
        durations = [t.get("duration_days", 0) for t in closed_trades if t.get("duration_days")]
        avg_duration = np.mean(durations) if durations else 0

        # Bars in trade (if available)
        bars = [t.get("bars_in_trade", 0) for t in closed_trades if t.get("bars_in_trade")]
        avg_bars = np.mean(bars) if bars else 0

        # Consecutive wins/losses
        max_consecutive_wins = 0
        max_consecutive_losses = 0
        current_wins = 0
        current_losses = 0

        for trade in closed_trades:
            if trade.get("profit_loss", 0) > 0:
                current_wins += 1
                current_losses = 0
                max_consecutive_wins = max(max_consecutive_wins, current_wins)
            else:
                current_losses += 1
                current_wins = 0
                max_consecutive_losses = max(max_consecutive_losses, current_losses)

        # R-multiples
        r_multiples = [t.get("r_multiple", 0) for t in closed_trades if t.get("r_multiple") is not None]
        avg_r_multiple = np.mean(r_multiples) if r_multiples else 0
        median_r_multiple = np.median(r_multiples) if r_multiples else 0

        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate,
            "loss_rate": loss_rate,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "avg_win_pct": avg_win_pct,
            "avg_loss_pct": avg_loss_pct,
            "largest_win": largest_win,
            "largest_loss": largest_loss,
            "largest_win_pct": largest_win_pct,
            "largest_loss_pct": largest_loss_pct,
            "profit_factor": profit_factor,
            "expectancy": expectancy,
            "expectancy_pct": expectancy_pct,
            "avg_duration": avg_duration,
            "avg_bars": avg_bars,
            "max_consecutive_wins": max_consecutive_wins,
            "max_consecutive_losses": max_consecutive_losses,
            "avg_r_multiple": avg_r_multiple,
            "median_r_multiple": median_r_multiple
        }

    @staticmethod
    def _calculate_ulcer_index(equity_curve: pd.Series) -> float:
        """
        Calculate Ulcer Index - a measure of downside volatility
        Lower is better
        """
        running_max = equity_curve.expanding().max()
        drawdown_pct = ((equity_curve - running_max) / running_max) * 100
        squared_drawdowns = drawdown_pct ** 2
        ulcer = np.sqrt(squared_drawdowns.mean())
        return ulcer

    @staticmethod
    def _empty_metrics(initial_capital: float) -> PerformanceMetrics:
        """Return empty metrics when no data available"""
        return PerformanceMetrics(
            initial_capital=initial_capital,
            final_capital=initial_capital,
            total_return=0,
            total_return_pct=0,
            cagr=0,
            sharpe_ratio=0,
            sortino_ratio=0,
            calmar_ratio=0,
            max_drawdown=0,
            max_drawdown_pct=0,
            avg_drawdown=0,
            max_drawdown_duration_days=0,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0,
            loss_rate=0,
            avg_win=0,
            avg_loss=0,
            avg_win_pct=0,
            avg_loss_pct=0,
            largest_win=0,
            largest_loss=0,
            largest_win_pct=0,
            largest_loss_pct=0,
            profit_factor=0,
            expectancy=0,
            expectancy_pct=0,
            avg_trade_duration_days=0,
            avg_bars_in_trade=0,
            max_consecutive_wins=0,
            max_consecutive_losses=0,
            avg_r_multiple=0,
            median_r_multiple=0,
            start_date=datetime.now(),
            end_date=datetime.now(),
            total_days=0,
            trading_days=0,
            daily_volatility=0,
            annual_volatility=0,
            downside_deviation=0,
            recovery_factor=0,
            ulcer_index=0
        )

    @staticmethod
    def _empty_trade_metrics() -> Dict[str, Any]:
        """Return empty trade metrics"""
        return {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0,
            "loss_rate": 0,
            "avg_win": 0,
            "avg_loss": 0,
            "avg_win_pct": 0,
            "avg_loss_pct": 0,
            "largest_win": 0,
            "largest_loss": 0,
            "largest_win_pct": 0,
            "largest_loss_pct": 0,
            "profit_factor": 0,
            "expectancy": 0,
            "expectancy_pct": 0,
            "avg_duration": 0,
            "avg_bars": 0,
            "max_consecutive_wins": 0,
            "max_consecutive_losses": 0,
            "avg_r_multiple": 0,
            "median_r_multiple": 0
        }
