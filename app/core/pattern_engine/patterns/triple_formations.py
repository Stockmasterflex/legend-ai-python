"""
Triple Tops and Bottoms detection adapted from Patternz FindPatterns.cs.

These routines use helper pivot finders plus nearness checks to keep the
logic faithful while staying lightweight for the Python engine.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np


def _are_near(helpers: Any, prices: List[float], tolerance: float) -> bool:
    """Check that all prices are near each other within a tolerance."""
    if len(prices) < 2:
        return False
    for i in range(len(prices) - 1):
        if not helpers.check_nearness(prices[i], prices[i + 1], percent=tolerance):
            return False
    return True


def _risk_reward(entry: float, stop: float, target: float) -> float:
    risk = entry - stop
    reward = target - entry
    if risk <= 0:
        return 0.0
    return round(reward / risk, 2)


def _build_pattern(
    name: str,
    start_idx: int,
    mid_idx: int,
    end_idx: int,
    entry: float,
    stop: float,
    target: float,
    confidence: float,
    highs: np.ndarray,
    lows: np.ndarray,
    metadata: Dict[str, Any],
) -> Dict[str, Any]:
    height = (
        float(highs[mid_idx] - lows[start_idx])
        if start_idx is not None and mid_idx is not None
        else None
    )
    current_price = float(highs[end_idx]) if end_idx is not None else None
    return {
        "pattern": name,
        "pattern_type": name,
        "confidence": round(confidence, 3),
        "score": round(confidence * 10, 2),
        "entry": round(entry, 2) if entry is not None else None,
        "stop": round(stop, 2) if stop is not None else None,
        "target": round(target, 2) if target is not None else None,
        "risk_reward": _risk_reward(entry, stop, target),
        "width": (
            int(end_idx - start_idx)
            if start_idx is not None and end_idx is not None
            else None
        ),
        "height": round(height, 2) if height is not None else None,
        "current_price": round(current_price, 2) if current_price is not None else None,
        "confirmed": bool(current_price and entry and current_price >= entry),
        "metadata": metadata,
        "start_idx": int(start_idx),
        "mid_idx": int(mid_idx),
        "end_idx": int(end_idx),
    }


def _find_triple(
    pivots: np.ndarray,
    series: np.ndarray,
    helpers: Any,
    tolerance: float,
    bullish: bool,
) -> Tuple[int, int, int]:
    """
    Locate three pivots (tops or bottoms) near the same level.
    Returns indices (p1, p2, p3) or (None, None, None).
    """
    if len(pivots) < 3:
        return None, None, None
    # Use the most recent three pivots for responsiveness
    p1, p2, p3 = pivots[-3], pivots[-2], pivots[-1]
    if not (p1 < p2 < p3):
        return None, None, None

    prices = [series[p1], series[p2], series[p3]]
    if not _are_near(helpers, prices, tolerance):
        return None, None, None

    # For bullish (bottoms) we also want rising bias; for bearish (tops) a slight falling bias.
    if bullish and series[p3] >= series[p1] * (1 + tolerance * 0.4):
        pass  # rising bottoms allowed
    elif bullish and series[p3] < series[p1] * (1 - tolerance):
        return None, None, None
    if (not bullish) and series[p3] <= series[p1] * (1 - tolerance * 0.4):
        pass
    elif (not bullish) and series[p3] > series[p1] * (1 + tolerance):
        return None, None, None

    return p1, p2, p3


def find_triple_bottoms(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """Find Triple Bottom patterns."""
    results: List[Dict[str, Any]] = []
    tolerance = 0.03 if strict else 0.05

    bottoms = helpers.find_all_bottoms(low, trade_days=2)
    tops = helpers.find_all_tops(high, trade_days=2)
    p1, p2, p3 = _find_triple(bottoms, low, helpers, tolerance, bullish=True)
    if p1 is None:
        return results

    # Require peaks between bottoms
    mid_top1 = max(
        [t for t in tops if p1 < t < p2], default=None, key=lambda i: high[i]
    )
    mid_top2 = max(
        [t for t in tops if p2 < t < p3], default=None, key=lambda i: high[i]
    )
    if mid_top1 is None:
        mid_top1 = int(np.argmax(high[p1:p2]) + p1)
    if mid_top2 is None:
        mid_top2 = int(np.argmax(high[p2:p3]) + p2)
    breakout_level = max(high[mid_top1], high[mid_top2])
    base_low = min(low[p1], low[p2], low[p3])
    height = breakout_level - base_low
    entry = breakout_level * (1.005 if strict else 1.003)
    stop = base_low * (0.97 if strict else 0.965)
    target = breakout_level + height

    confidence = 0.72
    if close[-1] >= entry:
        confidence += 0.05
    if low[p3] > low[p1]:
        confidence += 0.03

    results.append(
        _build_pattern(
            "Triple Bottom",
            start_idx=p1,
            mid_idx=p2,
            end_idx=p3,
            entry=entry,
            stop=stop,
            target=target,
            confidence=min(confidence, 0.95),
            highs=high,
            lows=low,
            metadata={
                "breakout_level": breakout_level,
                "swing_bottoms": [int(p1), int(p2), int(p3)],
                "mid_tops": [int(mid_top1), int(mid_top2)],
            },
        )
    )
    return results


def find_triple_tops(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """Find Triple Top patterns."""
    results: List[Dict[str, Any]] = []
    tolerance = 0.03 if strict else 0.05

    tops = helpers.find_all_tops(high, trade_days=2)
    bottoms = helpers.find_all_bottoms(low, trade_days=2)
    p1, p2, p3 = _find_triple(tops, high, helpers, tolerance, bullish=False)
    if p1 is None:
        # Fallback: use highest peak as middle with best neighbors
        head = int(np.argmax(high))
        if head <= 0 or head >= len(high) - 1:
            return results
        left = int(np.argmax(high[:head]))
        right = int(np.argmax(high[head + 1 :]) + head + 1)
        if not (left < head < right):
            return results
        if not _are_near(
            helpers, [high[left], high[head], high[right]], tolerance * 1.2
        ):
            return results
        p1, p2, p3 = left, head, right

    mid_bot1 = min(
        [b for b in bottoms if p1 < b < p2], default=None, key=lambda i: low[i]
    )
    mid_bot2 = min(
        [b for b in bottoms if p2 < b < p3], default=None, key=lambda i: low[i]
    )
    if mid_bot1 is None:
        mid_bot1 = int(np.argmin(low[p1:p2]) + p1)
    if mid_bot2 is None:
        mid_bot2 = int(np.argmin(low[p2:p3]) + p2)

    breakdown_level = min(low[mid_bot1], low[mid_bot2])
    peak_high = max(high[p1], high[p2], high[p3])
    height = peak_high - breakdown_level
    entry = breakdown_level * (0.997 if strict else 0.999)
    stop = peak_high * (1.02 if strict else 1.015)
    target = breakdown_level - height

    confidence = 0.7
    if close[-1] <= entry:
        confidence += 0.05
    if high[p3] < high[p1]:
        confidence += 0.03

    results.append(
        _build_pattern(
            "Triple Top",
            start_idx=p1,
            mid_idx=p2,
            end_idx=p3,
            entry=entry,
            stop=stop,
            target=target,
            confidence=min(confidence, 0.93),
            highs=high,
            lows=low,
            metadata={
                "breakdown_level": breakdown_level,
                "swing_tops": [int(p1), int(p2), int(p3)],
                "mid_bottoms": [int(mid_bot1), int(mid_bot2)],
            },
        )
    )
    return results
