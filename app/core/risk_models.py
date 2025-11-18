"""
Risk Management Data Models
Professional risk management data structures for trading
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum


class RiskMethod(str, Enum):
    """Position sizing method"""
    FIXED_FRACTIONAL = "fixed_fractional"
    KELLY_CRITERION = "kelly_criterion"
    KELLY_HALF = "kelly_half"
    KELLY_QUARTER = "kelly_quarter"
    ATR_BASED = "atr_based"
    VOLATILITY_ADJUSTED = "volatility_adjusted"
    PORTFOLIO_HEAT = "portfolio_heat"


class VolatilityRegime(str, Enum):
    """Market volatility regime"""
    LOW = "low"  # VIX < 15
    NORMAL = "normal"  # VIX 15-25
    ELEVATED = "elevated"  # VIX 25-35
    HIGH = "high"  # VIX > 35


@dataclass
class KellyResult:
    """Kelly Criterion calculation result"""
    kelly_percentage: float  # Full Kelly %
    kelly_fraction: str  # "full", "half", "quarter"
    adjusted_percentage: float  # Adjusted Kelly % (e.g., Kelly/2)
    position_size: int  # Number of shares
    position_dollars: float  # Dollar value
    edge: float  # Trading edge (win% - loss% adjusted)
    risk_of_ruin: float  # Probability of ruin
    notes: List[str] = field(default_factory=list)


@dataclass
class FixedFractionalResult:
    """Fixed fractional position sizing result"""
    risk_percentage: float  # % of account to risk
    account_size: float
    risk_dollars: float  # Dollar amount at risk
    position_size: int  # Number of shares
    position_dollars: float  # Total position value
    max_positions: int  # Max concurrent positions
    position_heat: float  # % of account in this position
    notes: List[str] = field(default_factory=list)


@dataclass
class VolatilityBasedResult:
    """Volatility-based position sizing result"""
    atr: float  # Average True Range
    atr_period: int  # ATR calculation period
    atr_multiplier: float  # Stop distance in ATR units
    stop_distance: float  # Actual stop distance in $
    position_size: int  # Shares based on volatility
    position_dollars: float
    volatility_regime: VolatilityRegime
    vix: Optional[float] = None  # Current VIX level
    volatility_adjustment: float = 1.0  # Position size multiplier
    notes: List[str] = field(default_factory=list)


@dataclass
class PortfolioPosition:
    """Individual position in portfolio"""
    symbol: str
    shares: int
    entry_price: float
    current_price: float
    stop_loss: float
    target: float
    entry_date: datetime
    sector: Optional[str] = None

    @property
    def market_value(self) -> float:
        """Current market value"""
        return self.shares * self.current_price

    @property
    def cost_basis(self) -> float:
        """Original cost"""
        return self.shares * self.entry_price

    @property
    def unrealized_pnl(self) -> float:
        """Unrealized P&L"""
        return self.market_value - self.cost_basis

    @property
    def risk_dollars(self) -> float:
        """Dollar amount at risk"""
        return abs(self.current_price - self.stop_loss) * self.shares

    @property
    def pnl_percentage(self) -> float:
        """P&L as percentage"""
        return (self.unrealized_pnl / self.cost_basis) * 100 if self.cost_basis > 0 else 0


@dataclass
class PortfolioHeat:
    """Portfolio-level risk metrics"""
    total_account_value: float
    total_positions_value: float
    total_cash: float
    total_risk_dollars: float  # Sum of all position risks
    total_risk_percentage: float  # Risk as % of account

    # Position details
    positions: List[PortfolioPosition] = field(default_factory=list)
    num_positions: int = 0

    # Risk concentration
    largest_position_pct: float = 0.0
    largest_risk_pct: float = 0.0
    sector_concentration: Dict[str, float] = field(default_factory=dict)

    # Correlation (placeholder for advanced version)
    correlation_adjusted_risk: Optional[float] = None

    # Heat levels
    heat_score: float = 0.0  # 0-100 composite risk score

    # Limits
    max_portfolio_risk_pct: float = 10.0  # Max total risk
    max_single_position_pct: float = 20.0  # Max single position size
    max_sector_concentration_pct: float = 30.0  # Max sector allocation

    # Status flags
    is_overheated: bool = False
    warnings: List[str] = field(default_factory=list)

    def calculate_heat_score(self) -> float:
        """
        Calculate composite heat score (0-100)
        Higher = more risk
        """
        score = 0.0

        # Risk percentage contribution (40% weight)
        risk_component = min(100, (self.total_risk_percentage / self.max_portfolio_risk_pct) * 100)
        score += risk_component * 0.4

        # Position concentration (30% weight)
        concentration_component = min(100, (self.largest_position_pct / self.max_single_position_pct) * 100)
        score += concentration_component * 0.3

        # Number of positions (20% weight) - more positions = more risk
        position_component = min(100, (self.num_positions / 10) * 100)
        score += position_component * 0.2

        # Sector concentration (10% weight)
        if self.sector_concentration:
            max_sector = max(self.sector_concentration.values())
            sector_component = min(100, (max_sector / self.max_sector_concentration_pct) * 100)
            score += sector_component * 0.1

        self.heat_score = round(score, 2)
        return self.heat_score

    def check_limits(self) -> List[str]:
        """Check if portfolio exceeds risk limits"""
        warnings = []

        if self.total_risk_percentage > self.max_portfolio_risk_pct:
            warnings.append(
                f"⚠️ PORTFOLIO RISK EXCEEDED: {self.total_risk_percentage:.1f}% "
                f"(max: {self.max_portfolio_risk_pct}%)"
            )
            self.is_overheated = True

        if self.largest_position_pct > self.max_single_position_pct:
            warnings.append(
                f"⚠️ POSITION SIZE EXCEEDED: {self.largest_position_pct:.1f}% "
                f"(max: {self.max_single_position_pct}%)"
            )
            self.is_overheated = True

        if self.sector_concentration:
            for sector, pct in self.sector_concentration.items():
                if pct > self.max_sector_concentration_pct:
                    warnings.append(
                        f"⚠️ SECTOR CONCENTRATION: {sector} at {pct:.1f}% "
                        f"(max: {self.max_sector_concentration_pct}%)"
                    )
                    self.is_overheated = True

        self.warnings = warnings
        return warnings


@dataclass
class RiskPyramid:
    """Risk pyramid visualization data"""
    tier1_conservative: List[str]  # 40% allocation
    tier2_moderate: List[str]  # 40% allocation
    tier3_aggressive: List[str]  # 20% allocation
    tier1_pct: float = 40.0
    tier2_pct: float = 40.0
    tier3_pct: float = 20.0


@dataclass
class RiskVisualization:
    """Data for risk visualizations"""
    # Position size comparison
    position_sizes: Dict[str, float]  # symbol -> position value
    position_risks: Dict[str, float]  # symbol -> risk dollars

    # Heat map data
    heat_map: Dict[str, Dict[str, float]]  # symbol -> {risk%, size%, pnl%}

    # Risk distribution
    risk_distribution: Dict[str, float]  # category -> percentage

    # Risk pyramid
    pyramid: Optional[RiskPyramid] = None

    # Charts data (for plotting)
    chart_data: Dict[str, any] = field(default_factory=dict)
