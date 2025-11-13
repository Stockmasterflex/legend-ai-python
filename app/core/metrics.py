"""
Shared indicator/metric helpers used across API surfaces.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
import math


def _to_float_list(values: List[Any]) -> List[float]:
    floats: List[float] = []
    for value in values:
        try:
            floats.append(float(value))
        except Exception:
            floats.append(float("nan"))
    return floats


def sanitize_series(values: List[Any]) -> List[Optional[float]]:
    """Replace NaN/Inf with None for JSON serialization."""
    sanitized: List[Optional[float]] = []
    for value in values:
        try:
            number = float(value)
        except Exception:
            sanitized.append(None)
            continue
        if math.isnan(number) or math.isinf(number):
            sanitized.append(None)
        else:
            sanitized.append(number)
    return sanitized


def last_valid(values: List[Any]) -> Optional[float]:
    """Return the most recent valid float."""
    for value in reversed(values):
        try:
            number = float(value)
        except Exception:
            continue
        if math.isnan(number) or math.isinf(number):
            continue
        return number
    return None


def ma_distances(price: float, ema_value: Optional[float], sma_value: Optional[float]) -> Dict[str, Optional[float]]:
    return {
        "vs_ema21_pct": percentage_distance(price, ema_value),
        "vs_sma50_pct": percentage_distance(price, sma_value),
        "price": round(price, 2) if price else None,
    }


def percentage_distance(price: Optional[float], reference: Optional[float]) -> Optional[float]:
    """Return the percent difference between price and a moving average base."""
    if price is None or reference in (None, 0):
        return None
    return round(((price - reference) / reference) * 100, 2)


def compute_atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> List[float]:
    """Average True Range using simple rolling mean."""
    if not highs or not lows or not closes:
        return []
    trs: List[float] = []
    prev_close = closes[0]
    for idx in range(len(closes)):
        if idx == 0:
            trs.append(highs[idx] - lows[idx])
            continue
        tr = max(
            highs[idx] - lows[idx],
            abs(highs[idx] - prev_close),
            abs(lows[idx] - prev_close),
        )
        trs.append(tr)
        prev_close = closes[idx]
    # Simple moving average of true range
    atr: List[float] = []
    for idx in range(len(trs)):
        window = trs[max(0, idx - period + 1): idx + 1]
        atr.append(sum(window) / len(window))
    return atr


def relative_strength_metrics(closes: List[float], spy_closes: List[float]) -> Dict[str, Any]:
    """Relative strength vs SPY, returning sanitized series and rank."""
    closes_clean = _to_float_list(closes)
    spy_clean = _to_float_list(spy_closes)
    if not closes_clean or not spy_clean:
        return {
            "series": [],
            "rank": None,
            "slope": None,
            "lookback": 0,
            "delta_vs_spy": None,
            "current": None,
        }

    length = min(len(closes_clean), len(spy_clean))
    closes_subset = closes_clean[-length:]
    spy_subset = spy_clean[-length:]

    rs_series: List[Optional[float]] = []
    for idx in range(length):
        base = spy_subset[idx]
        if base == 0 or math.isnan(base) or math.isinf(base):
            rs_series.append(None)
            continue
        ratio = closes_subset[idx] / base if base else None
        rs_series.append(ratio if ratio is not None and math.isfinite(ratio) else None)

    last_value = next((v for v in reversed(rs_series) if v is not None), None)
    slope = None
    window = 20
    valid = [v for v in rs_series if v is not None]
    if len(valid) > window:
        slope = round((valid[-1] - valid[-window]) / window, 4)

    rank = None
    delta_vs_spy = None
    lookback = min(50, length - 1)
    if lookback > 0:
        base_idx = length - lookback - 1
        stock_base = closes_subset[base_idx]
        spy_base = spy_subset[base_idx]
        if stock_base and spy_base:
            stock_ret = closes_subset[-1] / stock_base - 1
            spy_ret = spy_subset[-1] / spy_base - 1
            delta_vs_spy = round((stock_ret - spy_ret) * 100, 2)
            rank = max(1, min(99, round(50 + delta_vs_spy * 1.2)))

    return {
        "series": sanitize_series(rs_series[-150:]),
        "current": round(last_value, 4) if last_value else None,
        "slope": slope,
        "rank": rank,
        "delta_vs_spy": delta_vs_spy,
        "lookback": length,
    }


__all__ = [
    "compute_atr",
    "last_valid",
    "ma_distances",
    "relative_strength_metrics",
    "sanitize_series",
    "percentage_distance",
]
