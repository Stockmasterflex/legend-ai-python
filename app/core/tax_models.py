"""
Tax Optimization Core Models
Pydantic models for tax calculations, scenarios, and reporting
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator


class HoldingPeriod(str, Enum):
    """Tax holding period classification"""
    SHORT_TERM = "short_term"  # <= 1 year
    LONG_TERM = "long_term"    # > 1 year


class TaxTreatment(str, Enum):
    """Tax treatment type"""
    ORDINARY_INCOME = "ordinary_income"
    CAPITAL_GAIN = "capital_gain"
    QUALIFIED_DIVIDEND = "qualified_dividend"


class WashSaleStatus(str, Enum):
    """Wash sale status"""
    CLEAN = "clean"
    VIOLATION = "violation"
    PENDING = "pending"
    WARNING = "warning"


class TaxBracket(str, Enum):
    """Federal tax brackets (2024)"""
    BRACKET_10 = "10%"    # $0 - $11,600
    BRACKET_12 = "12%"    # $11,601 - $47,150
    BRACKET_22 = "22%"    # $47,151 - $100,525
    BRACKET_24 = "24%"    # $100,526 - $191,950
    BRACKET_32 = "32%"    # $191,951 - $243,725
    BRACKET_35 = "35%"    # $243,726 - $609,350
    BRACKET_37 = "37%"    # $609,351+


class CapitalGainsBracket(str, Enum):
    """Long-term capital gains tax brackets (2024)"""
    BRACKET_0 = "0%"      # $0 - $47,025
    BRACKET_15 = "15%"    # $47,026 - $518,900
    BRACKET_20 = "20%"    # $518,901+


class HarvestAction(str, Enum):
    """Tax loss harvesting action"""
    PENDING = "pending"
    HARVESTED = "harvested"
    SKIPPED = "skipped"
    EXPIRED = "expired"


# Pydantic Models for API

class TaxLotModel(BaseModel):
    """Tax lot information"""
    id: Optional[int] = None
    symbol: str
    quantity: float
    remaining_quantity: float
    cost_basis: float
    price_per_share: float
    purchase_date: datetime
    holding_period: Optional[HoldingPeriod] = None
    wash_sale_disallowed: float = 0.0
    adjusted_cost_basis: float
    is_closed: bool = False
    trade_id: Optional[str] = None

    @validator('adjusted_cost_basis', pre=True, always=True)
    def set_adjusted_cost_basis(cls, v, values):
        if v is None or v == 0:
            return values.get('cost_basis', 0) + values.get('wash_sale_disallowed', 0)
        return v

    class Config:
        from_attributes = True


class CapitalGainModel(BaseModel):
    """Capital gain/loss information"""
    id: Optional[int] = None
    symbol: str
    quantity: float
    sale_price: float
    sale_date: datetime
    proceeds: float
    cost_basis: float
    adjusted_cost_basis: float
    gain_loss: float
    holding_period: HoldingPeriod
    wash_sale_loss_disallowed: float = 0.0
    tax_year: int
    trade_id: Optional[str] = None

    class Config:
        from_attributes = True


class WashSaleModel(BaseModel):
    """Wash sale violation information"""
    id: Optional[int] = None
    symbol: str
    loss_sale_date: datetime
    loss_amount: float
    loss_quantity: float
    replacement_purchase_date: Optional[datetime] = None
    replacement_quantity: Optional[float] = None
    status: WashSaleStatus
    days_between: Optional[int] = None
    disallowed_loss: float = 0.0
    suggested_alternatives: Optional[List[str]] = None

    class Config:
        from_attributes = True


class TaxHarvestOpportunity(BaseModel):
    """Tax loss harvesting opportunity"""
    symbol: str
    tax_lot_id: int
    unrealized_loss: float
    current_price: float
    cost_basis: float
    quantity: float
    estimated_tax_savings: float
    replacement_suggestions: List[Dict[str, Any]] = []
    days_until_wash_safe: Optional[int] = None
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GainLossReport(BaseModel):
    """Comprehensive gain/loss report"""
    tax_year: int
    short_term_gains: float = 0.0
    short_term_losses: float = 0.0
    long_term_gains: float = 0.0
    long_term_losses: float = 0.0
    net_short_term: float = 0.0
    net_long_term: float = 0.0
    total_net_gain_loss: float = 0.0
    wash_sale_adjustments: float = 0.0
    realized_gains: List[CapitalGainModel] = []
    unrealized_gains: List[Dict[str, Any]] = []

    @validator('net_short_term', pre=True, always=True)
    def calc_net_short_term(cls, v, values):
        return values.get('short_term_gains', 0) + values.get('short_term_losses', 0)

    @validator('net_long_term', pre=True, always=True)
    def calc_net_long_term(cls, v, values):
        return values.get('long_term_gains', 0) + values.get('long_term_losses', 0)

    @validator('total_net_gain_loss', pre=True, always=True)
    def calc_total_net(cls, v, values):
        return values.get('net_short_term', 0) + values.get('net_long_term', 0)


class TaxEstimate(BaseModel):
    """Tax impact estimate"""
    short_term_tax: float = 0.0
    long_term_tax: float = 0.0
    total_tax: float = 0.0
    effective_rate: float = 0.0
    marginal_rate: float = 0.0
    ordinary_income_bracket: Optional[TaxBracket] = None
    capital_gains_bracket: Optional[CapitalGainsBracket] = None


class ScenarioAnalysis(BaseModel):
    """What-if scenario analysis"""
    scenario_name: str
    description: str
    current_gain_loss: float
    projected_gain_loss: float
    current_tax: float
    projected_tax: float
    tax_savings: float
    recommended_actions: List[str] = []
    assumptions: Dict[str, Any] = {}


class TaxOptimizationStrategy(BaseModel):
    """Tax optimization strategy recommendation"""
    strategy_name: str
    priority: int = Field(ge=1, le=10)
    potential_savings: float
    risk_level: str = Field(regex="^(low|medium|high)$")
    actions: List[str]
    wash_sale_risks: List[str] = []
    time_sensitive: bool = False
    deadline: Optional[datetime] = None


class Form8949Entry(BaseModel):
    """IRS Form 8949 entry"""
    description: str  # e.g., "100 shares AAPL"
    date_acquired: str
    date_sold: str
    proceeds: float
    cost_basis: float
    adjustment_code: Optional[str] = None  # W for wash sale
    adjustment_amount: float = 0.0
    gain_loss: float


class TurbotaxCSVEntry(BaseModel):
    """TurboTax CSV format entry"""
    security_name: str
    symbol: str
    shares: float
    date_acquired: str
    date_sold: str
    sales_price: float
    cost_basis: float
    gain_loss: float
    term: str  # "Short" or "Long"


# Dataclasses for internal calculations

@dataclass
class TaxCalculation:
    """Internal tax calculation result"""
    gross_income: float
    capital_gains: float
    ordinary_income: float
    deductions: float
    taxable_income: float
    tax_owed: float
    effective_rate: float


@dataclass
class WashSaleCheck:
    """Wash sale check result"""
    is_violation: bool
    days_until_safe: int
    conflicting_transactions: List[Dict[str, Any]]
    disallowed_loss: float
    adjusted_cost_basis: float


@dataclass
class ReplacementSecurity:
    """Suggested replacement security for tax loss harvesting"""
    symbol: str
    name: str
    similarity_score: float  # 0-1
    correlation: float  # -1 to 1
    sector: str
    current_price: float
    wash_sale_safe: bool
    reasons: List[str]


# Helper functions

def calculate_holding_period(purchase_date: datetime, sale_date: datetime) -> HoldingPeriod:
    """Calculate holding period for tax purposes"""
    holding_days = (sale_date - purchase_date).days
    if holding_days <= 365:
        return HoldingPeriod.SHORT_TERM
    return HoldingPeriod.LONG_TERM


def is_wash_sale_violation(loss_date: datetime, purchase_date: datetime) -> bool:
    """
    Check if a transaction violates the wash sale rule.
    IRS 30-day rule: Can't buy substantially identical security 30 days
    before or after realizing a loss.
    """
    days_diff = abs((purchase_date - loss_date).days)
    return days_diff <= 30


def get_tax_rate_for_bracket(bracket: TaxBracket) -> float:
    """Get numeric tax rate from bracket enum"""
    rates = {
        TaxBracket.BRACKET_10: 0.10,
        TaxBracket.BRACKET_12: 0.12,
        TaxBracket.BRACKET_22: 0.22,
        TaxBracket.BRACKET_24: 0.24,
        TaxBracket.BRACKET_32: 0.32,
        TaxBracket.BRACKET_35: 0.35,
        TaxBracket.BRACKET_37: 0.37,
    }
    return rates.get(bracket, 0.22)  # Default to 22%


def get_capital_gains_rate(bracket: CapitalGainsBracket) -> float:
    """Get numeric rate from capital gains bracket"""
    rates = {
        CapitalGainsBracket.BRACKET_0: 0.00,
        CapitalGainsBracket.BRACKET_15: 0.15,
        CapitalGainsBracket.BRACKET_20: 0.20,
    }
    return rates.get(bracket, 0.15)  # Default to 15%


def determine_tax_year(sale_date: datetime) -> int:
    """Determine tax year from sale date"""
    return sale_date.year


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"


def calculate_days_between(date1: datetime, date2: datetime) -> int:
    """Calculate days between two dates (absolute value)"""
    return abs((date2 - date1).days)
