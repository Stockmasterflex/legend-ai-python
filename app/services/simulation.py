"""
Simulation trading engine for paper trading and strategy testing
Practice trading without risk and track hypothetical P&L
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
import numpy as np
import pandas as pd

from app.models import SimulationAccount, SimulationTrade, Ticker
from app.services.database import DatabaseService
from app.services.market_data import MarketDataService


class SimulationEngine:
    """
    Paper trading simulation engine with full P&L tracking and statistics
    """

    def __init__(self, db_service: DatabaseService, market_data_service: MarketDataService):
        self.db = db_service
        self.market_data = market_data_service

    async def create_account(
        self,
        user_id: str,
        name: str,
        initial_balance: float = 100000.0
    ) -> Dict[str, Any]:
        """
        Create a new simulation trading account

        Args:
            user_id: User identifier
            name: Account name
            initial_balance: Starting cash balance

        Returns:
            Account details
        """
        with self.db.get_db() as session:
            account = SimulationAccount(
                user_id=user_id,
                name=name,
                initial_balance=initial_balance,
                current_balance=initial_balance,
                cash_balance=initial_balance
            )
            session.add(account)
            session.commit()
            session.refresh(account)

            return self._account_to_dict(account)

    async def get_account(self, account_id: int) -> Dict[str, Any]:
        """Get account details with current positions"""
        with self.db.get_db() as session:
            account = session.get(SimulationAccount, account_id)
            if not account:
                raise ValueError(f"Account {account_id} not found")

            # Get open positions
            open_trades = session.query(SimulationTrade).filter(
                SimulationTrade.account_id == account_id,
                SimulationTrade.status == "open"
            ).all()

            # Calculate current values for open positions
            positions = []
            total_position_value = 0.0

            for trade in open_trades:
                ticker = session.get(Ticker, trade.ticker_id)
                if ticker:
                    # For simulation, we'd need current price - simplified here
                    current_value = trade.entry_price * trade.position_size
                    unrealized_pnl = (trade.entry_price - trade.entry_price) * trade.position_size

                    positions.append({
                        "trade_id": trade.id,
                        "ticker": ticker.symbol,
                        "entry_date": trade.entry_date.isoformat(),
                        "entry_price": trade.entry_price,
                        "position_size": trade.position_size,
                        "current_value": current_value,
                        "unrealized_pnl": unrealized_pnl,
                        "stop_loss": trade.stop_loss,
                        "target_price": trade.target_price
                    })
                    total_position_value += current_value

            account_data = self._account_to_dict(account)
            account_data['positions'] = positions
            account_data['total_position_value'] = total_position_value
            account_data['buying_power'] = account.cash_balance

            return account_data

    async def enter_trade(
        self,
        account_id: int,
        ticker_symbol: str,
        entry_price: float,
        position_size: int,
        trade_type: str = "long",
        stop_loss: Optional[float] = None,
        target_price: Optional[float] = None,
        entry_date: Optional[datetime] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Enter a new simulated trade

        Args:
            account_id: Simulation account ID
            ticker_symbol: Stock ticker
            entry_price: Entry price
            position_size: Number of shares
            trade_type: "long" or "short"
            stop_loss: Optional stop loss price
            target_price: Optional target price
            entry_date: Optional entry date (for historical simulation)
            notes: Optional trade notes

        Returns:
            Trade details
        """
        if entry_date is None:
            entry_date = datetime.utcnow()

        with self.db.get_db() as session:
            # Validate account
            account = session.get(SimulationAccount, account_id)
            if not account:
                raise ValueError(f"Account {account_id} not found")

            if account.status != "active":
                raise ValueError(f"Account is {account.status}, not active")

            # Calculate trade cost
            trade_cost = entry_price * position_size

            # Check buying power
            if trade_cost > account.cash_balance:
                raise ValueError(
                    f"Insufficient buying power. Required: ${trade_cost:,.2f}, "
                    f"Available: ${account.cash_balance:,.2f}"
                )

            # Get or create ticker
            ticker = session.query(Ticker).filter(Ticker.symbol == ticker_symbol.upper()).first()
            if not ticker:
                ticker = Ticker(symbol=ticker_symbol.upper(), name=ticker_symbol.upper())
                session.add(ticker)
                session.flush()

            # Create trade
            trade = SimulationTrade(
                account_id=account_id,
                ticker_id=ticker.id,
                trade_type=trade_type,
                entry_date=entry_date,
                entry_price=entry_price,
                position_size=position_size,
                stop_loss=stop_loss,
                target_price=target_price,
                notes=notes,
                status="open"
            )
            session.add(trade)

            # Update account cash
            account.cash_balance -= trade_cost
            account.total_trades += 1

            session.commit()
            session.refresh(trade)

            return {
                "trade_id": trade.id,
                "account_id": account_id,
                "ticker": ticker_symbol,
                "trade_type": trade_type,
                "entry_date": trade.entry_date.isoformat(),
                "entry_price": trade.entry_price,
                "position_size": trade.position_size,
                "stop_loss": trade.stop_loss,
                "target_price": trade.target_price,
                "status": "open",
                "cost": trade_cost
            }

    async def exit_trade(
        self,
        trade_id: int,
        exit_price: float,
        exit_date: Optional[datetime] = None,
        exit_reason: str = "manual"
    ) -> Dict[str, Any]:
        """
        Exit a simulated trade

        Args:
            trade_id: Trade ID
            exit_price: Exit price
            exit_date: Optional exit date (for historical simulation)
            exit_reason: Reason for exit ("target", "stop", "manual")

        Returns:
            Updated trade with P&L
        """
        if exit_date is None:
            exit_date = datetime.utcnow()

        with self.db.get_db() as session:
            trade = session.get(SimulationTrade, trade_id)
            if not trade:
                raise ValueError(f"Trade {trade_id} not found")

            if trade.status != "open":
                raise ValueError(f"Trade is already {trade.status}")

            account = session.get(SimulationAccount, trade.account_id)

            # Calculate P&L
            if trade.trade_type == "long":
                pnl = (exit_price - trade.entry_price) * trade.position_size
            else:  # short
                pnl = (trade.entry_price - exit_price) * trade.position_size

            pnl_pct = (pnl / (trade.entry_price * trade.position_size)) * 100

            # Calculate R multiple
            r_multiple = None
            if trade.stop_loss:
                risk = abs(trade.entry_price - trade.stop_loss) * trade.position_size
                if risk > 0:
                    r_multiple = pnl / risk

            # Update trade
            trade.exit_date = exit_date
            trade.exit_price = exit_price
            trade.exit_reason = exit_reason
            trade.pnl = pnl
            trade.pnl_pct = pnl_pct
            trade.r_multiple = r_multiple
            trade.status = "closed"

            # Update account
            proceeds = exit_price * trade.position_size
            account.cash_balance += proceeds
            account.total_pnl += pnl
            account.total_pnl_pct = ((account.initial_balance + account.total_pnl) / account.initial_balance - 1) * 100

            if pnl > 0:
                account.winning_trades += 1
            else:
                account.losing_trades += 1

            if account.total_trades > 0:
                account.win_rate = (account.winning_trades / account.total_trades) * 100

            # Update current balance
            account.current_balance = account.cash_balance + self._calculate_open_positions_value(session, account.id)

            # Update max drawdown
            drawdown = ((account.current_balance - account.initial_balance) / account.initial_balance) * 100
            if drawdown < account.max_drawdown:
                account.max_drawdown = drawdown

            session.commit()
            session.refresh(trade)

            ticker = session.get(Ticker, trade.ticker_id)

            return {
                "trade_id": trade.id,
                "ticker": ticker.symbol if ticker else "UNKNOWN",
                "trade_type": trade.trade_type,
                "entry_date": trade.entry_date.isoformat(),
                "entry_price": trade.entry_price,
                "exit_date": trade.exit_date.isoformat(),
                "exit_price": trade.exit_price,
                "exit_reason": trade.exit_reason,
                "position_size": trade.position_size,
                "pnl": trade.pnl,
                "pnl_pct": trade.pnl_pct,
                "r_multiple": trade.r_multiple,
                "status": "closed"
            }

    def _calculate_open_positions_value(self, session: Session, account_id: int) -> float:
        """Calculate total value of open positions (simplified - uses entry prices)"""
        open_trades = session.query(SimulationTrade).filter(
            SimulationTrade.account_id == account_id,
            SimulationTrade.status == "open"
        ).all()

        total_value = sum(trade.entry_price * trade.position_size for trade in open_trades)
        return total_value

    async def get_trade_history(
        self,
        account_id: int,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get trade history for an account"""
        with self.db.get_db() as session:
            query = session.query(SimulationTrade).filter(
                SimulationTrade.account_id == account_id
            )

            if status:
                query = query.filter(SimulationTrade.status == status)

            trades = query.order_by(SimulationTrade.entry_date.desc()).limit(limit).all()

            result = []
            for trade in trades:
                ticker = session.get(Ticker, trade.ticker_id)
                result.append({
                    "trade_id": trade.id,
                    "ticker": ticker.symbol if ticker else "UNKNOWN",
                    "trade_type": trade.trade_type,
                    "entry_date": trade.entry_date.isoformat(),
                    "entry_price": trade.entry_price,
                    "exit_date": trade.exit_date.isoformat() if trade.exit_date else None,
                    "exit_price": trade.exit_price,
                    "position_size": trade.position_size,
                    "pnl": trade.pnl,
                    "pnl_pct": trade.pnl_pct,
                    "r_multiple": trade.r_multiple,
                    "status": trade.status,
                    "notes": trade.notes
                })

            return result

    async def get_statistics(self, account_id: int) -> Dict[str, Any]:
        """
        Get comprehensive trading statistics for an account

        Returns:
            Detailed performance metrics
        """
        with self.db.get_db() as session:
            account = session.get(SimulationAccount, account_id)
            if not account:
                raise ValueError(f"Account {account_id} not found")

            # Get all closed trades
            closed_trades = session.query(SimulationTrade).filter(
                SimulationTrade.account_id == account_id,
                SimulationTrade.status == "closed"
            ).all()

            if not closed_trades:
                return {
                    "account_id": account_id,
                    "total_trades": 0,
                    "message": "No closed trades yet"
                }

            # Calculate statistics
            winning_trades = [t for t in closed_trades if t.pnl > 0]
            losing_trades = [t for t in closed_trades if t.pnl <= 0]

            total_pnl = sum(t.pnl for t in closed_trades)
            avg_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
            avg_loss = np.mean([t.pnl for t in losing_trades]) if losing_trades else 0

            profit_factor = abs(sum(t.pnl for t in winning_trades) / sum(t.pnl for t in losing_trades)) if losing_trades and sum(t.pnl for t in losing_trades) != 0 else float('inf')

            # R multiples
            r_multiples = [t.r_multiple for t in closed_trades if t.r_multiple is not None]
            avg_r = np.mean(r_multiples) if r_multiples else None

            # Consecutive streaks
            max_win_streak = self._calculate_max_streak(closed_trades, True)
            max_loss_streak = self._calculate_max_streak(closed_trades, False)

            # Expectancy
            win_rate = len(winning_trades) / len(closed_trades) if closed_trades else 0
            expectancy = (win_rate * avg_win) - ((1 - win_rate) * abs(avg_loss))

            return {
                "account_id": account_id,
                "account_name": account.name,
                "initial_balance": account.initial_balance,
                "current_balance": account.current_balance,
                "cash_balance": account.cash_balance,
                "total_pnl": account.total_pnl,
                "total_pnl_pct": account.total_pnl_pct,
                "total_trades": len(closed_trades),
                "winning_trades": len(winning_trades),
                "losing_trades": len(losing_trades),
                "win_rate": account.win_rate,
                "avg_win": avg_win,
                "avg_loss": avg_loss,
                "largest_win": max(t.pnl for t in closed_trades),
                "largest_loss": min(t.pnl for t in closed_trades),
                "profit_factor": profit_factor,
                "avg_r_multiple": avg_r,
                "expectancy": expectancy,
                "max_win_streak": max_win_streak,
                "max_loss_streak": max_loss_streak,
                "max_drawdown": account.max_drawdown,
                "sharpe_ratio": account.sharpe_ratio
            }

    def _calculate_max_streak(self, trades: List[SimulationTrade], winning: bool) -> int:
        """Calculate maximum consecutive winning or losing streak"""
        max_streak = 0
        current_streak = 0

        for trade in trades:
            if (winning and trade.pnl > 0) or (not winning and trade.pnl <= 0):
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        return max_streak

    async def calculate_equity_curve(self, account_id: int) -> Dict[str, Any]:
        """
        Calculate equity curve over time

        Returns:
            Equity progression data
        """
        with self.db.get_db() as session:
            account = session.get(SimulationAccount, account_id)
            if not account:
                raise ValueError(f"Account {account_id} not found")

            # Get all trades in chronological order
            trades = session.query(SimulationTrade).filter(
                SimulationTrade.account_id == account_id,
                SimulationTrade.status == "closed"
            ).order_by(SimulationTrade.exit_date).all()

            if not trades:
                return {
                    "account_id": account_id,
                    "equity_curve": [],
                    "message": "No closed trades yet"
                }

            # Build equity curve
            equity = account.initial_balance
            equity_data = [{
                "date": account.created_at.isoformat(),
                "equity": equity,
                "trade_number": 0
            }]

            for idx, trade in enumerate(trades, 1):
                equity += trade.pnl
                equity_data.append({
                    "date": trade.exit_date.isoformat() if trade.exit_date else None,
                    "equity": equity,
                    "trade_number": idx,
                    "pnl": trade.pnl,
                    "ticker": session.get(Ticker, trade.ticker_id).symbol
                })

            # Calculate drawdown curve
            peak = account.initial_balance
            drawdown_data = []

            for point in equity_data:
                if point['equity'] > peak:
                    peak = point['equity']
                drawdown = ((point['equity'] - peak) / peak) * 100
                drawdown_data.append({
                    "date": point['date'],
                    "drawdown": drawdown
                })

            return {
                "account_id": account_id,
                "equity_curve": equity_data,
                "drawdown_curve": drawdown_data,
                "final_equity": equity,
                "peak_equity": peak
            }

    async def list_accounts(self, user_id: str) -> List[Dict[str, Any]]:
        """List all simulation accounts for a user"""
        with self.db.get_db() as session:
            accounts = session.query(SimulationAccount).filter(
                SimulationAccount.user_id == user_id
            ).order_by(SimulationAccount.created_at.desc()).all()

            return [self._account_to_dict(account) for account in accounts]

    def _account_to_dict(self, account: SimulationAccount) -> Dict[str, Any]:
        """Convert account model to dictionary"""
        return {
            "account_id": account.id,
            "user_id": account.user_id,
            "name": account.name,
            "initial_balance": account.initial_balance,
            "current_balance": account.current_balance,
            "cash_balance": account.cash_balance,
            "total_pnl": account.total_pnl,
            "total_pnl_pct": account.total_pnl_pct,
            "total_trades": account.total_trades,
            "winning_trades": account.winning_trades,
            "losing_trades": account.losing_trades,
            "win_rate": account.win_rate,
            "max_drawdown": account.max_drawdown,
            "status": account.status,
            "created_at": account.created_at.isoformat()
        }
