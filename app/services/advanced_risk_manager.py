"""
Advanced Risk Management Service
Professional position sizing and risk calculation methods
"""
import logging
import math
from typing import Optional, List, Tuple

from app.core.risk_models import (
    KellyResult,
    FixedFractionalResult,
    VolatilityBasedResult,
    RiskMethod,
    VolatilityRegime
)

logger = logging.getLogger(__name__)


class AdvancedRiskManager:
    """
    Advanced position sizing and risk management

    Implements:
    - Kelly Criterion (full, half, quarter)
    - Fixed Fractional sizing
    - Volatility-based sizing (ATR, VIX)
    - Dynamic position scaling
    """

    def __init__(self):
        # Default parameters
        self.DEFAULT_RISK_PCT = 0.02  # 2% per trade
        self.DEFAULT_ATR_PERIOD = 14
        self.DEFAULT_ATR_MULTIPLIER = 2.0

        # VIX thresholds for volatility regimes
        self.VIX_LOW = 15
        self.VIX_NORMAL = 25
        self.VIX_ELEVATED = 35

    # ========================================================================
    # KELLY CRITERION CALCULATOR
    # ========================================================================

    def calculate_kelly_criterion(
        self,
        account_size: float,
        win_rate: float,
        avg_win_dollars: float,
        avg_loss_dollars: float,
        kelly_fraction: str = "half",  # "full", "half", "quarter"
        entry_price: float = None,
        stop_loss: float = None
    ) -> KellyResult:
        """
        Calculate Kelly Criterion position sizing

        Kelly Formula: f* = (p × b - q) / b
        Where:
            p = win probability
            q = loss probability (1 - p)
            b = win/loss ratio (avg win / avg loss)
            f* = optimal fraction of capital to risk

        Args:
            account_size: Total account value
            win_rate: Historical win rate (0-1)
            avg_win_dollars: Average winning trade in $
            avg_loss_dollars: Average losing trade in $ (positive number)
            kelly_fraction: "full", "half", or "quarter" Kelly
            entry_price: Optional entry price for share calculation
            stop_loss: Optional stop loss for position sizing

        Returns:
            KellyResult with detailed calculations
        """

        # Validate inputs
        if not 0 < win_rate < 1:
            raise ValueError("Win rate must be between 0 and 1")
        if avg_win_dollars <= 0 or avg_loss_dollars <= 0:
            raise ValueError("Average win/loss must be positive")
        if account_size <= 0:
            raise ValueError("Account size must be positive")

        # Calculate probabilities
        loss_rate = 1 - win_rate

        # Calculate win/loss ratio
        win_loss_ratio = avg_win_dollars / avg_loss_dollars

        # Kelly percentage: f* = (p × b - q) / b
        kelly_pct = (win_rate * win_loss_ratio - loss_rate) / win_loss_ratio

        # Ensure positive edge
        if kelly_pct <= 0:
            return KellyResult(
                kelly_percentage=kelly_pct * 100,
                kelly_fraction="none",
                adjusted_percentage=0,
                position_size=0,
                position_dollars=0,
                edge=kelly_pct * 100,
                risk_of_ruin=100.0,
                notes=["❌ No positive edge - Kelly suggests no position"]
            )

        # Apply Kelly fraction
        fraction_multiplier = {
            "full": 1.0,
            "half": 0.5,
            "quarter": 0.25
        }.get(kelly_fraction.lower(), 0.5)

        adjusted_kelly_pct = kelly_pct * fraction_multiplier

        # Calculate position size
        position_dollars = account_size * adjusted_kelly_pct

        # If entry and stop provided, calculate shares
        position_size = 0
        if entry_price and stop_loss and entry_price > 0:
            risk_per_share = abs(entry_price - stop_loss)
            if risk_per_share > 0:
                risk_amount = account_size * adjusted_kelly_pct
                position_size = int(risk_amount / risk_per_share)

        # Calculate risk of ruin (simplified)
        # Using formula: RoR ≈ ((1-p)/p)^(E/A) where E=edge, A=account
        edge = win_rate * avg_win_dollars - loss_rate * avg_loss_dollars
        if edge > 0:
            risk_of_ruin = ((loss_rate / win_rate) ** (edge / avg_loss_dollars)) * 100
            risk_of_ruin = min(100, max(0, risk_of_ruin))
        else:
            risk_of_ruin = 100.0

        # Build notes
        notes = []
        if kelly_pct > 0.25:
            notes.append("⚠️ High Kelly % - consider using Kelly/4 or Kelly/2 for safety")
        if kelly_fraction == "full":
            notes.append("⚠️ Full Kelly is aggressive - most pros use Kelly/2")
        if edge > 0:
            notes.append(f"✅ Positive edge: ${edge:.2f} per trade")
        if win_rate > 0.6:
            notes.append(f"✅ Strong win rate: {win_rate*100:.1f}%")
        if win_loss_ratio > 1.5:
            notes.append(f"✅ Good win/loss ratio: {win_loss_ratio:.2f}:1")

        return KellyResult(
            kelly_percentage=kelly_pct * 100,
            kelly_fraction=kelly_fraction,
            adjusted_percentage=adjusted_kelly_pct * 100,
            position_size=position_size,
            position_dollars=position_dollars,
            edge=edge,
            risk_of_ruin=risk_of_ruin,
            notes=notes
        )

    # ========================================================================
    # FIXED FRACTIONAL SIZING
    # ========================================================================

    def calculate_fixed_fractional(
        self,
        account_size: float,
        entry_price: float,
        stop_loss: float,
        risk_percentage: float = 0.02,  # 2% default
        max_positions: int = 10,
        correlation_adjustment: float = 1.0
    ) -> FixedFractionalResult:
        """
        Fixed Fractional Position Sizing

        Risk a fixed percentage (e.g., 1%, 2%) of account per trade.
        Most common method used by professional traders.

        Args:
            account_size: Total account value
            entry_price: Entry price per share
            stop_loss: Stop loss price
            risk_percentage: % of account to risk (default 2%)
            max_positions: Maximum concurrent positions
            correlation_adjustment: Reduce size for correlated positions (0-1)

        Returns:
            FixedFractionalResult with position sizing
        """

        # Validate inputs
        if account_size <= 0:
            raise ValueError("Account size must be positive")
        if entry_price <= 0:
            raise ValueError("Entry price must be positive")
        if not 0.001 <= risk_percentage <= 0.10:
            raise ValueError("Risk percentage must be between 0.1% and 10%")
        if not 0 < correlation_adjustment <= 1:
            raise ValueError("Correlation adjustment must be between 0 and 1")

        # Calculate risk amount
        risk_dollars = account_size * risk_percentage

        # Apply correlation adjustment
        adjusted_risk = risk_dollars * correlation_adjustment

        # Calculate position size
        risk_per_share = abs(entry_price - stop_loss)
        if risk_per_share <= 0:
            raise ValueError("Stop loss must be different from entry price")

        position_size = int(adjusted_risk / risk_per_share)
        position_size = max(1, position_size)  # At least 1 share

        position_dollars = position_size * entry_price

        # Calculate position heat (% of account)
        position_heat = (position_dollars / account_size) * 100

        # Build notes
        notes = []
        if risk_percentage > 0.03:
            notes.append("⚠️ High risk per trade - consider reducing to 2% or less")
        if position_heat > 25:
            notes.append(f"⚠️ Large position: {position_heat:.1f}% of account")
        if position_heat > 50:
            notes.append("❌ Position too large - exceeds 50% of account")
        if correlation_adjustment < 1.0:
            notes.append(f"✅ Position reduced {(1-correlation_adjustment)*100:.0f}% for correlation")

        # Calculate max concurrent positions
        if max_positions > 0:
            notes.append(f"ℹ️ With {max_positions} positions, max total risk: {max_positions * risk_percentage * 100:.0f}%")

        return FixedFractionalResult(
            risk_percentage=risk_percentage * 100,
            account_size=account_size,
            risk_dollars=adjusted_risk,
            position_size=position_size,
            position_dollars=position_dollars,
            max_positions=max_positions,
            position_heat=position_heat,
            notes=notes
        )

    # ========================================================================
    # VOLATILITY-BASED SIZING (ATR)
    # ========================================================================

    def calculate_volatility_based(
        self,
        account_size: float,
        entry_price: float,
        atr: float,
        atr_multiplier: float = 2.0,
        risk_percentage: float = 0.02,
        vix: Optional[float] = None,
        atr_period: int = 14
    ) -> VolatilityBasedResult:
        """
        Volatility-Based Position Sizing using ATR

        Adjusts position size based on volatility:
        - Higher volatility = smaller position
        - Lower volatility = larger position

        Args:
            account_size: Total account value
            entry_price: Entry price per share
            atr: Average True Range (in dollars)
            atr_multiplier: Stop distance in ATR units (default 2.0)
            risk_percentage: % of account to risk
            vix: Optional VIX level for regime detection
            atr_period: ATR calculation period

        Returns:
            VolatilityBasedResult with volatility-adjusted sizing
        """

        # Validate inputs
        if account_size <= 0 or entry_price <= 0 or atr <= 0:
            raise ValueError("Account size, entry price, and ATR must be positive")
        if atr_multiplier <= 0:
            raise ValueError("ATR multiplier must be positive")

        # Calculate stop distance based on ATR
        stop_distance = atr * atr_multiplier

        # Calculate position size using fixed fractional with ATR stop
        risk_dollars = account_size * risk_percentage
        position_size = int(risk_dollars / stop_distance)
        position_size = max(1, position_size)

        position_dollars = position_size * entry_price

        # Determine volatility regime
        volatility_regime = VolatilityRegime.NORMAL
        volatility_adjustment = 1.0

        if vix is not None:
            if vix < self.VIX_LOW:
                volatility_regime = VolatilityRegime.LOW
                volatility_adjustment = 1.2  # Increase size in low vol
            elif vix < self.VIX_NORMAL:
                volatility_regime = VolatilityRegime.NORMAL
                volatility_adjustment = 1.0
            elif vix < self.VIX_ELEVATED:
                volatility_regime = VolatilityRegime.ELEVATED
                volatility_adjustment = 0.75  # Reduce size in elevated vol
            else:
                volatility_regime = VolatilityRegime.HIGH
                volatility_adjustment = 0.5  # Cut size in half in high vol

            # Apply adjustment
            adjusted_position = int(position_size * volatility_adjustment)
            position_size = max(1, adjusted_position)
            position_dollars = position_size * entry_price

        # Build notes
        notes = []
        atr_pct = (atr / entry_price) * 100
        notes.append(f"ℹ️ ATR is {atr_pct:.2f}% of price ({atr_period}-period)")
        notes.append(f"ℹ️ Stop distance: {atr_multiplier}× ATR = ${stop_distance:.2f}")

        if vix is not None:
            notes.append(f"ℹ️ VIX: {vix:.1f} ({volatility_regime.value} volatility)")
            if volatility_adjustment != 1.0:
                notes.append(
                    f"✅ Position adjusted {abs(1-volatility_adjustment)*100:.0f}% for volatility"
                )

        if atr_pct > 5:
            notes.append("⚠️ High volatility - wide stop distance")
        if atr_pct < 2:
            notes.append("✅ Low volatility - tight stop distance")

        return VolatilityBasedResult(
            atr=atr,
            atr_period=atr_period,
            atr_multiplier=atr_multiplier,
            stop_distance=stop_distance,
            position_size=position_size,
            position_dollars=position_dollars,
            volatility_regime=volatility_regime,
            vix=vix,
            volatility_adjustment=volatility_adjustment,
            notes=notes
        )

    # ========================================================================
    # DYNAMIC POSITION SCALING
    # ========================================================================

    def calculate_dynamic_scaling(
        self,
        account_size: float,
        entry_price: float,
        stop_loss: float,
        confidence_score: float,  # 0-100
        market_regime: str = "normal",  # "bull", "normal", "bear"
        base_risk_pct: float = 0.02
    ) -> FixedFractionalResult:
        """
        Dynamic Position Scaling

        Adjusts position size based on:
        - Confidence in the setup
        - Market regime
        - Recent performance

        Args:
            account_size: Total account value
            entry_price: Entry price
            stop_loss: Stop loss price
            confidence_score: Setup confidence (0-100)
            market_regime: "bull", "normal", or "bear"
            base_risk_pct: Base risk percentage

        Returns:
            FixedFractionalResult with dynamically scaled position
        """

        # Validate confidence score
        confidence_score = max(0, min(100, confidence_score))

        # Scale risk based on confidence (0.5x to 1.5x)
        confidence_multiplier = 0.5 + (confidence_score / 100)

        # Adjust for market regime
        regime_multiplier = {
            "bull": 1.2,
            "normal": 1.0,
            "bear": 0.7
        }.get(market_regime.lower(), 1.0)

        # Calculate adjusted risk
        adjusted_risk = base_risk_pct * confidence_multiplier * regime_multiplier

        # Cap at reasonable limits
        adjusted_risk = max(0.005, min(0.05, adjusted_risk))  # 0.5% to 5%

        # Calculate position using fixed fractional
        result = self.calculate_fixed_fractional(
            account_size=account_size,
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_percentage=adjusted_risk
        )

        # Add scaling notes
        result.notes.append(
            f"ℹ️ Confidence scaling: {confidence_score}/100 "
            f"({confidence_multiplier:.2f}x multiplier)"
        )
        result.notes.append(
            f"ℹ️ Market regime: {market_regime} "
            f"({regime_multiplier:.2f}x multiplier)"
        )
        result.notes.append(
            f"ℹ️ Final risk: {adjusted_risk*100:.2f}% "
            f"(base: {base_risk_pct*100:.1f}%)"
        )

        return result

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def compare_methods(
        self,
        account_size: float,
        entry_price: float,
        stop_loss: float,
        win_rate: float,
        avg_win: float,
        avg_loss: float,
        atr: Optional[float] = None,
        vix: Optional[float] = None
    ) -> dict:
        """
        Compare all position sizing methods

        Returns dict with all methods' results for comparison
        """

        results = {}

        # Fixed Fractional (2%)
        try:
            results['fixed_2pct'] = self.calculate_fixed_fractional(
                account_size, entry_price, stop_loss, 0.02
            )
        except Exception as e:
            logger.warning(f"Fixed fractional error: {e}")

        # Fixed Fractional (1%)
        try:
            results['fixed_1pct'] = self.calculate_fixed_fractional(
                account_size, entry_price, stop_loss, 0.01
            )
        except Exception as e:
            logger.warning(f"Fixed fractional 1% error: {e}")

        # Kelly Half
        try:
            results['kelly_half'] = self.calculate_kelly_criterion(
                account_size, win_rate, avg_win, avg_loss, "half",
                entry_price, stop_loss
            )
        except Exception as e:
            logger.warning(f"Kelly half error: {e}")

        # Kelly Quarter
        try:
            results['kelly_quarter'] = self.calculate_kelly_criterion(
                account_size, win_rate, avg_win, avg_loss, "quarter",
                entry_price, stop_loss
            )
        except Exception as e:
            logger.warning(f"Kelly quarter error: {e}")

        # ATR-based (if ATR provided)
        if atr is not None:
            try:
                results['atr_based'] = self.calculate_volatility_based(
                    account_size, entry_price, atr, vix=vix
                )
            except Exception as e:
                logger.warning(f"ATR-based error: {e}")

        return results


# Global singleton
_risk_manager: Optional[AdvancedRiskManager] = None


def get_risk_manager() -> AdvancedRiskManager:
    """Get or create risk manager singleton"""
    global _risk_manager
    if _risk_manager is None:
        _risk_manager = AdvancedRiskManager()
    return _risk_manager
