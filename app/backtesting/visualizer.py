"""
Backtest Visualization Tools
Generate equity curves, trade distributions, heatmaps, and reports
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class BacktestVisualizer:
    """
    Generate visualizations and reports for backtest results

    Note: Returns data structures that can be rendered by frontend charting libraries
    (Chart.js, Plotly, etc.) rather than generating images directly
    """

    @staticmethod
    def create_equity_curve_data(
        equity_curve: pd.Series,
        benchmark: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """
        Create equity curve chart data

        Args:
            equity_curve: Time series of portfolio values
            benchmark: Optional benchmark time series (e.g., SPY)

        Returns:
            Dictionary with chart data for frontend rendering
        """
        data = {
            "type": "line",
            "title": "Equity Curve",
            "x_label": "Date",
            "y_label": "Portfolio Value ($)",
            "datasets": [
                {
                    "label": "Strategy",
                    "data": [
                        {"x": date.isoformat(), "y": value}
                        for date, value in equity_curve.items()
                    ],
                    "borderColor": "rgb(75, 192, 192)",
                    "backgroundColor": "rgba(75, 192, 192, 0.1)",
                }
            ]
        }

        if benchmark is not None:
            # Normalize benchmark to same starting capital
            normalized_benchmark = benchmark / benchmark.iloc[0] * equity_curve.iloc[0]

            data["datasets"].append({
                "label": "Benchmark",
                "data": [
                    {"x": date.isoformat(), "y": value}
                    for date, value in normalized_benchmark.items()
                ],
                "borderColor": "rgb(255, 99, 132)",
                "backgroundColor": "rgba(255, 99, 132, 0.1)",
            })

        return data

    @staticmethod
    def create_drawdown_chart_data(equity_curve: pd.Series) -> Dict[str, Any]:
        """
        Create drawdown chart data

        Args:
            equity_curve: Time series of portfolio values

        Returns:
            Dictionary with drawdown chart data
        """
        # Calculate drawdown
        running_max = equity_curve.expanding().max()
        drawdown = equity_curve - running_max
        drawdown_pct = (drawdown / running_max) * 100

        return {
            "type": "area",
            "title": "Drawdown Over Time",
            "x_label": "Date",
            "y_label": "Drawdown (%)",
            "datasets": [
                {
                    "label": "Drawdown",
                    "data": [
                        {"x": date.isoformat(), "y": dd}
                        for date, dd in drawdown_pct.items()
                    ],
                    "borderColor": "rgb(255, 99, 132)",
                    "backgroundColor": "rgba(255, 99, 132, 0.3)",
                    "fill": "origin"
                }
            ]
        }

    @staticmethod
    def create_trade_distribution_data(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create trade P&L distribution histogram

        Args:
            trades: List of trade dictionaries

        Returns:
            Dictionary with histogram data
        """
        if not trades:
            return {"type": "histogram", "title": "Trade Distribution", "datasets": []}

        # Extract P&L percentages
        pnl_pcts = [t.get("profit_loss_pct", 0) for t in trades if "profit_loss_pct" in t]

        # Create bins
        bins = np.histogram_bin_edges(pnl_pcts, bins=20)
        hist, _ = np.histogram(pnl_pcts, bins=bins)

        return {
            "type": "histogram",
            "title": "Trade P&L Distribution",
            "x_label": "Profit/Loss (%)",
            "y_label": "Number of Trades",
            "bins": bins.tolist(),
            "counts": hist.tolist(),
            "statistics": {
                "mean": np.mean(pnl_pcts),
                "median": np.median(pnl_pcts),
                "std": np.std(pnl_pcts),
                "min": min(pnl_pcts),
                "max": max(pnl_pcts),
            }
        }

    @staticmethod
    def create_win_loss_heatmap_data(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create win/loss heatmap by day of week and hour (if intraday data available)

        Args:
            trades: List of trade dictionaries

        Returns:
            Dictionary with heatmap data
        """
        if not trades:
            return {"type": "heatmap", "title": "Win/Loss Heatmap", "data": []}

        # Extract trade data
        trade_data = []
        for t in trades:
            if "exit_date" not in t or "profit_loss_pct" not in t:
                continue

            exit_date = t["exit_date"]
            if isinstance(exit_date, str):
                exit_date = datetime.fromisoformat(exit_date)

            day_of_week = exit_date.strftime("%A")
            week_num = exit_date.isocalendar()[1]
            profit_loss_pct = t["profit_loss_pct"]

            trade_data.append({
                "day": day_of_week,
                "week": week_num,
                "pnl": profit_loss_pct,
                "is_win": profit_loss_pct > 0
            })

        # Calculate win rate by day of week
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        win_rates = {}

        for day in days:
            day_trades = [t for t in trade_data if t["day"] == day]
            if day_trades:
                wins = sum(1 for t in day_trades if t["is_win"])
                win_rates[day] = (wins / len(day_trades)) * 100
            else:
                win_rates[day] = 0

        return {
            "type": "heatmap",
            "title": "Win Rate by Day of Week",
            "x_label": "Day of Week",
            "y_label": "Win Rate (%)",
            "data": [
                {"day": day, "win_rate": win_rates[day]}
                for day in days
            ]
        }

    @staticmethod
    def create_monthly_returns_heatmap(equity_curve: pd.Series) -> Dict[str, Any]:
        """
        Create monthly returns heatmap

        Args:
            equity_curve: Time series of portfolio values

        Returns:
            Dictionary with monthly returns heatmap data
        """
        if len(equity_curve) == 0:
            return {"type": "heatmap", "title": "Monthly Returns", "data": []}

        # Calculate monthly returns
        monthly_equity = equity_curve.resample('M').last()
        monthly_returns = monthly_equity.pct_change() * 100

        # Organize by year and month
        heatmap_data = []
        for date, ret in monthly_returns.items():
            if pd.isna(ret):
                continue

            heatmap_data.append({
                "year": date.year,
                "month": date.strftime("%b"),
                "month_num": date.month,
                "return": ret
            })

        return {
            "type": "heatmap",
            "title": "Monthly Returns (%)",
            "x_label": "Month",
            "y_label": "Year",
            "data": heatmap_data
        }

    @staticmethod
    def create_risk_adjusted_returns_chart(
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create scatter plot of return vs risk (Sharpe ratio visualization)

        Args:
            results: List of backtest results to compare

        Returns:
            Dictionary with scatter plot data
        """
        scatter_data = []

        for result in results:
            metrics = result.get("metrics", {})
            risk_metrics = metrics.get("risk", {})
            return_metrics = metrics.get("returns", {})

            scatter_data.append({
                "name": result.get("strategy_name", "Unknown"),
                "return": return_metrics.get("total_return_pct", 0),
                "volatility": risk_metrics.get("annual_volatility", 0),
                "sharpe": risk_metrics.get("sharpe_ratio", 0)
            })

        return {
            "type": "scatter",
            "title": "Risk vs Return",
            "x_label": "Annual Volatility (%)",
            "y_label": "Total Return (%)",
            "data": scatter_data
        }

    @staticmethod
    def create_trade_timeline_data(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create trade timeline visualization

        Args:
            trades: List of trade dictionaries

        Returns:
            Dictionary with timeline data
        """
        timeline_data = []

        for i, trade in enumerate(trades):
            if "entry_date" not in trade or "exit_date" not in trade:
                continue

            entry_date = trade["entry_date"]
            exit_date = trade["exit_date"]

            if isinstance(entry_date, str):
                entry_date = datetime.fromisoformat(entry_date)
            if isinstance(exit_date, str):
                exit_date = datetime.fromisoformat(exit_date)

            timeline_data.append({
                "trade_num": i + 1,
                "ticker": trade.get("ticker", ""),
                "entry_date": entry_date.isoformat(),
                "exit_date": exit_date.isoformat(),
                "duration_days": (exit_date - entry_date).days,
                "profit_loss": trade.get("profit_loss", 0),
                "profit_loss_pct": trade.get("profit_loss_pct", 0),
                "is_win": trade.get("profit_loss", 0) > 0
            })

        return {
            "type": "timeline",
            "title": "Trade Timeline",
            "data": timeline_data
        }

    @staticmethod
    def create_monte_carlo_distribution(mc_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Monte Carlo simulation distribution chart

        Args:
            mc_result: Monte Carlo result dictionary

        Returns:
            Dictionary with distribution chart data
        """
        all_returns = mc_result.get("all_returns_pct", [])

        if not all_returns:
            return {"type": "histogram", "title": "Monte Carlo Distribution", "datasets": []}

        # Create histogram
        bins = np.histogram_bin_edges(all_returns, bins=50)
        hist, _ = np.histogram(all_returns, bins=bins)

        original_return = mc_result.get("original_return_pct", 0)
        percentile_5 = mc_result.get("percentiles", {}).get("5th", 0)
        percentile_95 = mc_result.get("percentiles", {}).get("95th", 0)

        return {
            "type": "histogram",
            "title": "Monte Carlo Return Distribution",
            "x_label": "Return (%)",
            "y_label": "Frequency",
            "bins": bins.tolist(),
            "counts": hist.tolist(),
            "markers": {
                "original": original_return,
                "percentile_5": percentile_5,
                "percentile_95": percentile_95,
            },
            "statistics": mc_result.get("statistics", {})
        }

    @staticmethod
    def generate_summary_report(
        backtest_result: Dict[str, Any],
        monte_carlo: Optional[Dict[str, Any]] = None,
        walk_forward: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive summary report

        Args:
            backtest_result: Backtest result dictionary
            monte_carlo: Optional Monte Carlo results
            walk_forward: Optional walk-forward results

        Returns:
            Dictionary with complete summary report
        """
        metrics = backtest_result.get("metrics", {})

        report = {
            "strategy_name": backtest_result.get("strategy_name", "Unknown"),
            "ticker": backtest_result.get("ticker", ""),
            "period": {
                "start": backtest_result.get("start_date", ""),
                "end": backtest_result.get("end_date", ""),
            },
            "capital": {
                "initial": backtest_result.get("initial_capital", 0),
                "final": backtest_result.get("final_capital", 0),
                "total_return": backtest_result.get("total_return", 0),
                "total_return_pct": backtest_result.get("total_return_pct", 0),
            },
            "performance": {
                "cagr": metrics.get("returns", {}).get("cagr", 0),
                "sharpe_ratio": metrics.get("risk", {}).get("sharpe_ratio", 0),
                "sortino_ratio": metrics.get("risk", {}).get("sortino_ratio", 0),
                "calmar_ratio": metrics.get("risk", {}).get("calmar_ratio", 0),
            },
            "risk": {
                "max_drawdown": metrics.get("risk", {}).get("max_drawdown", 0),
                "max_drawdown_pct": metrics.get("risk", {}).get("max_drawdown_pct", 0),
                "volatility": metrics.get("risk", {}).get("annual_volatility", 0),
            },
            "trades": {
                "total": metrics.get("trades", {}).get("total_trades", 0),
                "winning": metrics.get("trades", {}).get("winning_trades", 0),
                "losing": metrics.get("trades", {}).get("losing_trades", 0),
                "win_rate": metrics.get("trades", {}).get("win_rate", 0),
            },
            "profit_loss": {
                "profit_factor": metrics.get("profit_loss", {}).get("profit_factor", 0),
                "expectancy": metrics.get("profit_loss", {}).get("expectancy", 0),
                "avg_win": metrics.get("profit_loss", {}).get("avg_win", 0),
                "avg_loss": metrics.get("profit_loss", {}).get("avg_loss", 0),
            }
        }

        # Add Monte Carlo analysis if available
        if monte_carlo:
            report["monte_carlo"] = {
                "num_simulations": monte_carlo.get("num_simulations", 0),
                "mean_return": monte_carlo.get("statistics", {}).get("mean_return", 0),
                "var_95": monte_carlo.get("risk", {}).get("var_95", 0),
                "prob_profit": monte_carlo.get("probabilities", {}).get("prob_profit", 0),
            }

        # Add Walk-forward analysis if available
        if walk_forward:
            report["walk_forward"] = {
                "total_windows": walk_forward.get("total_windows", 0),
                "out_of_sample_return": walk_forward.get("aggregate_results", {}).get("out_of_sample_return_pct", 0),
                "degradation": walk_forward.get("degradation", {}).get("percentage", 0),
                "out_of_sample_win_rate": walk_forward.get("consistency", {}).get("out_of_sample_win_rate", 0),
            }

        # Generate grade
        report["overall_grade"] = BacktestVisualizer._calculate_grade(report)

        return report

    @staticmethod
    def _calculate_grade(report: Dict[str, Any]) -> str:
        """Calculate overall strategy grade based on metrics"""
        score = 0

        # Return score (max 30 points)
        cagr = report.get("performance", {}).get("cagr", 0)
        if cagr > 20:
            score += 30
        elif cagr > 15:
            score += 25
        elif cagr > 10:
            score += 20
        elif cagr > 5:
            score += 10

        # Risk-adjusted return (max 25 points)
        sharpe = report.get("performance", {}).get("sharpe_ratio", 0)
        if sharpe > 2:
            score += 25
        elif sharpe > 1.5:
            score += 20
        elif sharpe > 1:
            score += 15
        elif sharpe > 0.5:
            score += 10

        # Win rate (max 20 points)
        win_rate = report.get("trades", {}).get("win_rate", 0)
        if win_rate > 60:
            score += 20
        elif win_rate > 55:
            score += 15
        elif win_rate > 50:
            score += 10

        # Max drawdown (max 15 points)
        max_dd = abs(report.get("risk", {}).get("max_drawdown_pct", 100))
        if max_dd < 10:
            score += 15
        elif max_dd < 15:
            score += 12
        elif max_dd < 20:
            score += 8
        elif max_dd < 30:
            score += 5

        # Profit factor (max 10 points)
        pf = report.get("profit_loss", {}).get("profit_factor", 0)
        if pf > 2:
            score += 10
        elif pf > 1.5:
            score += 7
        elif pf > 1:
            score += 4

        # Convert to grade
        if score >= 85:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 75:
            return "A-"
        elif score >= 70:
            return "B+"
        elif score >= 65:
            return "B"
        elif score >= 60:
            return "B-"
        elif score >= 55:
            return "C+"
        elif score >= 50:
            return "C"
        elif score >= 45:
            return "C-"
        else:
            return "D"
