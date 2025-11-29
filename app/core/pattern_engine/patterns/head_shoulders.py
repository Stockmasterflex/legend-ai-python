"""
Head & Shoulders Top and Bottom detection adapted from Patternz.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np


def _risk_reward(entry: float, stop: float, target: float) -> float:
    risk = entry - stop
    reward = target - entry
    if risk <= 0:
        return 0.0
    return round(reward / risk, 2)


def _are_near(helpers: Any, a: float, b: float, tolerance: float) -> bool:
    return helpers.check_nearness(a, b, percent=tolerance)


def _neckline(low_segment: np.ndarray) -> float:
    return float(np.mean(low_segment)) if len(low_segment) else 0.0


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
        "confirmed": bool(
            current_price
            and entry
            and (
                (current_price <= entry) if "Top" in name else (current_price >= entry)
            )
        ),
        "metadata": metadata,
        "start_idx": int(start_idx),
        "mid_idx": int(mid_idx),
        "end_idx": int(end_idx),
    }


def _find_shoulder_head(
    pivots: np.ndarray,
    series: np.ndarray,
    helpers: Any,
    tolerance: float,
    inverted: bool,
) -> Tuple[int, int, int]:
    """
    Locate left shoulder, head, right shoulder indices using pivot arrays.
    Inverted=False for tops, True for bottoms.
    """
    if len(pivots) < 3:
        # Fallback: derive from raw series using extrema
        head = int(np.argmin(series)) if inverted else int(np.argmax(series))
        if head <= 0 or head >= len(series) - 1:
            return None, None, None
        ls = (
            int(np.argmax(series[:head]))
            if inverted is False
            else int(np.argmin(series[:head]))
        )
        rs_segment = series[head + 1 :]
        if len(rs_segment) == 0:
            return None, None, None
        rs = int(
            (np.argmax(rs_segment) if not inverted else np.argmin(rs_segment))
            + head
            + 1
        )
        if not (ls < head < rs):
            return None, None, None
    else:
        # Use the most recent three pivots
        ls, head, rs = pivots[-3], pivots[-2], pivots[-1]
        if not (ls < head < rs):
            return None, None, None

    ls_val, head_val, rs_val = series[ls], series[head], series[rs]
    if inverted:
        # Head should be lower
        if head_val >= min(ls_val, rs_val):
            return None, None, None
        if not _are_near(helpers, ls_val, rs_val, tolerance):
            return None, None, None
    else:
        # Head higher
        if head_val <= max(ls_val, rs_val):
            return None, None, None
        if not _are_near(helpers, ls_val, rs_val, tolerance):
            return None, None, None

    return ls, head, rs


def find_head_shoulders_top(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """Find Head & Shoulders Top patterns."""
    results: List[Dict[str, Any]] = []
    tolerance = 0.03 if strict else 0.05
    tops = helpers.find_all_tops(high, trade_days=4)
    bottoms = helpers.find_all_bottoms(low, trade_days=3)
    ls, head, rs = _find_shoulder_head(tops, high, helpers, tolerance, inverted=False)
    if ls is None:
        return results

    trough_left = min(
        [b for b in bottoms if ls < b < head], default=None, key=lambda i: low[i]
    )
    trough_right = min(
        [b for b in bottoms if head < b < rs], default=None, key=lambda i: low[i]
    )
    if trough_left is None:
        trough_left = int(np.argmin(low[ls:head]) + ls)
    if trough_right is None:
        trough_right = int(np.argmin(low[head:rs]) + head)

    neckline_pts = [low[trough_left], low[trough_right]]
    neckline = _neckline(np.array(neckline_pts))
    slope = (neckline_pts[1] - neckline_pts[0]) / max(rs - ls, 1)
    if strict and abs(slope) > 0.01 * neckline:
        return results

    entry = neckline * (0.995 if strict else 0.998)
    stop = high[head] * (1.02 if strict else 1.015)
    target = neckline - (high[head] - neckline)
    confidence = 0.72
    if close[-1] <= entry:
        confidence += 0.05
    if volume is not None and len(volume) >= head + 1:
        vol_head = volume[head]
        vol_ls = volume[ls] if ls < len(volume) else vol_head
        vol_rs = volume[rs] if rs < len(volume) else vol_head
        if vol_rs > vol_head * 0.9:
            confidence += 0.02
        if vol_head < vol_ls:
            confidence += 0.01

    results.append(
        _build_pattern(
            "Head & Shoulders Top",
            start_idx=ls,
            mid_idx=head,
            end_idx=rs,
            entry=entry,
            stop=stop,
            target=target,
            confidence=min(confidence, 0.95),
            highs=high,
            lows=low,
            metadata={
                "neckline": neckline,
                "neckline_slope": slope,
                "shoulders": [int(ls), int(rs)],
                "head": int(head),
                "troughs": [int(trough_left), int(trough_right)],
            },
        )
    )
    return results


def find_head_shoulders_bottom(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """Find Head & Shoulders Bottom (Inverse) patterns."""
    results: List[Dict[str, Any]] = []
    tolerance = 0.03 if strict else 0.05
    bottoms = helpers.find_all_bottoms(low, trade_days=4)
    tops = helpers.find_all_tops(high, trade_days=3)
    ls, head, rs = _find_shoulder_head(bottoms, low, helpers, tolerance, inverted=True)
    if ls is None:
        return results

    peak_left = max(
        [t for t in tops if ls < t < head], default=None, key=lambda i: high[i]
    )
    peak_right = max(
        [t for t in tops if head < t < rs], default=None, key=lambda i: high[i]
    )
    if peak_left is None:
        peak_left = int(np.argmax(high[ls:head]) + ls)
    if peak_right is None:
        peak_right = int(np.argmax(high[head:rs]) + head)

    neckline_pts = [high[peak_left], high[peak_right]]
    neckline = _neckline(np.array(neckline_pts))
    slope = (neckline_pts[1] - neckline_pts[0]) / max(rs - ls, 1)
    if strict and abs(slope) > 0.01 * neckline:
        return results

    entry = neckline * (1.005 if strict else 1.002)
    stop = low[head] * (0.98 if strict else 0.985)
    target = neckline + (neckline - low[head])
    confidence = 0.72
    if close[-1] >= entry:
        confidence += 0.05
    if volume is not None and len(volume) >= head + 1:
        vol_head = volume[head]
        vol_ls = volume[ls] if ls < len(volume) else vol_head
        vol_rs = volume[rs] if rs < len(volume) else vol_head
        if vol_rs > vol_head * 1.05:
            confidence += 0.02
        if vol_head < vol_ls:
            confidence += 0.01

    results.append(
        _build_pattern(
            "Head & Shoulders Bottom",
            start_idx=ls,
            mid_idx=head,
            end_idx=rs,
            entry=entry,
            stop=stop,
            target=target,
            confidence=min(confidence, 0.95),
            highs=high,
            lows=low,
            metadata={
                "neckline": neckline,
                "neckline_slope": slope,
                "shoulders": [int(ls), int(rs)],
                "head": int(head),
                "peaks": [int(peak_left), int(peak_right)],
            },
        )
    )
    return results
