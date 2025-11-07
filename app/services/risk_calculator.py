"""
Risk Calculator and Position Sizing Service
Implements professional risk management for swing traders
"""
import logging
from typing import Optional
from dataclasses import dataclass
import math

logger = logging.getLogger(__name__)


@dataclass
class PositionSize:
    """Position sizing result"""
    account_size: float
    risk_per_trade: float  # 2% of account
    entry_price: float
    stop_loss_price: float
    target_price: float

    # Calculated values
    risk_distance: float  # Distance from entry to stop
    reward_distance: float  # Distance from entry to target
    risk_percentage: float  # Risk as % of entry price
    reward_percentage: float  # Reward as % of entry price

    position_size: int  # Number of shares
    position_size_dollars: float  # Dollar amount to invest

    risk_reward_ratio: float  # Reward/Risk ratio
    expected_value: float  # Expected value per trade in $ using win rate

    kelly_position_size: Optional[int] = None  # Optional Kelly Criterion sizing
    kelly_position_percentage: Optional[float] = None  # % of Kelly to use

    conservative_position_size: Optional[int] = None  # Reduced sizing for safety
    aggressive_position_size: Optional[int] = None  # Increased sizing for confidence

    notes: list = None


class RiskCalculator:
    """Professional position sizing and risk management calculator"""

    # Constants
    DEFAULT_RISK_PERCENT = 0.02  # 2% per trade (standard rule)
    MIN_RISK_PERCENT = 0.01  # 1% minimum
    MAX_RISK_PERCENT = 0.05  # 5% maximum (aggressive)

    def __init__(self):
        pass

    def calculate_position_size(
        self,
        account_size: float,
        entry_price: float,
        stop_loss_price: float,
        target_price: float,
        risk_percentage: float = DEFAULT_RISK_PERCENT,
        win_rate: Optional[float] = None
    ) -> PositionSize:
        """
        Calculate optimal position size using the 2% rule

        The 2% rule: Never risk more than 2% of your account on a single trade.
        This allows you to survive 50 consecutive losses.

        Args:
            account_size: Total trading account size ($)
            entry_price: Entry price for the trade ($)
            stop_loss_price: Stop loss price ($)
            target_price: Target/Take profit price ($)
            risk_percentage: Risk per trade (default 2%, range 1-5%)
            win_rate: Historical win rate (0-1) for Kelly Criterion

        Returns:
            PositionSize with detailed calculations
        """

        # Validate inputs
        if account_size <= 0:
            raise ValueError("Account size must be positive")
        if entry_price <= 0:
            raise ValueError("Entry price must be positive")
        if stop_loss_price <= 0:
            raise ValueError("Stop loss price must be positive")
        if target_price <= 0:
            raise ValueError("Target price must be positive")
        if risk_percentage < self.MIN_RISK_PERCENT or risk_percentage > self.MAX_RISK_PERCENT:
            risk_percentage = self.DEFAULT_RISK_PERCENT

        # Validate entry/stop/target logic
        if stop_loss_price > entry_price and target_price > entry_price:
            # Long position
            if stop_loss_price > target_price:
                raise ValueError("For long positions, stop must be below target")
        elif stop_loss_price < entry_price and target_price < entry_price:
            # Short position
            if stop_loss_price < target_price:
                raise ValueError("For short positions, stop must be above target")
        else:
            # Mixed - check against entry
            pass

        # Calculate distances
        risk_distance = abs(entry_price - stop_loss_price)
        reward_distance = abs(target_price - entry_price)
        risk_percentage_val = (risk_distance / entry_price) * 100
        reward_percentage_val = (reward_distance / entry_price) * 100

        # Calculate allowed risk in dollars (2% of account)
        risk_amount = account_size * risk_percentage

        # Calculate position size (number of shares)
        # Position Size = Risk Amount / Risk Distance (per share)
        position_size = int(risk_amount / risk_distance)

        # Validate position size
        if position_size <= 0:
            logger.warning(f"Position size calculated as {position_size}, using minimum of 1")
            position_size = 1

        position_size_dollars = position_size * entry_price

        # Calculate risk/reward ratio
        if risk_distance > 0:
            risk_reward_ratio = reward_distance / risk_distance
        else:
            risk_reward_ratio = 0

        # Calculate expected value (if win rate known)
        expected_value = 0.0
        if win_rate is not None and win_rate > 0:
            # Expected Value = (Win Rate × Reward) - (Loss Rate × Risk)
            expected_value = (win_rate * reward_distance * position_size) - \
                           ((1 - win_rate) * risk_distance * position_size)

        # Calculate Kelly Criterion sizing (optional)
        kelly_size = None
        kelly_percentage = None
        if win_rate is not None and risk_reward_ratio > 0:
            kelly_size, kelly_percentage = self._kelly_criterion(
                account_size, win_rate, risk_reward_ratio, risk_distance, entry_price
            )

        # Conservative and aggressive sizing
        conservative_size = max(1, int(position_size * 0.75))
        aggressive_size = max(1, int(position_size * 1.25))

        # Build notes
        notes = []
        if account_size < 10000:
            notes.append("⚠️ Small account: Consider micro positions or paper trading")
        if position_size > account_size * 0.1:
            notes.append("⚠️ Large position relative to account - consider reducing size")
        if risk_reward_ratio < 1.0:
            notes.append("⚠️ Risk > Reward - unfavorable R:R ratio")
        if risk_reward_ratio >= 2.0:
            notes.append("✅ Excellent risk:reward ratio (2:1+)")
        if risk_reward_ratio >= 1.5:
            notes.append("✅ Good risk:reward ratio (1.5:1+)")

        return PositionSize(
            account_size=account_size,
            risk_per_trade=risk_amount,
            entry_price=entry_price,
            stop_loss_price=stop_loss_price,
            target_price=target_price,
            risk_distance=risk_distance,
            reward_distance=reward_distance,
            risk_percentage=risk_percentage_val,
            reward_percentage=reward_percentage_val,
            position_size=position_size,
            position_size_dollars=position_size_dollars,
            risk_reward_ratio=risk_reward_ratio,
            expected_value=expected_value,
            kelly_position_size=kelly_size,
            kelly_position_percentage=kelly_percentage,
            conservative_position_size=conservative_size,
            aggressive_position_size=aggressive_size,
            notes=notes
        )

    def _kelly_criterion(
        self,
        account_size: float,
        win_rate: float,
        risk_reward_ratio: float,
        risk_distance: float,
        entry_price: float
    ) -> tuple:
        """
        Calculate Kelly Criterion position sizing

        Kelly % = (Win% × Avg Win) - (Loss% × Avg Loss) / Avg Win

        Result is optimal % of bankroll to risk. However, many traders
        use Kelly/2 or Kelly/4 for safety.

        Args:
            account_size: Account size
            win_rate: Win rate (0-1)
            risk_reward_ratio: Ratio of reward to risk
            risk_distance: $ distance to stop
            entry_price: Entry price

        Returns:
            Tuple of (kelly_position_size, kelly_percentage)
        """
        if win_rate <= 0 or win_rate >= 1 or risk_reward_ratio <= 0:
            return None, None

        try:
            # Kelly formula: f* = (bp - q) / b
            # Where: b = risk/reward ratio, p = win %, q = loss %
            loss_rate = 1 - win_rate

            if risk_reward_ratio == 0:
                return None, None

            # Kelly percentage to risk
            kelly_percent = (win_rate - (loss_rate / risk_reward_ratio)) / risk_reward_ratio

            # Ensure positive
            if kelly_percent <= 0:
                return None, None

            # Most traders use Kelly / 2 for safety
            safe_kelly = kelly_percent / 2

            # Calculate position size based on safe kelly
            risk_amount = account_size * safe_kelly
            position_size = int(risk_amount / risk_distance)

            if position_size <= 0:
                return None, None

            return position_size, safe_kelly * 100

        except Exception as e:
            logger.warning(f"Kelly Criterion calculation error: {e}")
            return None, None

    def calculate_break_even_points(
        self,
        entry_price: float,
        position_size: int,
        commission_per_share: float = 0.01
    ) -> dict:
        """
        Calculate break-even points accounting for commissions

        Args:
            entry_price: Entry price per share
            position_size: Number of shares
            commission_per_share: Commission cost per share (both entry/exit)

        Returns:
            Break-even analysis dictionary
        """
        entry_commission = commission_per_share * position_size
        total_entry_cost = (entry_price * position_size) + entry_commission
        breakeven_price = total_entry_cost / position_size

        return {
            "entry_price": entry_price,
            "breakeven_price": breakeven_price,
            "commission_impact": breakeven_price - entry_price,
            "commission_percentage": ((breakeven_price - entry_price) / entry_price) * 100,
            "notes": f"Need {((breakeven_price - entry_price) / entry_price) * 100:.2f}% profit just to break even after commissions"
        }

    def calculate_account_recovery(
        self,
        starting_account: float,
        current_account: float
    ) -> dict:
        """
        Calculate how much profit needed to recover from losses

        Args:
            starting_account: Starting account size
            current_account: Current account size

        Returns:
            Recovery analysis
        """
        loss_amount = starting_account - current_account
        loss_percentage = (loss_amount / starting_account) * 100

        if loss_percentage <= 0:
            return {
                "status": "profitable",
                "profit_amount": -loss_amount,
                "profit_percentage": -loss_percentage
            }

        # Recovery percentage needed
        recovery_needed = (loss_amount / current_account) * 100

        return {
            "status": "recovering",
            "loss_amount": loss_amount,
            "loss_percentage": loss_percentage,
            "recovery_needed_dollars": loss_amount,
            "recovery_needed_percentage": recovery_needed,
            "warning": f"Need +{recovery_needed:.1f}% gain to recover from {loss_percentage:.1f}% loss"
        }


# Global instance
_risk_calc: Optional[RiskCalculator] = None


def get_risk_calculator() -> RiskCalculator:
    """Get or create risk calculator singleton"""
    global _risk_calc
    if _risk_calc is None:
        _risk_calc = RiskCalculator()
    return _risk_calc
