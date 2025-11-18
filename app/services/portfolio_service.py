"""
Portfolio Management Service
Handles position tracking, real-time P&L, cost basis, and allocation management
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

from app.models import Portfolio, Position, Ticker, TradeJournal
from app.services.market_data import get_current_price

logger = logging.getLogger(__name__)


class PortfolioService:
    """Service for managing portfolios and positions"""

    def __init__(self, db: Session):
        self.db = db

    async def create_portfolio(
        self,
        user_id: str = "default",
        name: str = "My Portfolio",
        initial_capital: float = 100000.0
    ) -> Portfolio:
        """Create a new portfolio"""
        portfolio = Portfolio(
            user_id=user_id,
            name=name,
            initial_capital=initial_capital,
            cash_balance=initial_capital,
            total_value=initial_capital
        )
        self.db.add(portfolio)
        self.db.commit()
        self.db.refresh(portfolio)
        logger.info(f"Created portfolio {portfolio.id} for user {user_id}")
        return portfolio

    async def get_portfolio(self, portfolio_id: int) -> Optional[Portfolio]:
        """Get portfolio by ID"""
        return self.db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

    async def get_user_portfolios(self, user_id: str = "default") -> List[Portfolio]:
        """Get all portfolios for a user"""
        return self.db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

    async def add_position(
        self,
        portfolio_id: int,
        symbol: str,
        quantity: float,
        entry_price: float,
        stop_loss: Optional[float] = None,
        target_price: Optional[float] = None,
        notes: Optional[str] = None
    ) -> Position:
        """Add a new position to the portfolio"""
        # Get or create ticker
        ticker = self.db.query(Ticker).filter(Ticker.symbol == symbol).first()
        if not ticker:
            ticker = Ticker(symbol=symbol, name=symbol)
            self.db.add(ticker)
            self.db.commit()
            self.db.refresh(ticker)

        # Calculate total cost
        total_cost = quantity * entry_price

        # Check if position already exists
        existing_position = self.db.query(Position).filter(
            Position.portfolio_id == portfolio_id,
            Position.ticker_id == ticker.id,
            Position.status == "open"
        ).first()

        if existing_position:
            # Update existing position (average down/up)
            new_quantity = existing_position.quantity + quantity
            new_total_cost = existing_position.total_cost + total_cost
            new_avg_cost = new_total_cost / new_quantity

            existing_position.quantity = new_quantity
            existing_position.total_cost = new_total_cost
            existing_position.avg_cost_basis = new_avg_cost
            existing_position.updated_at = datetime.utcnow()

            if stop_loss:
                existing_position.stop_loss = stop_loss
            if target_price:
                existing_position.target_price = target_price
            if notes:
                existing_position.notes = (existing_position.notes or "") + f"\n{notes}"

            position = existing_position
        else:
            # Create new position
            position = Position(
                portfolio_id=portfolio_id,
                ticker_id=ticker.id,
                quantity=quantity,
                avg_cost_basis=entry_price,
                total_cost=total_cost,
                stop_loss=stop_loss,
                target_price=target_price,
                notes=notes,
                status="open"
            )
            self.db.add(position)

        # Update portfolio cash balance
        portfolio = await self.get_portfolio(portfolio_id)
        if portfolio:
            portfolio.cash_balance -= total_cost
            portfolio.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(position)

        # Update position with current market data
        await self.update_position_pnl(position)

        logger.info(f"Added position {symbol} to portfolio {portfolio_id}")
        return position

    async def remove_position(
        self,
        position_id: int,
        quantity: Optional[float] = None,
        exit_price: Optional[float] = None
    ) -> Tuple[Position, float]:
        """Remove or reduce a position (full or partial exit)"""
        position = self.db.query(Position).filter(Position.id == position_id).first()
        if not position:
            raise ValueError(f"Position {position_id} not found")

        # Use current market price if exit price not provided
        if not exit_price:
            ticker = self.db.query(Ticker).filter(Ticker.id == position.ticker_id).first()
            exit_price = await get_current_price(ticker.symbol)

        # Full or partial exit
        exit_quantity = quantity if quantity else position.quantity
        if exit_quantity > position.quantity:
            raise ValueError(f"Cannot exit {exit_quantity} shares, only {position.quantity} available")

        # Calculate realized P&L
        cost_basis_for_exit = position.avg_cost_basis * exit_quantity
        exit_value = exit_price * exit_quantity
        realized_pnl = exit_value - cost_basis_for_exit
        realized_pnl_pct = (realized_pnl / cost_basis_for_exit) * 100

        # Update portfolio cash balance
        portfolio = await self.get_portfolio(position.portfolio_id)
        if portfolio:
            portfolio.cash_balance += exit_value
            portfolio.updated_at = datetime.utcnow()

        # Update or close position
        if exit_quantity == position.quantity:
            # Full exit
            position.status = "closed"
            position.closed_at = datetime.utcnow()
            position.quantity = 0
        else:
            # Partial exit
            position.quantity -= exit_quantity
            position.total_cost -= cost_basis_for_exit
            position.status = "partial"

        position.updated_at = datetime.utcnow()
        self.db.commit()

        logger.info(f"Removed {exit_quantity} shares from position {position_id}, P&L: ${realized_pnl:.2f}")
        return position, realized_pnl

    async def update_position_pnl(self, position: Position) -> Position:
        """Update position with current market price and P&L"""
        ticker = self.db.query(Ticker).filter(Ticker.id == position.ticker_id).first()
        if not ticker:
            return position

        try:
            current_price = await get_current_price(ticker.symbol)
            position.current_price = current_price
            position.current_value = current_price * position.quantity
            position.unrealized_pnl = position.current_value - position.total_cost
            position.unrealized_pnl_pct = (position.unrealized_pnl / position.total_cost) * 100 if position.total_cost > 0 else 0
            position.updated_at = datetime.utcnow()

            self.db.commit()
        except Exception as e:
            logger.warning(f"Failed to update price for {ticker.symbol}: {e}")

        return position

    async def get_portfolio_positions(self, portfolio_id: int, status: str = "open") -> List[Position]:
        """Get all positions for a portfolio"""
        query = self.db.query(Position).filter(Position.portfolio_id == portfolio_id)
        if status:
            query = query.filter(Position.status == status)
        return query.all()

    async def update_all_positions(self, portfolio_id: int) -> List[Position]:
        """Update all positions with current market prices"""
        positions = await self.get_portfolio_positions(portfolio_id, status="open")
        updated_positions = []

        for position in positions:
            updated = await self.update_position_pnl(position)
            updated_positions.append(updated)

        return updated_positions

    async def calculate_portfolio_metrics(self, portfolio_id: int) -> Dict:
        """Calculate comprehensive portfolio metrics"""
        portfolio = await self.get_portfolio(portfolio_id)
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")

        # Update all positions
        positions = await self.update_all_positions(portfolio_id)

        # Calculate metrics
        total_invested = sum(p.total_cost for p in positions if p.status == "open")
        total_current_value = sum(p.current_value or 0 for p in positions if p.status == "open")
        total_unrealized_pnl = sum(p.unrealized_pnl or 0 for p in positions if p.status == "open")
        total_portfolio_value = portfolio.cash_balance + total_current_value

        # Update portfolio total value
        portfolio.total_value = total_portfolio_value
        portfolio.updated_at = datetime.utcnow()
        self.db.commit()

        # Calculate allocation percentages
        position_allocations = []
        for position in positions:
            if position.status == "open" and position.current_value:
                ticker = self.db.query(Ticker).filter(Ticker.id == position.ticker_id).first()
                allocation_pct = (position.current_value / total_portfolio_value) * 100 if total_portfolio_value > 0 else 0
                position.position_size_pct = allocation_pct

                position_allocations.append({
                    "symbol": ticker.symbol,
                    "value": position.current_value,
                    "allocation_pct": allocation_pct,
                    "pnl": position.unrealized_pnl,
                    "pnl_pct": position.unrealized_pnl_pct
                })

        self.db.commit()

        total_pnl = total_portfolio_value - portfolio.initial_capital
        total_return_pct = (total_pnl / portfolio.initial_capital) * 100 if portfolio.initial_capital > 0 else 0

        return {
            "portfolio_id": portfolio_id,
            "total_value": total_portfolio_value,
            "cash_balance": portfolio.cash_balance,
            "invested_capital": total_invested,
            "total_pnl": total_pnl,
            "total_return_pct": total_return_pct,
            "unrealized_pnl": total_unrealized_pnl,
            "num_positions": len([p for p in positions if p.status == "open"]),
            "allocations": position_allocations,
            "cash_allocation_pct": (portfolio.cash_balance / total_portfolio_value) * 100 if total_portfolio_value > 0 else 0
        }

    async def get_allocation_data(self, portfolio_id: int) -> Dict:
        """Get allocation data for pie chart visualization"""
        metrics = await self.calculate_portfolio_metrics(portfolio_id)

        # Format for pie chart
        pie_data = {
            "labels": [alloc["symbol"] for alloc in metrics["allocations"]],
            "values": [alloc["value"] for alloc in metrics["allocations"]],
            "percentages": [alloc["allocation_pct"] for alloc in metrics["allocations"]]
        }

        # Add cash if significant
        if metrics["cash_allocation_pct"] > 1:
            pie_data["labels"].append("Cash")
            pie_data["values"].append(metrics["cash_balance"])
            pie_data["percentages"].append(metrics["cash_allocation_pct"])

        return pie_data
