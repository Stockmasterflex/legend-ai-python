"""
MTF Entry Timing Optimizer
Optimizes entry timing using lower timeframes while respecting higher timeframe direction
"""
import logging
import pandas as pd
import numpy as np
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime

from app.core.mtf_analyzer import TimeframeData

logger = logging.getLogger(__name__)


@dataclass
class EntrySignal:
    """Entry signal with timing and price levels"""
    signal_type: str  # "buy", "sell", "wait"
    confidence: float  # 0-1
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward_ratio: float

    # Entry context
    entry_timeframe: str  # Timeframe for entry (e.g., "1H")
    direction_timeframe: str  # Timeframe for direction (e.g., "1D")
    entry_reason: str

    # Timing
    timestamp: datetime
    valid_until: Optional[datetime] = None

    # Confirmation flags
    higher_tf_confirmed: bool = False
    volume_confirmed: bool = False
    pattern_confirmed: bool = False


@dataclass
class EntryTiming:
    """Entry timing analysis result"""
    optimal_entry_tf: str  # Best timeframe for entry
    current_signal: EntrySignal

    # Alternative entries
    alternative_entries: List[EntrySignal]

    # Timing insights
    timing_notes: List[str]
    wait_for: List[str]  # Conditions to wait for


class MTFEntryTimingOptimizer:
    """
    MTF Entry Timing Optimizer

    Strategy:
    - Higher timeframes (Daily, Weekly, Monthly) determine DIRECTION
    - Lower timeframes (4H, 1H) determine ENTRY TIMING
    - Entry on pullbacks to support on lower TF in direction of higher TF
    """

    # Entry timeframes (used for precise entry timing)
    ENTRY_TIMEFRAMES = ["1hour", "4hour"]

    # Direction timeframes (used for trend direction)
    DIRECTION_TIMEFRAMES = ["1day", "1week", "1month"]

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def optimize_entry(
        self,
        ticker: str,
        timeframe_data: Dict[str, TimeframeData],
        data_by_timeframe: Dict[str, pd.DataFrame]
    ) -> EntryTiming:
        """
        Optimize entry timing across timeframes

        Args:
            ticker: Stock symbol
            timeframe_data: Dictionary of TimeframeData
            data_by_timeframe: Dictionary of OHLCV DataFrames

        Returns:
            EntryTiming with optimal entry signal
        """
        # Determine direction from higher timeframes
        direction = self._get_higher_tf_direction(timeframe_data)

        # Find optimal entry on lower timeframes
        entry_signals = []

        for entry_tf in self.ENTRY_TIMEFRAMES:
            if entry_tf not in timeframe_data or entry_tf not in data_by_timeframe:
                continue

            tf_data = timeframe_data[entry_tf]
            ohlcv = data_by_timeframe[entry_tf]

            if ohlcv is None or len(ohlcv) < 20:
                continue

            # Generate entry signal for this timeframe
            signal = self._generate_entry_signal(
                ticker, entry_tf, tf_data, ohlcv, direction, timeframe_data
            )

            if signal:
                entry_signals.append(signal)

        # Select best entry signal
        if entry_signals:
            # Sort by confidence
            entry_signals.sort(key=lambda s: s.confidence, reverse=True)
            best_signal = entry_signals[0]
            alternative_signals = entry_signals[1:] if len(entry_signals) > 1 else []
        else:
            # No clear entry signal - create "wait" signal
            best_signal = self._create_wait_signal(ticker, direction)
            alternative_signals = []

        # Determine optimal entry timeframe
        optimal_tf = best_signal.entry_timeframe

        # Generate timing notes and wait conditions
        timing_notes, wait_for = self._generate_timing_insights(
            timeframe_data, best_signal, direction
        )

        return EntryTiming(
            optimal_entry_tf=optimal_tf,
            current_signal=best_signal,
            alternative_entries=alternative_signals,
            timing_notes=timing_notes,
            wait_for=wait_for
        )

    def _get_higher_tf_direction(
        self,
        timeframe_data: Dict[str, TimeframeData]
    ) -> str:
        """
        Get consensus direction from higher timeframes

        Returns: "up", "down", or "sideways"
        """
        trends = []
        weights = []

        for tf_key in self.DIRECTION_TIMEFRAMES:
            if tf_key in timeframe_data:
                tf_data = timeframe_data[tf_key]
                trends.append(tf_data.trend_direction)
                weights.append(tf_data.weight)

        if not trends:
            return "sideways"

        # Weighted voting
        up_weight = sum(w for t, w in zip(trends, weights) if t == "up")
        down_weight = sum(w for t, w in zip(trends, weights) if t == "down")

        if up_weight > down_weight * 1.2:
            return "up"
        elif down_weight > up_weight * 1.2:
            return "down"
        else:
            return "sideways"

    def _generate_entry_signal(
        self,
        ticker: str,
        entry_tf: str,
        tf_data: TimeframeData,
        ohlcv: pd.DataFrame,
        higher_tf_direction: str,
        all_tf_data: Dict[str, TimeframeData]
    ) -> Optional[EntrySignal]:
        """
        Generate entry signal for a specific timeframe

        Strategy:
        - For LONG: Wait for pullback to support on lower TF when higher TF is up
        - For SHORT: Wait for rally to resistance on lower TF when higher TF is down
        """
        current_price = float(ohlcv['close'].iloc[-1])

        # Only generate signals if lower TF aligns with higher TF direction
        if higher_tf_direction == "up":
            # Looking for LONG entry
            signal_type = "buy"

            # Check if we're in a good entry zone
            if tf_data.nearest_support:
                # Calculate distance to support
                dist_to_support = (current_price - tf_data.nearest_support) / current_price

                # Good entry if within 2% of support
                if 0 < dist_to_support <= 0.02:
                    entry_price = current_price
                    stop_loss = tf_data.nearest_support * 0.98  # 2% below support
                    take_profit = tf_data.nearest_resistance if tf_data.nearest_resistance else current_price * 1.05

                    rr_ratio = (take_profit - entry_price) / (entry_price - stop_loss)

                    # Confidence based on alignment and setup quality
                    confidence = self._calculate_entry_confidence(
                        tf_data, higher_tf_direction, dist_to_support, all_tf_data
                    )

                    # Only signal if R:R is good
                    if rr_ratio >= 1.5:
                        return EntrySignal(
                            signal_type=signal_type,
                            confidence=confidence,
                            entry_price=entry_price,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            risk_reward_ratio=rr_ratio,
                            entry_timeframe=tf_data.label,
                            direction_timeframe="Higher TFs",
                            entry_reason=f"Pullback to support on {tf_data.label} in uptrend",
                            timestamp=datetime.now(),
                            higher_tf_confirmed=(higher_tf_direction == "up"),
                            volume_confirmed=(tf_data.volume_trend == "increasing"),
                            pattern_confirmed=tf_data.pattern_detected
                        )

        elif higher_tf_direction == "down":
            # Looking for SHORT entry
            signal_type = "sell"

            if tf_data.nearest_resistance:
                # Calculate distance to resistance
                dist_to_resistance = (tf_data.nearest_resistance - current_price) / current_price

                # Good entry if within 2% of resistance
                if 0 < dist_to_resistance <= 0.02:
                    entry_price = current_price
                    stop_loss = tf_data.nearest_resistance * 1.02  # 2% above resistance
                    take_profit = tf_data.nearest_support if tf_data.nearest_support else current_price * 0.95

                    rr_ratio = (entry_price - take_profit) / (stop_loss - entry_price)

                    confidence = self._calculate_entry_confidence(
                        tf_data, higher_tf_direction, dist_to_resistance, all_tf_data
                    )

                    if rr_ratio >= 1.5:
                        return EntrySignal(
                            signal_type=signal_type,
                            confidence=confidence,
                            entry_price=entry_price,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            risk_reward_ratio=rr_ratio,
                            entry_timeframe=tf_data.label,
                            direction_timeframe="Higher TFs",
                            entry_reason=f"Rally to resistance on {tf_data.label} in downtrend",
                            timestamp=datetime.now(),
                            higher_tf_confirmed=(higher_tf_direction == "down"),
                            volume_confirmed=(tf_data.volume_trend == "increasing"),
                            pattern_confirmed=tf_data.pattern_detected
                        )

        return None

    def _calculate_entry_confidence(
        self,
        tf_data: TimeframeData,
        higher_tf_direction: str,
        dist_to_level: float,
        all_tf_data: Dict[str, TimeframeData]
    ) -> float:
        """
        Calculate confidence for entry signal (0-1)

        Higher confidence when:
        - Closer to support/resistance
        - Volume increasing
        - RSI not overbought/oversold
        - All timeframes aligned
        """
        confidence = 0.5  # Base confidence

        # Distance to level (closer = better)
        if dist_to_level <= 0.01:
            confidence += 0.2
        elif dist_to_level <= 0.02:
            confidence += 0.1

        # Volume confirmation
        if tf_data.volume_trend == "increasing":
            confidence += 0.15

        # RSI confirmation (not overbought/oversold)
        if tf_data.rsi:
            if higher_tf_direction == "up":
                if 40 <= tf_data.rsi <= 60:
                    confidence += 0.10
                elif tf_data.rsi > 70:
                    confidence -= 0.10  # Overbought
            else:
                if 40 <= tf_data.rsi <= 60:
                    confidence += 0.10
                elif tf_data.rsi < 30:
                    confidence -= 0.10  # Oversold

        # Pattern confirmation
        if tf_data.pattern_detected:
            confidence += 0.10

        # Check alignment with all timeframes
        aligned_tfs = 0
        total_tfs = 0

        for other_tf_key, other_tf_data in all_tf_data.items():
            if other_tf_data.trend_direction == higher_tf_direction:
                aligned_tfs += 1
            total_tfs += 1

        if total_tfs > 0:
            alignment_ratio = aligned_tfs / total_tfs
            confidence += (alignment_ratio - 0.5) * 0.2  # +/- 0.1 based on alignment

        return max(0.0, min(1.0, confidence))

    def _create_wait_signal(self, ticker: str, direction: str) -> EntrySignal:
        """Create a 'wait' signal when no clear entry exists"""
        return EntrySignal(
            signal_type="wait",
            confidence=0.0,
            entry_price=0.0,
            stop_loss=0.0,
            take_profit=0.0,
            risk_reward_ratio=0.0,
            entry_timeframe="N/A",
            direction_timeframe="N/A",
            entry_reason=f"No clear entry point yet. Higher TF direction: {direction.upper()}",
            timestamp=datetime.now(),
            higher_tf_confirmed=False,
            volume_confirmed=False,
            pattern_confirmed=False
        )

    def _generate_timing_insights(
        self,
        timeframe_data: Dict[str, TimeframeData],
        signal: EntrySignal,
        direction: str
    ) -> Tuple[List[str], List[str]]:
        """
        Generate timing insights and wait conditions

        Returns:
            Tuple of (timing_notes, wait_for_conditions)
        """
        timing_notes = []
        wait_for = []

        # Signal quality notes
        if signal.signal_type == "buy":
            timing_notes.append(f"🎯 LONG entry signal on {signal.entry_timeframe}")
            timing_notes.append(f"   Entry: ${signal.entry_price:.2f}")
            timing_notes.append(f"   Stop: ${signal.stop_loss:.2f}")
            timing_notes.append(f"   Target: ${signal.take_profit:.2f}")
            timing_notes.append(f"   R:R = {signal.risk_reward_ratio:.2f}")
            timing_notes.append(f"   Confidence: {signal.confidence:.0%}")

        elif signal.signal_type == "sell":
            timing_notes.append(f"🎯 SHORT entry signal on {signal.entry_timeframe}")
            timing_notes.append(f"   Entry: ${signal.entry_price:.2f}")
            timing_notes.append(f"   Stop: ${signal.stop_loss:.2f}")
            timing_notes.append(f"   Target: ${signal.take_profit:.2f}")
            timing_notes.append(f"   R:R = {signal.risk_reward_ratio:.2f}")
            timing_notes.append(f"   Confidence: {signal.confidence:.0%}")

        else:
            timing_notes.append(f"⏸️ WAIT - No clear entry yet")
            timing_notes.append(f"   Higher TF Direction: {direction.upper()}")

        # Confirmation status
        if not signal.higher_tf_confirmed:
            wait_for.append("Higher timeframe trend confirmation")

        if not signal.volume_confirmed:
            wait_for.append("Volume increase on breakout")

        if not signal.pattern_confirmed:
            wait_for.append("Pattern completion")

        # Timeframe-specific insights
        for tf_key in ["1hour", "4hour"]:
            if tf_key in timeframe_data:
                tf_data = timeframe_data[tf_key]

                if direction == "up" and tf_data.trend_direction == "down":
                    wait_for.append(f"{tf_data.label} pullback completion")

                elif direction == "down" and tf_data.trend_direction == "up":
                    wait_for.append(f"{tf_data.label} rally completion")

        # RSI considerations
        hour_1 = timeframe_data.get("1hour")
        if hour_1 and hour_1.rsi:
            if direction == "up" and hour_1.rsi > 70:
                wait_for.append("1H RSI to cool down from overbought")
            elif direction == "down" and hour_1.rsi < 30:
                wait_for.append("1H RSI to bounce from oversold")

        return timing_notes, wait_for
