"""
Portfolio Risk Management Module for Paper Trading Automation

Manages portfolio-level risk including:
- Max loss per trade (2%)
- Max portfolio heat (6%)
- Correlation checks
- Sector exposure limits
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk level assessment"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PositionRisk:
    """Risk metrics for a single position"""
    ticker: str
    quantity: int
    entry_price: float
    current_price: float
    stop_loss: float

    # Calculated fields
    position_value: float = 0.0
    risk_amount: float = 0.0
    risk_percentage: float = 0.0  # % of account
    unrealized_pnl: float = 0.0
    unrealized_pnl_pct: float = 0.0

    # Metadata
    sector: Optional[str] = None
    industry: Optional[str] = None
    entry_date: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self.position_value = self.quantity * self.current_price
        self.risk_amount = self.quantity * (self.entry_price - self.stop_loss)
        self.unrealized_pnl = self.quantity * (self.current_price - self.entry_price)
        self.unrealized_pnl_pct = ((self.current_price / self.entry_price) - 1) * 100


@dataclass
class PortfolioRisk:
    """Portfolio-level risk metrics"""
    account_value: float
    total_positions: int
    total_exposure: float
    total_risk_amount: float
    portfolio_heat: float  # % of account at risk

    # Diversification
    sectors: Dict[str, float]  # sector -> exposure %
    industries: Dict[str, float]  # industry -> exposure %

    # Risk levels
    positions_at_risk: List[str]  # Tickers with high risk
    risk_level: RiskLevel = RiskLevel.LOW

    # Recommendations
    warnings: List[str] = field(default_factory=list)
    can_add_position: bool = True
    max_new_position_size: float = 0.0


@dataclass
class CorrelationMatrix:
    """Correlation between positions"""
    tickers: List[str]
    correlations: Dict[Tuple[str, str], float] = field(default_factory=dict)
    high_correlation_pairs: List[Tuple[str, str]] = field(default_factory=list)


class PortfolioRiskManager:
    """
    Manage portfolio-level risk for paper trading
    """

    def __init__(
        self,
        account_size: float,
        max_risk_per_trade_pct: float = 2.0,
        max_portfolio_heat_pct: float = 6.0,
        max_sector_exposure_pct: float = 25.0,
        max_correlation: float = 0.7
    ):
        """
        Initialize portfolio risk manager

        Args:
            account_size: Total account value
            max_risk_per_trade_pct: Maximum risk per trade (default 2%)
            max_portfolio_heat_pct: Maximum total risk (default 6%)
            max_sector_exposure_pct: Maximum exposure per sector (default 25%)
            max_correlation: Maximum correlation between positions (default 0.7)
        """
        self.account_size = account_size
        self.max_risk_per_trade_pct = max_risk_per_trade_pct
        self.max_portfolio_heat_pct = max_portfolio_heat_pct
        self.max_sector_exposure_pct = max_sector_exposure_pct
        self.max_correlation = max_correlation

        self.positions: Dict[str, PositionRisk] = {}
        self.logger = logging.getLogger(__name__)

    def add_position(self, position: PositionRisk) -> None:
        """Add a position to the portfolio"""
        position.risk_percentage = (position.risk_amount / self.account_size) * 100
        self.positions[position.ticker] = position
        self.logger.info(f"Added position {position.ticker} with {position.risk_percentage:.2f}% risk")

    def remove_position(self, ticker: str) -> None:
        """Remove a position from the portfolio"""
        if ticker in self.positions:
            del self.positions[ticker]
            self.logger.info(f"Removed position {ticker}")

    def update_position_price(self, ticker: str, current_price: float) -> None:
        """Update current price for a position"""
        if ticker in self.positions:
            position = self.positions[ticker]
            position.current_price = current_price
            position.position_value = position.quantity * current_price
            position.unrealized_pnl = position.quantity * (current_price - position.entry_price)
            position.unrealized_pnl_pct = ((current_price / position.entry_price) - 1) * 100

    def calculate_portfolio_heat(self) -> float:
        """
        Calculate total portfolio heat (% of account at risk)

        Returns:
            Portfolio heat as percentage
        """
        total_risk = sum(pos.risk_amount for pos in self.positions.values())
        return (total_risk / self.account_size) * 100

    def calculate_sector_exposure(self) -> Dict[str, float]:
        """
        Calculate exposure by sector

        Returns:
            Dictionary of sector -> exposure percentage
        """
        sector_exposure = {}

        for position in self.positions.values():
            if position.sector:
                sector_exposure[position.sector] = sector_exposure.get(position.sector, 0.0)
                sector_exposure[position.sector] += position.position_value

        # Convert to percentages
        for sector in sector_exposure:
            sector_exposure[sector] = (sector_exposure[sector] / self.account_size) * 100

        return sector_exposure

    def calculate_industry_exposure(self) -> Dict[str, float]:
        """
        Calculate exposure by industry

        Returns:
            Dictionary of industry -> exposure percentage
        """
        industry_exposure = {}

        for position in self.positions.values():
            if position.industry:
                industry_exposure[position.industry] = industry_exposure.get(position.industry, 0.0)
                industry_exposure[position.industry] += position.position_value

        # Convert to percentages
        for industry in industry_exposure:
            industry_exposure[industry] = (industry_exposure[industry] / self.account_size) * 100

        return industry_exposure

    def check_correlation(
        self,
        ticker1: str,
        ticker2: str,
        correlation: float
    ) -> bool:
        """
        Check if correlation between two positions is acceptable

        Args:
            ticker1: First ticker
            ticker2: Second ticker
            correlation: Correlation coefficient (-1 to 1)

        Returns:
            True if correlation is acceptable, False otherwise
        """
        return abs(correlation) <= self.max_correlation

    def can_add_new_position(
        self,
        risk_amount: float,
        sector: Optional[str] = None,
        position_value: Optional[float] = None
    ) -> Tuple[bool, List[str]]:
        """
        Check if a new position can be added without exceeding risk limits

        Args:
            risk_amount: Risk amount for the new position
            sector: Sector of the new position
            position_value: Value of the new position

        Returns:
            Tuple of (can_add, list_of_reasons)
        """
        reasons = []

        # Check per-trade risk limit
        risk_pct = (risk_amount / self.account_size) * 100
        if risk_pct > self.max_risk_per_trade_pct:
            reasons.append(
                f"Risk {risk_pct:.2f}% exceeds max per-trade risk of {self.max_risk_per_trade_pct}%"
            )

        # Check portfolio heat limit
        current_heat = self.calculate_portfolio_heat()
        new_heat = current_heat + risk_pct

        if new_heat > self.max_portfolio_heat_pct:
            reasons.append(
                f"New portfolio heat {new_heat:.2f}% would exceed max of {self.max_portfolio_heat_pct}%"
            )

        # Check sector exposure limit
        if sector and position_value:
            sector_exposure = self.calculate_sector_exposure()
            current_sector_exp = sector_exposure.get(sector, 0.0)
            new_position_pct = (position_value / self.account_size) * 100
            new_sector_exp = current_sector_exp + new_position_pct

            if new_sector_exp > self.max_sector_exposure_pct:
                reasons.append(
                    f"Sector {sector} exposure would be {new_sector_exp:.2f}% "
                    f"(max: {self.max_sector_exposure_pct}%)"
                )

        can_add = len(reasons) == 0

        if can_add:
            self.logger.info(
                f"New position approved: Risk={risk_pct:.2f}%, "
                f"Portfolio heat={new_heat:.2f}%"
            )
        else:
            self.logger.warning(f"New position rejected: {'; '.join(reasons)}")

        return can_add, reasons

    def get_max_position_size(
        self,
        entry_price: float,
        stop_loss: float,
        sector: Optional[str] = None
    ) -> int:
        """
        Calculate maximum position size based on risk limits

        Args:
            entry_price: Entry price
            stop_loss: Stop loss price
            sector: Sector (for sector exposure check)

        Returns:
            Maximum number of shares
        """
        # Calculate based on per-trade risk limit
        max_risk_amount = self.account_size * (self.max_risk_per_trade_pct / 100)
        risk_per_share = entry_price - stop_loss

        if risk_per_share <= 0:
            return 0

        max_shares_risk = int(max_risk_amount / risk_per_share)

        # Calculate based on portfolio heat limit
        current_heat = self.calculate_portfolio_heat()
        remaining_heat = self.max_portfolio_heat_pct - current_heat

        if remaining_heat <= 0:
            self.logger.warning("Portfolio heat limit reached, cannot add new positions")
            return 0

        max_heat_risk = self.account_size * (remaining_heat / 100)
        max_shares_heat = int(max_heat_risk / risk_per_share)

        # Take the minimum
        max_shares = min(max_shares_risk, max_shares_heat)

        # Check sector exposure if applicable
        if sector:
            sector_exposure = self.calculate_sector_exposure()
            current_sector_exp = sector_exposure.get(sector, 0.0)
            remaining_sector = self.max_sector_exposure_pct - current_sector_exp

            if remaining_sector <= 0:
                self.logger.warning(f"Sector {sector} exposure limit reached")
                return 0

            max_sector_value = self.account_size * (remaining_sector / 100)
            max_shares_sector = int(max_sector_value / entry_price)
            max_shares = min(max_shares, max_shares_sector)

        return max_shares

    def assess_risk_level(self) -> RiskLevel:
        """
        Assess overall portfolio risk level

        Returns:
            RiskLevel enum
        """
        heat = self.calculate_portfolio_heat()

        if heat >= self.max_portfolio_heat_pct:
            return RiskLevel.CRITICAL
        elif heat >= self.max_portfolio_heat_pct * 0.75:
            return RiskLevel.HIGH
        elif heat >= self.max_portfolio_heat_pct * 0.5:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.LOW

    def get_portfolio_risk_report(self) -> PortfolioRisk:
        """
        Generate comprehensive portfolio risk report

        Returns:
            PortfolioRisk object with all metrics
        """
        total_exposure = sum(pos.position_value for pos in self.positions.values())
        total_risk = sum(pos.risk_amount for pos in self.positions.values())
        portfolio_heat = (total_risk / self.account_size) * 100

        sector_exposure = self.calculate_sector_exposure()
        industry_exposure = self.calculate_industry_exposure()

        # Find positions at risk
        positions_at_risk = []
        warnings = []

        for ticker, position in self.positions.items():
            # Check if position is down significantly
            if position.unrealized_pnl_pct < -5.0:
                positions_at_risk.append(ticker)
                warnings.append(
                    f"{ticker} down {abs(position.unrealized_pnl_pct):.1f}%"
                )

        # Check sector concentration
        for sector, exposure in sector_exposure.items():
            if exposure > self.max_sector_exposure_pct:
                warnings.append(
                    f"Sector {sector} overexposed: {exposure:.1f}% "
                    f"(max: {self.max_sector_exposure_pct}%)"
                )

        # Check portfolio heat
        if portfolio_heat > self.max_portfolio_heat_pct:
            warnings.append(
                f"Portfolio heat {portfolio_heat:.1f}% exceeds limit "
                f"({self.max_portfolio_heat_pct}%)"
            )

        # Determine if can add new position
        current_heat = portfolio_heat
        can_add = current_heat < self.max_portfolio_heat_pct * 0.9  # Leave 10% buffer

        # Calculate max new position size
        remaining_heat = max(0, self.max_portfolio_heat_pct - current_heat)
        max_new_position = (remaining_heat / 100) * self.account_size

        risk_level = self.assess_risk_level()

        report = PortfolioRisk(
            account_value=self.account_size,
            total_positions=len(self.positions),
            total_exposure=total_exposure,
            total_risk_amount=total_risk,
            portfolio_heat=portfolio_heat,
            sectors=sector_exposure,
            industries=industry_exposure,
            positions_at_risk=positions_at_risk,
            risk_level=risk_level,
            warnings=warnings,
            can_add_position=can_add,
            max_new_position_size=max_new_position
        )

        self.logger.info(
            f"Portfolio Risk Report: {len(self.positions)} positions, "
            f"{portfolio_heat:.2f}% heat, {risk_level.value} risk"
        )

        return report

    def get_position(self, ticker: str) -> Optional[PositionRisk]:
        """Get position by ticker"""
        return self.positions.get(ticker)

    def get_all_positions(self) -> List[PositionRisk]:
        """Get all positions"""
        return list(self.positions.values())

    def update_account_size(self, new_size: float) -> None:
        """Update account size (after profits/losses)"""
        old_size = self.account_size
        self.account_size = new_size

        # Recalculate all position risk percentages
        for position in self.positions.values():
            position.risk_percentage = (position.risk_amount / self.account_size) * 100

        self.logger.info(
            f"Updated account size from ${old_size:,.2f} to ${new_size:,.2f} "
            f"({((new_size/old_size - 1) * 100):+.2f}%)"
        )

    def clear_positions(self) -> None:
        """Clear all positions"""
        self.positions.clear()
        self.logger.info("Cleared all positions")


def calculate_position_correlation(
    prices1: List[float],
    prices2: List[float]
) -> float:
    """
    Calculate correlation between two price series

    Args:
        prices1: Price series for asset 1
        prices2: Price series for asset 2

    Returns:
        Correlation coefficient (-1 to 1)
    """
    import numpy as np

    if len(prices1) != len(prices2) or len(prices1) < 2:
        return 0.0

    # Calculate returns
    returns1 = np.diff(prices1) / prices1[:-1]
    returns2 = np.diff(prices2) / prices2[:-1]

    # Calculate correlation
    correlation = np.corrcoef(returns1, returns2)[0, 1]

    return float(correlation) if not np.isnan(correlation) else 0.0


def check_sector_diversification(
    positions: List[PositionRisk],
    max_sector_concentration: float = 0.3
) -> Tuple[bool, Dict[str, float]]:
    """
    Check if portfolio is well-diversified across sectors

    Args:
        positions: List of positions
        max_sector_concentration: Max % in single sector (default 30%)

    Returns:
        Tuple of (is_diversified, sector_concentrations)
    """
    total_value = sum(pos.position_value for pos in positions)

    if total_value == 0:
        return True, {}

    sector_values = {}
    for pos in positions:
        if pos.sector:
            sector_values[pos.sector] = sector_values.get(pos.sector, 0.0)
            sector_values[pos.sector] += pos.position_value

    # Calculate concentrations
    sector_concentrations = {
        sector: value / total_value
        for sector, value in sector_values.items()
    }

    # Check if any sector is over-concentrated
    max_concentration = max(sector_concentrations.values()) if sector_concentrations else 0.0
    is_diversified = max_concentration <= max_sector_concentration

    return is_diversified, sector_concentrations
