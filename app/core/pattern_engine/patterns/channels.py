"""
Channel pattern detection (ascending, descending, horizontal).
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
    slope: float,
    highs: np.ndarray,
    lows: np.ndarray,
    breakout: str,
    confidence: float,
) -> Dict[str, Any]:
    height = upper_last - lower_last
    if breakout == "up":
        entry = upper_last * 1.005
        stop = lower_last * 0.98
        target = entry + height
    else:
        entry = lower_last * 0.995
        stop = upper_last * 1.02
        target = entry - height

    current_price = float(highs[end_idx]) if breakout == "up" else float(lows[end_idx])
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
        "confirmed": bool(
            (current_price >= entry) if breakout == "up" else (current_price <= entry)
        ),
        "metadata": {
            "slope": slope,
            "breakout_direction": breakout,
            "upper_last": upper_last,
            "lower_last": lower_last,
        },
        "start_idx": int(start_idx),
        "end_idx": int(end_idx),
    }


def _detect_channel(
    high: np.ndarray,
    low: np.ndarray,
    name: str,
    slope_sign: int,
    strict: bool,
) -> Dict[str, Any] | None:
    window = min(len(high), 60)
    if window < 20:
        return None

    high_seg = high[-window:]
    low_seg = low[-window:]
    slope_high = _fit_slope(high_seg)
    slope_low = _fit_slope(low_seg)

    if slope_sign == 1 and (slope_high <= 0 or slope_low <= 0):
        return None
    if slope_sign == -1 and (slope_high >= 0 or slope_low >= 0):
        return None
    if slope_sign == 0 and (abs(slope_high) > 0.02 or abs(slope_low) > 0.02):
        return None

    # Require roughly parallel slopes
    if slope_low == 0:
        return None
    ratio = abs(slope_high / slope_low)
    if ratio < 0.5 or ratio > 2.0:
        return None

    upper_last = float(high_seg[-1])
    lower_last = float(low_seg[-1])
    start_idx = len(high) - window
    end_idx = len(high) - 1
    breakout = "up" if slope_sign >= 0 else "down"
    confidence = 0.68 + (0.05 if ratio < 1.2 else 0.0)
    if strict and abs(slope_high - slope_low) > 0.02:
        return None
    return _build_pattern(
        name,
        start_idx,
        end_idx,
        upper_last,
        lower_last,
        slope_high,
        high,
        low,
        breakout,
        confidence,
    )


def find_channels(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """Find ascending, descending, and horizontal channels."""
    results: List[Dict[str, Any]] = []
    asc = _detect_channel(high, low, "Ascending Channel", slope_sign=1, strict=strict)
    desc = _detect_channel(
        high, low, "Descending Channel", slope_sign=-1, strict=strict
    )
    flat = _detect_channel(high, low, "Horizontal Channel", slope_sign=0, strict=strict)
    for pat in (asc, desc, flat):
        if pat:
            results.append(pat)
    return results


def find_ascending_channel(*args, **kwargs) -> List[Dict[str, Any]]:
    return [
        pat
        for pat in find_channels(*args, **kwargs)
        if pat["pattern"] == "Ascending Channel"
    ]


def find_descending_channel(*args, **kwargs) -> List[Dict[str, Any]]:
    return [
        pat
        for pat in find_channels(*args, **kwargs)
        if pat["pattern"] == "Descending Channel"
    ]


def find_horizontal_channel(*args, **kwargs) -> List[Dict[str, Any]]:
    return [
        pat
        for pat in find_channels(*args, **kwargs)
        if pat["pattern"] == "Horizontal Channel"
    ]
