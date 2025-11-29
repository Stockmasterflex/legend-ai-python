"""
Broadening formations (top, bottom, ascending/descending wedges).
"""
from __future__ import annotations

from typing import Any, Dict, List

import numpy as np


def _risk_reward(entry: float, stop: float, target: float) -> float:
    risk = entry - stop
    reward = target - entry
    if risk <= 0:
        return 0.0
    return round(reward / risk, 2)


def _fit_slope(series: np.ndarray) -> float:
    if len(series) < 2:
        return 0.0
    x = np.arange(len(series))
    try:
        slope, _ = np.polyfit(x, series, 1)
        return float(slope)
    except Exception:
        return 0.0


def _build_pattern(
    name: str,
    start_idx: int,
    end_idx: int,
    upper_last: float,
    lower_last: float,
    confidence: float,
    highs: np.ndarray,
    lows: np.ndarray,
    breakout: str,
    height: float,
    slopes: Dict[str, float],
) -> Dict[str, Any]:
    if breakout == "down":
        entry = lower_last * 0.995
        stop = upper_last * 1.02
        target = entry - height
        current_price = float(lows[end_idx])
    else:
        entry = upper_last * 1.005
        stop = lower_last * 0.98
        target = entry + height
        current_price = float(highs[end_idx])

    return {
        "pattern": name,
        "pattern_type": name,
        "confidence": round(confidence, 3),
        "score": round(confidence * 10, 2),
        "entry": round(entry, 2),
        "stop": round(stop, 2),
        "target": round(target, 2),
        "risk_reward": _risk_reward(entry, stop, target),
        "width": int(end_idx - start_idx),
        "height": round(height, 2),
        "current_price": round(current_price, 2),
        "confirmed": bool((current_price <= entry) if breakout == "down" else (current_price >= entry)),
        "metadata": {
            "breakout_direction": breakout,
            "slopes": slopes,
        },
        "start_idx": int(start_idx),
        "end_idx": int(end_idx),
    }


def _detect_broadening(
    high: np.ndarray,
    low: np.ndarray,
    name: str,
    strict: bool,
) -> Dict[str, Any] | None:
    window = min(len(high), 70)
    if window < 25:
        return None

    highs_win = high[-window:]
    lows_win = low[-window:]
    slope_high = _fit_slope(highs_win)
    slope_low = _fit_slope(lows_win)

    # Diverging requirement: high slope up and low slope down
    if slope_high <= 0 or slope_low >= 0:
        return None
    # Ensure distance expanding
    spread_start = highs_win[0] - lows_win[0]
    spread_end = highs_win[-1] - lows_win[-1]
    if spread_end <= spread_start * (1.05 if strict else 1.02):
        return None

    upper_last = float(highs_win[-1])
    lower_last = float(lows_win[-1])
    height = spread_end
    start_idx = len(high) - window
    end_idx = len(high) - 1
    breakout = "down" if "Top" in name or "Ascending" in name else "up"
    confidence = 0.7 + (0.05 if spread_end > spread_start * 1.1 else 0.0)
    if strict and (abs(slope_high) < 0.01 or abs(slope_low) < 0.01):
        return None

    return _build_pattern(
        name=name,
        start_idx=start_idx,
        end_idx=end_idx,
        upper_last=upper_last,
        lower_last=lower_last,
        confidence=min(confidence, 0.93),
        highs=high,
        lows=low,
        breakout=breakout,
        height=height,
        slopes={"high": slope_high, "low": slope_low},
    )


def find_broadening_top(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    pat = _detect_broadening(high, low, "Broadening Top", strict)
    return [pat] if pat else []


def find_broadening_bottom(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    pat = _detect_broadening(high, low, "Broadening Bottom", strict)
    return [pat] if pat else []


def find_broadening_formations(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """Find all broadening formation variants."""
    results: List[Dict[str, Any]] = []
    for name in ["Broadening Top", "Broadening Bottom", "Ascending Broadening Wedge", "Descending Broadening Wedge"]:
        pat = _detect_broadening(high, low, name, strict)
        if pat:
            results.append(pat)
    return results
