"""
Institutional Ownership Service

Tracks institutional ownership and insider transactions:
- 13F filings analysis
- Ownership changes tracking
- Top holders monitoring
- Insider transaction tracking
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import logging
from collections import defaultdict

from .models import InstitutionalHolder, InsiderTransaction, OwnershipChange

logger = logging.getLogger(__name__)


class InstitutionalOwnershipService:
    """Service for tracking institutional ownership and insider activity"""

    def __init__(self):
        # In-memory storage (replace with database in production)
        self._holders: Dict[str, List[InstitutionalHolder]] = defaultdict(list)
        self._insider_transactions: Dict[str, List[InsiderTransaction]] = defaultdict(list)
        self._ownership_changes: Dict[str, List[OwnershipChange]] = defaultdict(list)

    async def get_top_holders(
        self,
        symbol: str,
        limit: int = 20
    ) -> List[InstitutionalHolder]:
        """
        Get top institutional holders for a symbol

        Args:
            symbol: Stock ticker symbol
            limit: Number of top holders to return

        Returns:
            List of top institutional holders
        """
        try:
            holders = self._holders.get(symbol, [])

            # Sort by shares descending
            holders.sort(key=lambda x: x.shares, reverse=True)

            return holders[:limit]

        except Exception as e:
            logger.error(f"Error getting top holders for {symbol}: {e}")
            return []

    async def get_ownership_changes(
        self,
        symbol: str,
        quarters: int = 4
    ) -> List[OwnershipChange]:
        """
        Get ownership change history

        Args:
            symbol: Stock ticker symbol
            quarters: Number of quarters to retrieve

        Returns:
            List of ownership changes by quarter
        """
        try:
            changes = self._ownership_changes.get(symbol, [])

            # Sort by quarter descending
            changes.sort(key=lambda x: x.quarter, reverse=True)

            return changes[:quarters]

        except Exception as e:
            logger.error(f"Error getting ownership changes for {symbol}: {e}")
            return []

    async def get_recent_changes(
        self,
        symbol: str,
        change_type: Optional[str] = None
    ) -> List[InstitutionalHolder]:
        """
        Get recent institutional position changes

        Args:
            symbol: Stock ticker symbol
            change_type: Filter by 'increased', 'decreased', 'new', 'sold_out', or None for all

        Returns:
            List of holders with recent changes
        """
        try:
            holders = self._holders.get(symbol, [])

            # Filter by change type
            if change_type == 'increased':
                filtered = [h for h in holders if h.change > 0]
            elif change_type == 'decreased':
                filtered = [h for h in holders if h.change < 0]
            elif change_type == 'new':
                filtered = [h for h in holders if h.is_new_position]
            elif change_type == 'sold_out':
                filtered = [h for h in holders if h.is_sold_out]
            else:
                filtered = holders

            # Sort by absolute change descending
            filtered.sort(key=lambda x: abs(x.change), reverse=True)

            return filtered

        except Exception as e:
            logger.error(f"Error getting recent changes for {symbol}: {e}")
            return []

    async def get_insider_transactions(
        self,
        symbol: str,
        days: int = 90,
        transaction_type: Optional[str] = None
    ) -> List[InsiderTransaction]:
        """
        Get insider transactions

        Args:
            symbol: Stock ticker symbol
            days: Number of days to look back
            transaction_type: Filter by transaction type (Buy, Sell, etc.)

        Returns:
            List of insider transactions
        """
        try:
            transactions = self._insider_transactions.get(symbol, [])

            # Filter by date range
            cutoff = datetime.now() - timedelta(days=days)
            filtered = [t for t in transactions if t.transaction_date >= cutoff]

            # Filter by transaction type
            if transaction_type:
                filtered = [t for t in filtered if t.transaction_type.lower() == transaction_type.lower()]

            # Sort by transaction date descending
            filtered.sort(key=lambda x: x.transaction_date, reverse=True)

            return filtered

        except Exception as e:
            logger.error(f"Error getting insider transactions for {symbol}: {e}")
            return []

    async def analyze_insider_sentiment(
        self,
        symbol: str,
        days: int = 90
    ) -> Dict[str, Any]:
        """
        Analyze insider trading sentiment

        Args:
            symbol: Stock ticker symbol
            days: Number of days to analyze

        Returns:
            Insider sentiment analysis
        """
        try:
            transactions = await self.get_insider_transactions(symbol, days)

            if not transactions:
                return self._empty_insider_sentiment(symbol, days)

            # Separate buys and sells
            buys = [t for t in transactions if t.transaction_type.lower() == 'buy']
            sells = [t for t in transactions if t.transaction_type.lower() == 'sell']

            total_buy_value = sum(t.value for t in buys)
            total_sell_value = sum(t.value for t in sells)
            net_value = total_buy_value - total_sell_value

            # Calculate sentiment
            if net_value > 0:
                sentiment = "bullish"
            elif net_value < 0:
                sentiment = "bearish"
            else:
                sentiment = "neutral"

            # Insider activity score (-100 to 100)
            total_value = total_buy_value + total_sell_value
            if total_value > 0:
                activity_score = (net_value / total_value) * 100
            else:
                activity_score = 0

            return {
                "symbol": symbol,
                "period_days": days,
                "total_transactions": len(transactions),
                "buy_transactions": len(buys),
                "sell_transactions": len(sells),
                "total_buy_value": total_buy_value,
                "total_sell_value": total_sell_value,
                "net_value": net_value,
                "sentiment": sentiment,
                "activity_score": round(activity_score, 2),
                "recent_insiders": len(set(t.insider_name for t in transactions))
            }

        except Exception as e:
            logger.error(f"Error analyzing insider sentiment for {symbol}: {e}")
            return self._empty_insider_sentiment(symbol, days)

    async def get_institutional_flow(
        self,
        symbol: str,
        quarters: int = 1
    ) -> Dict[str, Any]:
        """
        Calculate institutional money flow

        Args:
            symbol: Stock ticker symbol
            quarters: Number of quarters to analyze

        Returns:
            Institutional flow metrics
        """
        try:
            changes = await self.get_ownership_changes(symbol, quarters)

            if not changes:
                return self._empty_flow(symbol)

            # Use most recent quarter
            latest = changes[0] if changes else None
            if not latest:
                return self._empty_flow(symbol)

            # Calculate flow metrics
            total_holders = latest.total_holders
            net_change = latest.net_change_shares
            net_change_pct = latest.net_change_percentage

            # Determine flow direction
            if net_change_pct > 2:
                flow_direction = "strong_inflow"
            elif net_change_pct > 0:
                flow_direction = "inflow"
            elif net_change_pct < -2:
                flow_direction = "strong_outflow"
            elif net_change_pct < 0:
                flow_direction = "outflow"
            else:
                flow_direction = "neutral"

            # Calculate conviction score based on holder changes
            new_holders = latest.holders_new
            sold_out = latest.holders_sold_out
            conviction_score = ((new_holders - sold_out) / total_holders * 100) if total_holders > 0 else 0

            return {
                "symbol": symbol,
                "quarter": latest.quarter,
                "total_holders": total_holders,
                "institutional_ownership": latest.institutional_ownership_percentage,
                "net_change_shares": net_change,
                "net_change_percentage": net_change_pct,
                "flow_direction": flow_direction,
                "holders_increased": latest.holders_increased,
                "holders_decreased": latest.holders_decreased,
                "holders_new": new_holders,
                "holders_sold_out": sold_out,
                "conviction_score": round(conviction_score, 2)
            }

        except Exception as e:
            logger.error(f"Error calculating institutional flow for {symbol}: {e}")
            return self._empty_flow(symbol)

    async def detect_significant_moves(
        self,
        symbol: str,
        min_change_pct: float = 5.0
    ) -> List[InstitutionalHolder]:
        """
        Detect significant institutional position changes

        Args:
            symbol: Stock ticker symbol
            min_change_pct: Minimum percentage change to consider significant

        Returns:
            List of holders with significant changes
        """
        try:
            holders = self._holders.get(symbol, [])

            # Filter for significant changes
            significant = [
                h for h in holders
                if abs(h.change_percentage) >= min_change_pct
            ]

            # Sort by change percentage descending
            significant.sort(key=lambda x: abs(x.change_percentage), reverse=True)

            return significant

        except Exception as e:
            logger.error(f"Error detecting significant moves for {symbol}: {e}")
            return []

    async def add_holder(self, holder: InstitutionalHolder) -> None:
        """Add institutional holder data"""
        self._holders[holder.shares].append(holder)

    async def add_insider_transaction(self, transaction: InsiderTransaction) -> None:
        """Add insider transaction"""
        self._insider_transactions[transaction.symbol].append(transaction)

    async def add_ownership_change(self, change: OwnershipChange) -> None:
        """Add ownership change data"""
        self._ownership_changes[change.symbol].append(change)

    def _empty_insider_sentiment(self, symbol: str, days: int) -> Dict[str, Any]:
        """Return empty insider sentiment structure"""
        return {
            "symbol": symbol,
            "period_days": days,
            "total_transactions": 0,
            "buy_transactions": 0,
            "sell_transactions": 0,
            "total_buy_value": 0,
            "total_sell_value": 0,
            "net_value": 0,
            "sentiment": "neutral",
            "activity_score": 0,
            "recent_insiders": 0
        }

    def _empty_flow(self, symbol: str) -> Dict[str, Any]:
        """Return empty flow structure"""
        return {
            "symbol": symbol,
            "quarter": "N/A",
            "total_holders": 0,
            "institutional_ownership": 0,
            "net_change_shares": 0,
            "net_change_percentage": 0,
            "flow_direction": "neutral",
            "holders_increased": 0,
            "holders_decreased": 0,
            "holders_new": 0,
            "holders_sold_out": 0,
            "conviction_score": 0
        }

    async def generate_sample_data(self, symbol: str) -> None:
        """Generate sample institutional data for testing"""
        import random

        # Top institutional holders
        institutions = [
            "Vanguard Group Inc",
            "BlackRock Inc",
            "State Street Corp",
            "Fidelity Management & Research",
            "Geode Capital Management",
            "Morgan Stanley",
            "Bank of America Corp",
            "JP Morgan Chase & Co",
            "Goldman Sachs Group Inc",
            "Northern Trust Corp"
        ]

        total_shares = 16000000000  # Example total shares
        base_date = datetime.now() - timedelta(days=45)

        for i, name in enumerate(institutions):
            shares = random.randint(500000000, 1500000000)
            value = shares * 178.50  # Example price
            percentage = (shares / total_shares) * 100
            change = random.randint(-50000000, 50000000)
            change_pct = (change / shares) * 100 if shares > 0 else 0

            holder = InstitutionalHolder(
                name=name,
                shares=shares,
                value=value,
                percentage=round(percentage, 2),
                change=change,
                change_percentage=round(change_pct, 2),
                filing_date=base_date,
                is_new_position=i >= 8,  # Last 2 are new
                is_sold_out=False
            )

            await self.add_holder(holder)

        # Insider transactions
        insiders = [
            ("Tim Cook", "CEO"),
            ("Luca Maestri", "CFO"),
            ("Jeff Williams", "COO"),
            ("Katherine Adams", "General Counsel")
        ]

        for name, title in insiders:
            # Generate 1-3 transactions per insider
            num_txns = random.randint(1, 3)

            for j in range(num_txns):
                days_ago = random.randint(1, 90)
                txn_date = datetime.now() - timedelta(days=days_ago)
                filing_date = txn_date + timedelta(days=random.randint(1, 4))

                shares = random.randint(5000, 100000)
                price = 178.50 + random.uniform(-10, 10)
                value = shares * price

                transaction = InsiderTransaction(
                    symbol=symbol,
                    insider_name=name,
                    title=title,
                    transaction_type="Sell" if random.random() > 0.3 else "Buy",
                    shares=shares,
                    price=round(price, 2),
                    value=round(value, 2),
                    filing_date=filing_date,
                    transaction_date=txn_date,
                    ownership_type="Direct",
                    shares_owned_after=random.randint(1000000, 5000000)
                )

                await self.add_insider_transaction(transaction)

        # Ownership changes
        quarters = ["Q3 2025", "Q2 2025", "Q1 2025", "Q4 2024"]

        for quarter in quarters:
            total_holders = random.randint(5000, 5500)
            holders_increased = random.randint(1800, 2300)
            holders_decreased = random.randint(1600, 2100)
            holders_new = random.randint(300, 500)
            holders_sold_out = random.randint(250, 450)

            total_inst_shares = int(total_shares * 0.62)
            net_change = random.randint(-200000000, 300000000)
            net_change_pct = (net_change / total_inst_shares) * 100

            change = OwnershipChange(
                symbol=symbol,
                quarter=quarter,
                total_holders=total_holders,
                holders_increased=holders_increased,
                holders_decreased=holders_decreased,
                holders_new=holders_new,
                holders_sold_out=holders_sold_out,
                total_shares=total_inst_shares,
                total_value=total_inst_shares * 178.50,
                institutional_ownership_percentage=62.0 + random.uniform(-2, 2),
                net_change_shares=net_change,
                net_change_percentage=round(net_change_pct, 2)
            )

            await self.add_ownership_change(change)

        logger.info(f"Generated sample institutional data for {symbol}")


# Global instance
_institutional_service = None


def get_institutional_service() -> InstitutionalOwnershipService:
    """Get or create institutional ownership service instance"""
    global _institutional_service
    if _institutional_service is None:
        _institutional_service = InstitutionalOwnershipService()
    return _institutional_service
