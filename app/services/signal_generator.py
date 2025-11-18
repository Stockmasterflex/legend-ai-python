"""
Signal Generation Module for Paper Trading Automation

Auto-detects entry signals, calculates position size,
sets stop-loss & targets, and generates orders.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from enum import Enum
import logging

from app.services.risk_calculator import RiskCalculator, PositionSize

# Conditional import for PatternScan (only needed for pattern-based signals)
if TYPE_CHECKING:
    from app.models import PatternScan

logger = logging.getLogger(__name__)


class SignalType(Enum):
    """Types of trading signals"""
    PATTERN_BREAKOUT = "pattern_breakout"
    SUPPORT_BOUNCE = "support_bounce"
    RESISTANCE_BREAK = "resistance_break"
    TREND_CONTINUATION = "trend_continuation"
    REVERSAL = "reversal"
    VOLUME_SURGE = "volume_surge"


class SignalStrength(Enum):
    """Signal strength levels"""
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


@dataclass
class TradingSignal:
    """Trading signal with all necessary information"""
    signal_id: str
    ticker: str
    signal_type: SignalType
    strength: SignalStrength

    # Price levels
    entry_price: float
    stop_loss: float
    target_price: float

    # Position sizing
    position_size: PositionSize

    # Signal details
    detected_at: datetime
    pattern_type: Optional[str] = None
    pattern_score: Optional[float] = None
    confidence: float = 0.0

    # Additional context
    timeframe: str = "daily"
    notes: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.notes is None:
            self.notes = []
        if self.metadata is None:
            self.metadata = {}

    @property
    def risk_reward_ratio(self) -> float:
        """Calculate risk/reward ratio"""
        if self.entry_price <= self.stop_loss:
            return 0.0
        risk = self.entry_price - self.stop_loss
        reward = self.target_price - self.entry_price
        return reward / risk if risk > 0 else 0.0

    @property
    def is_valid(self) -> bool:
        """Check if signal is valid for trading"""
        # Must have positive risk/reward
        if self.risk_reward_ratio < 1.5:
            return False

        # Entry must be between stop and target
        if not (self.stop_loss < self.entry_price < self.target_price):
            return False

        # Must have minimum confidence
        if self.confidence < 0.5:
            return False

        return True


class SignalGenerator:
    """
    Generate trading signals from pattern detection and technical analysis
    """

    def __init__(self, risk_calculator: RiskCalculator):
        self.risk_calculator = risk_calculator
        self.logger = logging.getLogger(__name__)

    def generate_signal_from_pattern(
        self,
        pattern_scan: "PatternScan",
        account_size: float,
        risk_per_trade_pct: float = 2.0,
        current_price: Optional[float] = None
    ) -> Optional[TradingSignal]:
        """
        Generate a trading signal from a pattern scan result

        Args:
            pattern_scan: Pattern detection result
            account_size: Trading account size
            risk_per_trade_pct: Risk percentage per trade (default 2%)
            current_price: Current market price (optional, uses entry_price if not provided)

        Returns:
            TradingSignal if valid, None otherwise
        """
        try:
            # Use current price or pattern entry price
            entry = current_price or pattern_scan.entry_price
            stop = pattern_scan.stop_price
            target = pattern_scan.target_price

            # Validate price levels
            if not (stop < entry < target):
                self.logger.warning(
                    f"Invalid price levels for {pattern_scan.ticker.symbol}: "
                    f"stop={stop}, entry={entry}, target={target}"
                )
                return None

            # Calculate position size
            position_size = self.risk_calculator.calculate_position_size(
                account_size=account_size,
                entry_price=entry,
                stop_loss_price=stop,
                target_price=target,
                risk_percentage=risk_per_trade_pct
            )

            # Determine signal strength based on pattern score
            strength = self._calculate_signal_strength(
                pattern_scan.score,
                pattern_scan.risk_reward_ratio
            )

            # Map pattern type to signal type
            signal_type = self._pattern_to_signal_type(pattern_scan.pattern_type)

            # Generate unique signal ID
            signal_id = f"{pattern_scan.ticker.symbol}_{pattern_scan.pattern_type}_{int(datetime.now().timestamp())}"

            # Create signal
            signal = TradingSignal(
                signal_id=signal_id,
                ticker=pattern_scan.ticker.symbol,
                signal_type=signal_type,
                strength=strength,
                entry_price=entry,
                stop_loss=stop,
                target_price=target,
                position_size=position_size,
                detected_at=datetime.now(),
                pattern_type=pattern_scan.pattern_type,
                pattern_score=pattern_scan.score,
                confidence=pattern_scan.score / 100.0,  # Convert 0-100 to 0-1
                notes=[
                    f"Pattern: {pattern_scan.pattern_type}",
                    f"Score: {pattern_scan.score}",
                    f"R/R: {pattern_scan.risk_reward_ratio:.2f}",
                    f"Position: {position_size.position_size} shares (${position_size.position_size_dollars:,.2f})"
                ],
                metadata={
                    "pattern_id": pattern_scan.id,
                    "sector": pattern_scan.ticker.sector,
                    "industry": pattern_scan.ticker.industry,
                    "scanned_at": pattern_scan.scanned_at.isoformat()
                }
            )

            # Validate signal before returning
            if not signal.is_valid:
                self.logger.warning(f"Generated signal for {signal.ticker} is invalid")
                return None

            self.logger.info(
                f"Generated {strength.value} signal for {signal.ticker}: "
                f"{signal_type.value} @ ${entry:.2f}"
            )

            return signal

        except Exception as e:
            self.logger.error(f"Error generating signal: {e}", exc_info=True)
            return None

    def generate_signals_batch(
        self,
        pattern_scans: List["PatternScan"],
        account_size: float,
        risk_per_trade_pct: float = 2.0,
        min_strength: SignalStrength = SignalStrength.MODERATE
    ) -> List[TradingSignal]:
        """
        Generate signals from multiple pattern scans

        Args:
            pattern_scans: List of pattern detection results
            account_size: Trading account size
            risk_per_trade_pct: Risk percentage per trade
            min_strength: Minimum signal strength to include

        Returns:
            List of valid trading signals
        """
        signals = []

        for pattern in pattern_scans:
            signal = self.generate_signal_from_pattern(
                pattern_scan=pattern,
                account_size=account_size,
                risk_per_trade_pct=risk_per_trade_pct
            )

            if signal and self._meets_minimum_strength(signal.strength, min_strength):
                signals.append(signal)

        # Sort by strength and confidence
        signals.sort(
            key=lambda s: (self._strength_to_score(s.strength), s.confidence),
            reverse=True
        )

        self.logger.info(f"Generated {len(signals)} signals from {len(pattern_scans)} patterns")
        return signals

    def _calculate_signal_strength(
        self,
        pattern_score: float,
        risk_reward_ratio: float
    ) -> SignalStrength:
        """
        Calculate signal strength based on pattern score and R/R ratio

        Pattern Score (0-100) + R/R ratio combined scoring:
        - Very Strong: Score >= 80 AND R/R >= 3.0
        - Strong: Score >= 70 AND R/R >= 2.5
        - Moderate: Score >= 60 AND R/R >= 2.0
        - Weak: Everything else
        """
        if pattern_score >= 80 and risk_reward_ratio >= 3.0:
            return SignalStrength.VERY_STRONG
        elif pattern_score >= 70 and risk_reward_ratio >= 2.5:
            return SignalStrength.STRONG
        elif pattern_score >= 60 and risk_reward_ratio >= 2.0:
            return SignalStrength.MODERATE
        else:
            return SignalStrength.WEAK

    def _pattern_to_signal_type(self, pattern_type: str) -> SignalType:
        """Map pattern type to signal type"""
        pattern_lower = pattern_type.lower()

        if "vcp" in pattern_lower or "cup" in pattern_lower or "handle" in pattern_lower:
            return SignalType.PATTERN_BREAKOUT
        elif "support" in pattern_lower or "bounce" in pattern_lower:
            return SignalType.SUPPORT_BOUNCE
        elif "resistance" in pattern_lower or "breakout" in pattern_lower:
            return SignalType.RESISTANCE_BREAK
        elif "trend" in pattern_lower or "continuation" in pattern_lower:
            return SignalType.TREND_CONTINUATION
        elif "reversal" in pattern_lower or "bottom" in pattern_lower:
            return SignalType.REVERSAL
        elif "volume" in pattern_lower:
            return SignalType.VOLUME_SURGE
        else:
            return SignalType.PATTERN_BREAKOUT

    def _strength_to_score(self, strength: SignalStrength) -> int:
        """Convert strength to numeric score for sorting"""
        scores = {
            SignalStrength.WEAK: 1,
            SignalStrength.MODERATE: 2,
            SignalStrength.STRONG: 3,
            SignalStrength.VERY_STRONG: 4
        }
        return scores.get(strength, 0)

    def _meets_minimum_strength(
        self,
        signal_strength: SignalStrength,
        min_strength: SignalStrength
    ) -> bool:
        """Check if signal meets minimum strength requirement"""
        return self._strength_to_score(signal_strength) >= self._strength_to_score(min_strength)


def create_manual_signal(
    ticker: str,
    entry_price: float,
    stop_loss: float,
    target_price: float,
    account_size: float,
    risk_per_trade_pct: float = 2.0,
    signal_type: SignalType = SignalType.PATTERN_BREAKOUT,
    notes: Optional[List[str]] = None
) -> Optional[TradingSignal]:
    """
    Create a manual trading signal (for testing or manual entry)

    Args:
        ticker: Stock ticker symbol
        entry_price: Entry price
        stop_loss: Stop loss price
        target_price: Target price
        account_size: Trading account size
        risk_per_trade_pct: Risk percentage per trade
        signal_type: Type of signal
        notes: Additional notes

    Returns:
        TradingSignal if valid, None otherwise
    """
    try:
        # Validate price levels
        if not (stop_loss < entry_price < target_price):
            logger.error(
                f"Invalid price levels: stop={stop_loss}, entry={entry_price}, target={target_price}"
            )
            return None

        # Calculate position size
        risk_calc = RiskCalculator()
        position_size = risk_calc.calculate_position_size(
            account_size=account_size,
            entry_price=entry_price,
            stop_loss_price=stop_loss,
            target_price=target_price,
            risk_percentage=risk_per_trade_pct
        )

        # Calculate confidence based on R/R ratio
        rr_ratio = (target_price - entry_price) / (entry_price - stop_loss)
        # Map R/R ratio to confidence: 2:1 = 0.6, 3:1 = 1.0
        confidence = min((rr_ratio - 1.0) / 2.0 + 0.1, 1.0) if rr_ratio >= 1.5 else 0.0

        # Determine strength
        if rr_ratio >= 3.0:
            strength = SignalStrength.VERY_STRONG
        elif rr_ratio >= 2.5:
            strength = SignalStrength.STRONG
        elif rr_ratio >= 2.0:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK

        # Generate signal ID
        signal_id = f"{ticker}_MANUAL_{int(datetime.now().timestamp())}"

        signal = TradingSignal(
            signal_id=signal_id,
            ticker=ticker,
            signal_type=signal_type,
            strength=strength,
            entry_price=entry_price,
            stop_loss=stop_loss,
            target_price=target_price,
            position_size=position_size,
            detected_at=datetime.now(),
            pattern_type="Manual Entry",
            confidence=confidence,
            notes=notes or [],
            metadata={"manual": True}
        )

        if signal.is_valid:
            return signal
        else:
            logger.warning(f"Manual signal for {ticker} is invalid")
            return None

    except Exception as e:
        logger.error(f"Error creating manual signal: {e}", exc_info=True)
        return None
