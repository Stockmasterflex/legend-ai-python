"""
Minervini-style VCP (MMU/MMD), High Tight Flag, Flags, Pennants, and Wedges.

These implementations are pragmatic ports of the Patternz logic with
Legend AI heuristics added to keep runtime light while preserving the
key structure/metadata expected by downstream consumers.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np

# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #


def _segment_slope(series: np.ndarray) -> float:
    """Return slope of a series for trend/flag checks."""
    if len(series) < 2:
        return 0.0
    x = np.arange(len(series))
    try:
        slope, _ = np.polyfit(x, series, 1)
        return float(slope)
    except Exception:
        return 0.0


def _risk_reward(entry: float, stop: float, target: float) -> float:
    if entry is None or stop is None or target is None:
        return 0.0
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
    lows: np.ndarray,
    highs: np.ndarray,
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
        "end_idx": int(end_idx),
        "mid_idx": int(mid_idx),
    }


# --------------------------------------------------------------------------- #
# MMU / MMD (Volatility Contraction)
# --------------------------------------------------------------------------- #


def _contraction_sequence(
    highs: np.ndarray, lows: np.ndarray, bottoms: np.ndarray, tops: np.ndarray
) -> Tuple[int, int, int, int]:
    """
    Find a simple contraction sequence Bottom1 -> Top -> Bottom2.
    Returns (b1, top, b2, breakout_idx) or (None, None, None, None).
    """
    if len(bottoms) < 2 or len(tops) < 2:
        return None, None, None, None

    # Use the last two bottoms for recency
    b1, b2 = bottoms[-2], bottoms[-1]
    if b2 <= b1:
        return None, None, None, None

    # Require rising low
    if lows[b2] <= lows[b1] * 1.01:
        return None, None, None, None

    # Choose strongest top between the bottoms
    between_tops = [t for t in tops if b1 < t < b2]
    if not between_tops:
        return None, None, None, None
    top_idx = max(between_tops, key=lambda i: highs[i])

    # Ensure contraction ratio similar to Patternz heuristic
    span1 = highs[top_idx] - lows[b1]
    span2 = highs[top_idx] - lows[b2]
    if span1 <= 0 or span2 <= 0 or (span2 / span1) <= 0.7:
        return None, None, None, None

    breakout_idx = b2 + 1
    return b1, top_idx, b2, breakout_idx


def find_mmu(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """Find Minervini Momentum Up (VCP) patterns."""
    results: List[Dict[str, Any]] = []
    if len(close) < 50:
        return results

    bottoms = helpers.find_all_bottoms(low, trade_days=4)
    tops = helpers.find_all_tops(high, trade_days=4)

    b1, top_idx, b2, breakout_idx = _contraction_sequence(high, low, bottoms, tops)
    if b1 is None:
        return results

    breakout_level = high[top_idx]
    stop = low[b2] * (0.98 if strict else 0.97)
    target = breakout_level + (breakout_level - min(low[b1], low[b2]))
    entry = breakout_level * (1.01 if strict else 1.005)

    current_close = close[-1]
    volume_trend = _segment_slope(volume[-20:]) if len(volume) >= 20 else 0.0
    confidence = 0.72
    if current_close >= entry:
        confidence += 0.05
    if volume_trend > 0:
        confidence += 0.03
    if (low[b2] - low[b1]) / max(low[b1], 1e-6) >= 0.03:
        confidence += 0.02

    metadata = {
        "breakout_level": breakout_level,
        "volume_trend": volume_trend,
        "swing_lows": [int(b1), int(b2)],
        "swing_high": int(top_idx),
    }
    results.append(
        _build_pattern(
            "MMU VCP",
            start_idx=b1,
            mid_idx=top_idx,
            end_idx=len(close) - 1,
            entry=entry,
            stop=stop,
            target=target,
            confidence=min(confidence, 0.97),
            lows=low,
            highs=high,
            metadata=metadata,
        )
    )
    return results


def find_mmd(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """Find Minervini Momentum Down (inverse VCP) patterns."""
    results: List[Dict[str, Any]] = []
    if len(close) < 50:
        return results

    tops = helpers.find_all_tops(high, trade_days=4)
    bottoms = helpers.find_all_bottoms(low, trade_days=4)
    if len(tops) < 2 or len(bottoms) < 1:
        return results

    t1, t2 = tops[-2], tops[-1]
    if t2 <= t1 or high[t2] >= high[t1] * (0.99 if strict else 1.0):
        return results

    between_bottoms = [b for b in bottoms if t1 < b < t2]
    if not between_bottoms:
        return results
    b_idx = min(between_bottoms, key=lambda i: low[i])

    span1 = high[t1] - low[b_idx]
    span2 = high[t2] - low[b_idx]
    if span1 <= 0 or (span2 / span1) <= 0.7:
        return results

    breakdown_level = low[b_idx]
    entry = breakdown_level * (0.995 if strict else 0.999)
    stop = high[t2] * (1.02 if strict else 1.015)
    target = breakdown_level - (high[t1] - breakdown_level)

    current_close = close[-1]
    confidence = 0.7
    if current_close <= entry:
        confidence += 0.05
    if (high[t1] - high[t2]) / max(high[t1], 1e-6) >= 0.02:
        confidence += 0.03

    metadata = {
        "breakdown_level": breakdown_level,
        "swing_tops": [int(t1), int(t2)],
        "swing_bottom": int(b_idx),
    }
    results.append(
        _build_pattern(
            "MMD VCP",
            start_idx=t1,
            mid_idx=b_idx,
            end_idx=len(close) - 1,
            entry=entry,
            stop=stop,
            target=target,
            confidence=min(confidence, 0.95),
            lows=low,
            highs=high,
            metadata=metadata,
        )
    )
    return results


# --------------------------------------------------------------------------- #
# NOTE: HTF, Flags, Pennants, and Wedges have been moved to dedicated files
# --------------------------------------------------------------------------- #
# - find_ht_flag() -> flags.py (more accurate Patternz implementation)
# - find_flags() -> flags.py (correct implementation without buffers)
# - find_pennants() -> flags.py (proper pole height calculation)
# - find_wedges() -> wedges.py (full convergence validation)
#
# The implementations above had discrepancies:
# - Added unnecessary price buffers (0.5%-3%)
# - Used flag/pennant range instead of pole height for targets
# - Missing proper convergence validation for wedges
#
# See ACCURACY_AUDIT.md for full details.
# --------------------------------------------------------------------------- #
