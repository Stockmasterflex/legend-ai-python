"""
Double Bottom Pattern Detection

Ported from Patternz FindPatterns.cs FindDoubleBottoms() method (lines 4782-4886)

Includes Adam/Eve variants:
- Adam-Adam: Both bottoms are sharp V-shaped (spike > 30%)
- Eve-Eve: Both bottoms are rounded U-shaped (spike < 30%)
- Adam-Eve: First sharp, second rounded
- Eve-Adam: First rounded, second sharp
"""

import logging
from typing import Any, Dict, List

from app.core.pattern_engine.helpers import PatternData, PatternHelpers

logger = logging.getLogger(__name__)


def find_double_bottoms(
    data: PatternData, helpers: PatternHelpers, find_variants: bool = True
) -> List[Dict[str, Any]]:
    """
    Find Double Bottom patterns with Adam/Eve variants.

    Ported from FindPatterns.cs lines 4782-4886

    Pattern characteristics:
    - Two bottoms at similar price levels (within 0.5%)
    - Separated by 5-126 days
    - Preceded by downtrend
    - Peak between bottoms
    - Confirmed by breaking above peak between bottoms

    Adam vs Eve classification:
    - Spike > 30% = Adam (sharp V)
    - Spike < 30% = Eve (rounded U)

    Args:
        data: PatternData with OHLCV
        helpers: PatternHelpers instance
        find_variants: Whether to classify Adam/Eve variants

    Returns:
        List of detected double bottom patterns
    """
    patterns = []

    # Find bottoms (4-day validation window)
    bottoms = helpers.find_all_bottoms(
        data.lows, data.chart_start_index, data.chart_end_index, trade_days=4
    )

    if len(bottoms) < 2:
        logger.debug(f"Not enough bottoms for double bottom detection: {len(bottoms)}")
        return patterns

    # Find tops (2-day validation window)
    tops = helpers.find_all_tops(
        data.highs, data.chart_start_index, data.chart_end_index, trade_days=2
    )

    if len(tops) == 0:
        logger.debug("No tops found for double bottom detection")
        return patterns

    # Check each pair of bottoms
    for i in range(len(bottoms)):
        for j in range(i + 1, len(bottoms)):
            bottom1_idx = bottoms[i]
            bottom2_idx = bottoms[j]

            # Bottoms must be 5-126 days apart
            bottom_distance = bottom2_idx - bottom1_idx
            if bottom_distance > 126:
                break  # Later bottoms will be even further
            if bottom_distance < 5:
                continue

            bottom1_low = data.lows[bottom1_idx]
            bottom2_low = data.lows[bottom2_idx]

            # Bottoms must be at similar price (within 0.5%)
            if not helpers.check_nearness(bottom1_low, bottom2_low, percent=0.005):
                continue

            # Check for downtrend before first bottom
            has_downtrend = helpers.check_db_downtrend(
                data.highs, data.lows, bottom1_idx, bottom2_idx, slope_threshold=0.2
            )

            if not has_downtrend:
                continue  # Skip if NO strong downtrend (required for pattern)

            # Check confirmation (breakout above peak between bottoms)
            confirmation = helpers.check_confirmation(
                data.opens,
                data.highs,
                data.lows,
                data.closes,
                bottom1_idx + 1,
                bottom2_idx - 1,
                bot_top=-1,
            )

            if confirmation == -1:
                continue  # Pattern failed (broke down)

            # Find peak between bottoms
            peak_idx = bottom1_idx
            for k in range(bottom1_idx, bottom2_idx + 1):
                if data.highs[k] > data.highs[peak_idx]:
                    peak_idx = k

            peak_high = data.highs[peak_idx]

            # Calculate target (measure move)
            depth = peak_high - min(bottom1_low, bottom2_low)
            target = peak_high + depth

            # Calculate entry and stop (matching Patternz)
            entry = peak_high  # Entry at breakout above peak
            stop = min(bottom1_low, bottom2_low) * 0.98  # Stop 2% below lower bottom

            # Classify Adam/Eve if requested
            pattern_name = "DB"
            variant = None

            if find_variants:
                # Calculate spike characteristics
                left_spike, _ = helpers.find_bottom_spike_length(
                    data.highs, data.lows, bottom1_idx, bottom2_idx
                )
                _, right_spike = helpers.find_bottom_spike_length(
                    data.highs, data.lows, bottom1_idx, bottom2_idx
                )

                # Classify based on spikes
                # Spike > 30% = Adam (sharp)
                # Spike < 30% = Eve (rounded)
                left_is_adam = abs(left_spike) > 30
                right_is_adam = abs(right_spike) > 30

                if left_is_adam and right_is_adam:
                    pattern_name = "AADB"
                    variant = "Adam-Adam"
                elif not left_is_adam and not right_is_adam:
                    pattern_name = "EEDB"
                    variant = "Eve-Eve"
                elif left_is_adam and not right_is_adam:
                    pattern_name = "AEDB"
                    variant = "Adam-Eve"
                else:  # not left_is_adam and right_is_adam
                    pattern_name = "EADB"
                    variant = "Eve-Adam"

            # Add confirmation status
            if confirmation == 0:
                pattern_name += "?"  # Pending

            # Calculate risk/reward
            risk = entry - stop
            reward = target - entry
            risk_reward = round(reward / risk, 2) if risk > 0 else 0.0

            patterns.append(
                {
                    "pattern": pattern_name,
                    "start_idx": bottom1_idx,
                    "mid_idx": peak_idx,
                    "end_idx": bottom2_idx,
                    "bottom1": bottom1_low,
                    "bottom2": bottom2_low,
                    "peak": peak_high,
                    "entry": round(entry, 2),
                    "stop": round(stop, 2),
                    "target": round(target, 2),
                    "risk_reward": risk_reward,
                    "depth": depth,
                    "width": bottom_distance,
                    "confirmed": confirmation == 1,
                    "pending": confirmation == 0,
                    "variant": variant,
                    "left_spike": abs(left_spike) if find_variants else 0,
                    "right_spike": abs(right_spike) if find_variants else 0,
                    "confidence": _calculate_db_confidence(
                        bottom_distance,
                        depth,
                        abs(bottom1_low - bottom2_low) / bottom1_low,
                        confirmation == 1,
                    ),
                }
            )

    logger.info(f"Found {len(patterns)} double bottom patterns")
    return patterns


def _calculate_db_confidence(
    width: int, depth: float, bottom_diff_pct: float, confirmed: bool
) -> float:
    """Calculate confidence score for double bottom pattern"""
    confidence = 0.65  # Base confidence

    # Width factor: 20-60 days is ideal
    if 20 <= width <= 60:
        confidence += 0.12
    elif 10 <= width <= 80:
        confidence += 0.08

    # Bottom similarity: closer is better
    if bottom_diff_pct < 0.001:  # Within 0.1%
        confidence += 0.1
    elif bottom_diff_pct < 0.003:  # Within 0.3%
        confidence += 0.08
    elif bottom_diff_pct < 0.005:  # Within 0.5%
        confidence += 0.05

    # Depth factor: deeper is generally better
    if depth > 5.0:
        confidence += 0.08
    elif depth > 3.0:
        confidence += 0.05

    # Confirmation bonus
    if confirmed:
        confidence += 0.1

    return min(1.0, confidence)
