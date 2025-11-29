"""
Rectangle consolidation pattern detection (bullish and bearish breakouts).
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


def _build_pattern(
    name: str,
    start_idx: int,
    end_idx: int,
    entry: float,
    stop: float,
    target: float,
    confidence: float,
    highs: np.ndarray,
    lows: np.ndarray,
    metadata: Dict[str, Any],
) -> Dict[str, Any]:
    width = int(end_idx - start_idx)
    height = float(metadata["resistance"] - metadata["support"])
    current_price = float(highs[end_idx]) if end_idx is not None else None
    return {
        "pattern": name,
        "pattern_type": name,
        "confidence": round(confidence, 3),
        "score": round(confidence * 10, 2),
        "entry": round(entry, 2),
        "stop": round(stop, 2),
        "target": round(target, 2),
        "risk_reward": _risk_reward(entry, stop, target),
        "width": width,
        "height": round(height, 2),
        "current_price": round(current_price, 2) if current_price is not None else None,
        "confirmed": bool(
            current_price
            and (
                (current_price >= entry) if "Bull" in name else (current_price <= entry)
            )
        ),
        "metadata": metadata,
        "start_idx": int(start_idx),
        "end_idx": int(end_idx),
    }


def _find_levels(high: np.ndarray, low: np.ndarray, helpers: Any, tolerance: float):
    tops = helpers.find_all_tops(high, trade_days=2)
    bottoms = helpers.find_all_bottoms(low, trade_days=2)
    if len(tops) < 2 or len(bottoms) < 2:
        return None, None

    top_prices = [high[i] for i in tops[-4:]] or [np.max(high)]
    bottom_prices = [low[i] for i in bottoms[-4:]] or [np.min(low)]
    resistance = float(np.median(top_prices))
    support = float(np.median(bottom_prices))
    if support <= 0 or resistance <= support:
        return None, None

    if not helpers.check_nearness(resistance, max(top_prices), percent=tolerance):
        return None, None
    if not helpers.check_nearness(support, min(bottom_prices), percent=tolerance):
        return None, None

    return support, resistance


def find_rectangles(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """Find Rectangle consolidation patterns (bullish and bearish scenarios)."""
    results: List[Dict[str, Any]] = []
    if len(close) < 12:
        return results

    tolerance = 0.02 if strict else 0.03
    support, resistance = _find_levels(high, low, helpers, tolerance)
    if support is None:
        return results

    height = resistance - support
    start_idx = max(0, len(close) - 60)
    end_idx = len(close) - 1

    bull_entry = resistance * (1.005 if strict else 1.003)
    bull_stop = support * 0.98
    bull_target = resistance + height
    confidence = 0.7 + (0.05 if close[-1] > (support + height * 0.7) else 0.0)
    results.append(
        _build_pattern(
            "Rectangle Bullish",
            start_idx=start_idx,
            end_idx=end_idx,
            entry=bull_entry,
            stop=bull_stop,
            target=bull_target,
            confidence=min(confidence, 0.92),
            highs=high,
            lows=low,
            metadata={"support": support, "resistance": resistance, "height": height},
        )
    )

    bear_entry = support * (0.997 if strict else 0.999)
    bear_stop = resistance * 1.02
    bear_target = support - height
    confidence_bear = 0.7 + (0.05 if close[-1] < (support + height * 0.3) else 0.0)
    results.append(
        _build_pattern(
            "Rectangle Bearish",
            start_idx=start_idx,
            end_idx=end_idx,
            entry=bear_entry,
            stop=bear_stop,
            target=bear_target,
            confidence=min(confidence_bear, 0.92),
            highs=high,
            lows=low,
            metadata={"support": support, "resistance": resistance, "height": height},
        )
    )

    return results
