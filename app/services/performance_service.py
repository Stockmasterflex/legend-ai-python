"""
Performance Analytics Service
Handles return calculations, benchmark comparisons, and performance metrics
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging
import numpy as np
import pandas as pd

from app.models import Portfolio, Position, Ticker, TradeJournal
from app.services.market_data import get_historical_data, get_current_price

logger = logging.getLogger(__name__)


class PerformanceService:
    """Service for performance analytics and benchmarking"""

    def __init__(self, db: Session):
        self.db = db

    async def calculate_returns(
        self,
        portfolio_id: int,
        period: str = "daily"
    ) -> Dict:
        """
        Calculate portfolio returns for different time periods

        Args:
            portfolio_id: Portfolio ID
            period: "daily", "weekly", or "monthly"

        Returns:
            Dictionary with return metrics
        """
        portfolio = self.db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")

        # Calculate current portfolio value
        positions = self.db.query(Position).filter(
            Position.portfolio_id == portfolio_id,
            Position.status == "open"
        ).all()

        current_value = portfolio.cash_balance
        for position in positions:
            ticker = self.db.query(Ticker).filter(Ticker.id == position.ticker_id).first()
            try:
                current_price = await get_current_price(ticker.symbol)
                current_value += current_price * position.quantity
            except:
                current_value += position.current_value or 0

        # Calculate returns based on period
        period_map = {
            "daily": 1,
            "weekly": 7,
            "monthly": 30
        }
        days = period_map.get(period, 1)

        # For now, calculate simple return from initial capital
        # In production, you'd track historical portfolio values
        total_return = current_value - portfolio.initial_capital
        total_return_pct = (total_return / portfolio.initial_capital) * 100

        # Calculate annualized return
        days_since_inception = (datetime.utcnow() - portfolio.created_at).days
        if days_since_inception > 0:
            annualized_return = (((current_value / portfolio.initial_capital) ** (365.25 / days_since_inception)) - 1) * 100
        else:
            annualized_return = 0

        return {
            "period": period,
            "current_value": current_value,
            "total_return": total_return,
            "total_return_pct": total_return_pct,
            "annualized_return_pct": annualized_return,
            "days_since_inception": days_since_inception
        }

    async def benchmark_comparison(
        self,
        portfolio_id: int,
        benchmark_symbol: str = "SPY",
        period_days: int = 30
    ) -> Dict:
        """
        Compare portfolio performance to a benchmark (default: SPY)

        Args:
            portfolio_id: Portfolio ID
            benchmark_symbol: Benchmark ticker (default SPY)
            period_days: Comparison period in days

        Returns:
            Comparison metrics
        """
        portfolio = self.db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")

        # Calculate portfolio return
        portfolio_returns = await self.calculate_returns(portfolio_id, "daily")
        portfolio_return_pct = portfolio_returns["total_return_pct"]

        # Get benchmark historical data
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=period_days)

            benchmark_data = await get_historical_data(
                benchmark_symbol,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )

            if benchmark_data and len(benchmark_data) > 0:
                df = pd.DataFrame(benchmark_data)
                first_price = df.iloc[0]['close']
                last_price = df.iloc[-1]['close']
                benchmark_return_pct = ((last_price - first_price) / first_price) * 100
            else:
                # Fallback: use simple calculation
                current_price = await get_current_price(benchmark_symbol)
                # Assume ~10% annual return for SPY
                days_calc = min(period_days, (datetime.utcnow() - portfolio.created_at).days)
                benchmark_return_pct = (0.10 * days_calc / 365.25) * 100

        except Exception as e:
            logger.warning(f"Failed to get benchmark data: {e}")
            benchmark_return_pct = 0

        # Calculate alpha (excess return over benchmark)
        alpha = portfolio_return_pct - benchmark_return_pct

        # Calculate relative performance
        outperformance = alpha > 0

        return {
            "benchmark_symbol": benchmark_symbol,
            "period_days": period_days,
            "portfolio_return_pct": portfolio_return_pct,
            "benchmark_return_pct": benchmark_return_pct,
            "alpha": alpha,
            "outperforming": outperformance,
            "relative_performance": "Outperforming" if outperformance else "Underperforming"
        }

    async def get_best_worst_performers(self, portfolio_id: int) -> Dict:
        """Get best and worst performing positions in the portfolio"""
        positions = self.db.query(Position).filter(
            Position.portfolio_id == portfolio_id,
            Position.status == "open"
        ).all()

        performers = []
        for position in positions:
            ticker = self.db.query(Ticker).filter(Ticker.id == position.ticker_id).first()
            if position.unrealized_pnl_pct is not None:
                performers.append({
                    "symbol": ticker.symbol,
                    "pnl": position.unrealized_pnl,
                    "pnl_pct": position.unrealized_pnl_pct,
                    "current_value": position.current_value,
                    "position_size_pct": position.position_size_pct
                })

        # Sort by performance
        performers_sorted = sorted(performers, key=lambda x: x["pnl_pct"], reverse=True)

        best_performers = performers_sorted[:5] if len(performers_sorted) >= 5 else performers_sorted
        worst_performers = performers_sorted[-5:][::-1] if len(performers_sorted) >= 5 else []

        return {
            "best_performers": best_performers,
            "worst_performers": worst_performers,
            "total_positions": len(performers)
        }

    async def calculate_risk_adjusted_returns(self, portfolio_id: int) -> Dict:
        """
        Calculate risk-adjusted return metrics (Sharpe, Sortino ratios)

        Note: This is a simplified version. For accurate calculations,
        you'd need historical daily portfolio values.
        """
        portfolio = self.db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")

        # Get all closed trades for volatility calculation
        closed_trades = self.db.query(TradeJournal).filter(
            TradeJournal.portfolio_id == portfolio_id,
            TradeJournal.trade_type == "exit",
            TradeJournal.profit_loss_pct.isnot(None)
        ).all()

        if len(closed_trades) < 2:
            return {
                "sharpe_ratio": None,
                "sortino_ratio": None,
                "max_drawdown_pct": None,
                "note": "Insufficient trade history for risk-adjusted metrics"
            }

        # Calculate returns from closed trades
        returns = [trade.profit_loss_pct for trade in closed_trades]
        returns_array = np.array(returns)

        # Calculate mean return and standard deviation
        mean_return = np.mean(returns_array)
        std_return = np.std(returns_array)

        # Risk-free rate (assume 4% annual, converted to per-trade)
        risk_free_rate = 0.04 / 252  # Daily risk-free rate

        # Sharpe Ratio
        if std_return > 0:
            sharpe_ratio = (mean_return - risk_free_rate) / std_return
        else:
            sharpe_ratio = 0

        # Sortino Ratio (only downside deviation)
        negative_returns = returns_array[returns_array < 0]
        if len(negative_returns) > 0:
            downside_std = np.std(negative_returns)
            if downside_std > 0:
                sortino_ratio = (mean_return - risk_free_rate) / downside_std
            else:
                sortino_ratio = 0
        else:
            sortino_ratio = sharpe_ratio

        # Calculate max drawdown from trade history
        cumulative_returns = np.cumprod(1 + returns_array / 100)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdowns = (cumulative_returns - running_max) / running_max
        max_drawdown = np.min(drawdowns) * 100 if len(drawdowns) > 0 else 0

        return {
            "sharpe_ratio": round(sharpe_ratio, 2),
            "sortino_ratio": round(sortino_ratio, 2),
            "max_drawdown_pct": round(max_drawdown, 2),
            "mean_return_pct": round(mean_return, 2),
            "volatility_pct": round(std_return, 2),
            "num_trades": len(closed_trades)
        }

    async def get_performance_summary(self, portfolio_id: int) -> Dict:
        """Get comprehensive performance summary"""
        # Get all metrics
        returns = await self.calculate_returns(portfolio_id, "daily")
        benchmark = await self.benchmark_comparison(portfolio_id, "SPY", 30)
        performers = await self.get_best_worst_performers(portfolio_id)
        risk_adjusted = await self.calculate_risk_adjusted_returns(portfolio_id)

        # Get trade statistics
        trades = self.db.query(TradeJournal).filter(
            TradeJournal.portfolio_id == portfolio_id,
            TradeJournal.trade_type == "exit"
        ).all()

        winning_trades = [t for t in trades if t.profit_loss and t.profit_loss > 0]
        losing_trades = [t for t in trades if t.profit_loss and t.profit_loss < 0]

        win_rate = (len(winning_trades) / len(trades) * 100) if len(trades) > 0 else 0
        avg_win = np.mean([t.profit_loss for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t.profit_loss for t in losing_trades]) if losing_trades else 0
        profit_factor = abs(sum([t.profit_loss for t in winning_trades]) / sum([t.profit_loss for t in losing_trades])) if losing_trades and sum([t.profit_loss for t in losing_trades]) != 0 else 0

        return {
            "returns": returns,
            "benchmark_comparison": benchmark,
            "best_performers": performers["best_performers"][:3],
            "worst_performers": performers["worst_performers"][:3],
            "risk_adjusted_metrics": risk_adjusted,
            "trade_statistics": {
                "total_trades": len(trades),
                "winning_trades": len(winning_trades),
                "losing_trades": len(losing_trades),
                "win_rate_pct": round(win_rate, 2),
                "avg_win": round(avg_win, 2) if avg_win else 0,
                "avg_loss": round(avg_loss, 2) if avg_loss else 0,
                "profit_factor": round(profit_factor, 2) if profit_factor else 0
            }
        }
