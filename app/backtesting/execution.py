"""
Execution Simulation
Realistic simulation of order execution with slippage, commissions, market impact, and partial fills
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple
import random
import pandas as pd


class CommissionType(str, Enum):
    """Commission model types"""
    FIXED = "fixed"  # Fixed $ per trade
    PERCENTAGE = "percentage"  # Percentage of trade value
    PER_SHARE = "per_share"  # $ per share
    TIERED = "tiered"  # Tiered based on volume


class SlippageType(str, Enum):
    """Slippage model types"""
    FIXED_BPS = "fixed_bps"  # Fixed basis points
    PERCENTAGE = "percentage"  # Percentage of price
    VOLUME_BASED = "volume_based"  # Based on order size vs volume
    RANDOM = "random"  # Random within range


@dataclass
class CommissionModel:
    """Commission calculation model"""
    type: CommissionType
    value: float  # Depends on type
    minimum: float = 0.0
    maximum: Optional[float] = None

    def calculate(self, quantity: int, price: float) -> float:
        """
        Calculate commission for a trade

        Args:
            quantity: Number of shares
            price: Price per share

        Returns:
            Commission amount in $
        """
        if self.type == CommissionType.FIXED:
            commission = self.value

        elif self.type == CommissionType.PERCENTAGE:
            commission = (quantity * price) * (self.value / 100)

        elif self.type == CommissionType.PER_SHARE:
            commission = quantity * self.value

        elif self.type == CommissionType.TIERED:
            # Simplified tiered model
            trade_value = quantity * price
            if trade_value < 1000:
                commission = 10.0
            elif trade_value < 10000:
                commission = 5.0
            else:
                commission = 1.0

        else:
            commission = 0.0

        # Apply min/max
        commission = max(commission, self.minimum)
        if self.maximum is not None:
            commission = min(commission, self.maximum)

        return commission


@dataclass
class SlippageModel:
    """Slippage calculation model"""
    type: SlippageType
    value: float  # Depends on type
    is_aggressive: bool = False  # More aggressive execution = more slippage

    def calculate(
        self,
        quantity: int,
        price: float,
        volume: float,
        is_buy: bool,
    ) -> Tuple[float, float]:
        """
        Calculate slippage and adjusted price

        Args:
            quantity: Order quantity
            price: Target price
            volume: Bar volume
            is_buy: True for buy, False for sell

        Returns:
            (slippage_amount, adjusted_price)
        """
        slippage_pct = 0.0

        if self.type == SlippageType.FIXED_BPS:
            # Fixed basis points (1 bps = 0.01%)
            slippage_pct = self.value / 10000

        elif self.type == SlippageType.PERCENTAGE:
            slippage_pct = self.value / 100

        elif self.type == SlippageType.VOLUME_BASED:
            # Slippage based on order size relative to volume
            if volume > 0:
                participation_rate = quantity / volume
                # More slippage for larger participation
                slippage_pct = participation_rate * self.value
            else:
                slippage_pct = self.value  # Default if no volume data

        elif self.type == SlippageType.RANDOM:
            # Random slippage up to max value
            slippage_pct = random.uniform(0, self.value / 100)

        # Aggressive execution increases slippage
        if self.is_aggressive:
            slippage_pct *= 1.5

        # Apply slippage direction
        if is_buy:
            # Buy at higher price
            adjusted_price = price * (1 + slippage_pct)
        else:
            # Sell at lower price
            adjusted_price = price * (1 - slippage_pct)

        slippage_amount = abs(adjusted_price - price) * quantity

        return slippage_amount, adjusted_price


@dataclass
class MarketImpactModel:
    """
    Market impact model (for large orders)
    Price moves against you as you execute
    """
    enabled: bool = False
    impact_coefficient: float = 0.1  # How much order moves market
    temporary_impact_pct: float = 0.5  # % that is temporary vs permanent

    def calculate(
        self,
        quantity: int,
        price: float,
        volume: float,
        volatility: float,
        is_buy: bool,
    ) -> Tuple[float, float]:
        """
        Calculate market impact

        Args:
            quantity: Order quantity
            price: Current price
            volume: Average daily volume
            volatility: Price volatility (std dev)
            is_buy: True for buy, False for sell

        Returns:
            (impact_cost, price_with_impact)
        """
        if not self.enabled or volume == 0:
            return 0.0, price

        # Calculate participation rate
        participation = quantity / volume

        # Square root impact model (common in research)
        # Impact ∝ σ * √(Q/V)
        impact_pct = volatility * self.impact_coefficient * (participation ** 0.5)

        # Apply direction
        if is_buy:
            impacted_price = price * (1 + impact_pct)
        else:
            impacted_price = price * (1 - impact_pct)

        impact_cost = abs(impacted_price - price) * quantity

        return impact_cost, impacted_price


@dataclass
class PartialFillModel:
    """
    Partial fill simulation
    Orders may not fill completely
    """
    enabled: bool = False
    min_fill_rate: float = 0.5  # Minimum % of order that fills
    max_fill_rate: float = 1.0  # Maximum % of order that fills

    def simulate_fill(
        self,
        quantity: int,
        price: float,
        volume: float,
        liquidity_threshold: float = 0.1,  # Max % of volume to fill
    ) -> Tuple[int, bool]:
        """
        Simulate partial fill

        Args:
            quantity: Desired quantity
            price: Order price
            volume: Bar volume
            liquidity_threshold: Max % of volume that can be filled

        Returns:
            (filled_quantity, is_complete)
        """
        if not self.enabled:
            return quantity, True

        # Calculate liquidity-based fill rate
        if volume > 0:
            max_fillable = int(volume * liquidity_threshold)
            if quantity > max_fillable:
                # Can't fill entire order
                filled = max_fillable
                is_complete = False
            else:
                # Can fill, but simulate partial fill anyway
                fill_rate = random.uniform(self.min_fill_rate, self.max_fill_rate)
                filled = int(quantity * fill_rate)
                is_complete = filled == quantity
        else:
            # No volume data, use random fill rate
            fill_rate = random.uniform(self.min_fill_rate, self.max_fill_rate)
            filled = int(quantity * fill_rate)
            is_complete = filled == quantity

        return max(1, filled), is_complete  # At least 1 share


class ExecutionSimulator:
    """
    Comprehensive execution simulator
    Handles commissions, slippage, market impact, and partial fills
    """

    def __init__(
        self,
        commission_model: Optional[CommissionModel] = None,
        slippage_model: Optional[SlippageModel] = None,
        market_impact_model: Optional[MarketImpactModel] = None,
        partial_fill_model: Optional[PartialFillModel] = None,
    ):
        """
        Initialize execution simulator

        Args:
            commission_model: Commission calculation model
            slippage_model: Slippage calculation model
            market_impact_model: Market impact model
            partial_fill_model: Partial fill model
        """
        # Default models
        self.commission_model = commission_model or CommissionModel(
            type=CommissionType.PER_SHARE,
            value=0.005,  # $0.005 per share (typical for retail)
            minimum=1.0,
        )

        self.slippage_model = slippage_model or SlippageModel(
            type=SlippageType.FIXED_BPS,
            value=5.0,  # 5 basis points
        )

        self.market_impact_model = market_impact_model or MarketImpactModel(
            enabled=False,  # Disabled by default
        )

        self.partial_fill_model = partial_fill_model or PartialFillModel(
            enabled=False,  # Disabled by default
        )

    def execute_order(
        self,
        quantity: int,
        price: float,
        is_buy: bool,
        volume: Optional[float] = None,
        volatility: Optional[float] = None,
    ) -> Dict:
        """
        Execute an order with realistic simulation

        Args:
            quantity: Desired quantity
            price: Target price
            is_buy: True for buy, False for sell
            volume: Bar volume (for volume-based calculations)
            volatility: Price volatility (for market impact)

        Returns:
            Dictionary with execution results
        """
        volume = volume or 1000000  # Default volume
        volatility = volatility or 0.02  # Default 2% volatility

        # 1. Simulate partial fill
        filled_quantity, is_complete = self.partial_fill_model.simulate_fill(
            quantity, price, volume
        )

        # 2. Calculate market impact (permanent price move)
        impact_cost, price_with_impact = self.market_impact_model.calculate(
            filled_quantity, price, volume, volatility, is_buy
        )

        # 3. Calculate slippage (temporary price move during execution)
        slippage_amount, final_price = self.slippage_model.calculate(
            filled_quantity, price_with_impact, volume, is_buy
        )

        # 4. Calculate commission
        commission = self.commission_model.calculate(filled_quantity, final_price)

        # 5. Calculate total cost
        gross_cost = filled_quantity * final_price
        total_cost = gross_cost + commission + slippage_amount + impact_cost

        return {
            "requested_quantity": quantity,
            "filled_quantity": filled_quantity,
            "is_complete": is_complete,
            "fill_rate": filled_quantity / quantity if quantity > 0 else 0.0,
            "target_price": price,
            "final_price": final_price,
            "price_with_impact": price_with_impact,
            "commission": commission,
            "slippage": slippage_amount,
            "market_impact": impact_cost,
            "total_execution_cost": commission + slippage_amount + impact_cost,
            "gross_cost": gross_cost,
            "total_cost": total_cost,
        }

    def get_realistic_config(self, account_size: str = "retail") -> "ExecutionSimulator":
        """
        Get realistic configuration for different account sizes

        Args:
            account_size: "retail", "small_institutional", "large_institutional"

        Returns:
            Configured ExecutionSimulator
        """
        if account_size == "retail":
            # Retail trader: higher commissions, moderate slippage
            return ExecutionSimulator(
                commission_model=CommissionModel(
                    type=CommissionType.PER_SHARE,
                    value=0.005,
                    minimum=1.0,
                ),
                slippage_model=SlippageModel(
                    type=SlippageType.FIXED_BPS,
                    value=5.0,  # 5 bps
                ),
                market_impact_model=MarketImpactModel(enabled=False),
                partial_fill_model=PartialFillModel(enabled=False),
            )

        elif account_size == "small_institutional":
            # Small fund: lower commissions, volume-based slippage, some market impact
            return ExecutionSimulator(
                commission_model=CommissionModel(
                    type=CommissionType.PER_SHARE,
                    value=0.002,
                    minimum=10.0,
                ),
                slippage_model=SlippageModel(
                    type=SlippageType.VOLUME_BASED,
                    value=0.02,  # 2% of participation rate
                ),
                market_impact_model=MarketImpactModel(
                    enabled=True,
                    impact_coefficient=0.05,
                ),
                partial_fill_model=PartialFillModel(
                    enabled=True,
                    min_fill_rate=0.8,
                    max_fill_rate=1.0,
                ),
            )

        elif account_size == "large_institutional":
            # Large fund: very low commissions, significant market impact
            return ExecutionSimulator(
                commission_model=CommissionModel(
                    type=CommissionType.PER_SHARE,
                    value=0.001,
                    minimum=50.0,
                ),
                slippage_model=SlippageModel(
                    type=SlippageType.VOLUME_BASED,
                    value=0.05,
                ),
                market_impact_model=MarketImpactModel(
                    enabled=True,
                    impact_coefficient=0.15,
                ),
                partial_fill_model=PartialFillModel(
                    enabled=True,
                    min_fill_rate=0.5,
                    max_fill_rate=0.9,
                ),
            )

        else:
            return self

    @staticmethod
    def create_from_config(config: Dict) -> "ExecutionSimulator":
        """Create ExecutionSimulator from configuration dictionary"""
        commission_config = config.get("commission", {})
        slippage_config = config.get("slippage", {})
        impact_config = config.get("market_impact", {})
        partial_fill_config = config.get("partial_fills", {})

        commission_model = CommissionModel(
            type=CommissionType(commission_config.get("type", "per_share")),
            value=commission_config.get("value", 0.005),
            minimum=commission_config.get("minimum", 1.0),
            maximum=commission_config.get("maximum"),
        )

        slippage_model = SlippageModel(
            type=SlippageType(slippage_config.get("type", "fixed_bps")),
            value=slippage_config.get("value", 5.0),
            is_aggressive=slippage_config.get("is_aggressive", False),
        )

        market_impact_model = MarketImpactModel(
            enabled=impact_config.get("enabled", False),
            impact_coefficient=impact_config.get("impact_coefficient", 0.1),
            temporary_impact_pct=impact_config.get("temporary_impact_pct", 0.5),
        )

        partial_fill_model = PartialFillModel(
            enabled=partial_fill_config.get("enabled", False),
            min_fill_rate=partial_fill_config.get("min_fill_rate", 0.5),
            max_fill_rate=partial_fill_config.get("max_fill_rate", 1.0),
        )

        return ExecutionSimulator(
            commission_model=commission_model,
            slippage_model=slippage_model,
            market_impact_model=market_impact_model,
            partial_fill_model=partial_fill_model,
        )
