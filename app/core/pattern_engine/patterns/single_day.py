"""
Single-Day Pattern Detection

Ported from Patternz FindPatterns.cs single-bar routines:
- Inside/Outside Day
- NR4 / NR7
- Wide Range Up/Down
- Spike Up/Down
- 3-Bar
- Close Price Reversal Up/Down
- Opening Close Reversal Up/Down
"""
from typing import List, Dict, Any
import logging

import numpy as np

from app.core.pattern_engine.helpers import PatternData, PatternHelpers

logger = logging.getLogger(__name__)


def find_single_day_patterns(
    data: PatternData,
    helpers: PatternHelpers
) -> List[Dict[str, Any]]:
    """Run all single-day detectors in one pass."""
    patterns: List[Dict[str, Any]] = []
    patterns.extend(find_inside_day(data, helpers))
    patterns.extend(find_outside_day(data, helpers))
    patterns.extend(find_nr4(data, helpers))
    patterns.extend(find_nr7(data, helpers))
    patterns.extend(find_wide_range_up(data, helpers))
    patterns.extend(find_wide_range_down(data, helpers))
    patterns.extend(find_spike_up(data, helpers))
    patterns.extend(find_spike_down(data, helpers))
    patterns.extend(find_three_bar(data, helpers))
    patterns.extend(find_cpr_up(data, helpers))
    patterns.extend(find_cpr_down(data, helpers))
    patterns.extend(find_ocr_up(data, helpers))
    patterns.extend(find_ocr_down(data, helpers))
    logger.info(f"Found {len(patterns)} single-day patterns")
    return patterns


def find_inside_day(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Inside Day: current bar trades inside prior day's range."""
    patterns: List[Dict[str, Any]] = []
    start = data.chart_start_index
    end = min(data.chart_end_index, len(data.highs) - 2)

    for i in range(start, end + 1):
        prev_range = _bar_range(data.highs, data.lows, i)
        curr_range = _bar_range(data.highs, data.lows, i + 1)
        if prev_range <= 0 or curr_range <= 0:
            continue

        if data.highs[i] > data.highs[i + 1] and data.lows[i] < data.lows[i + 1]:
            ratio = curr_range / prev_range
            patterns.append({
                'pattern': 'Inside Day',
                'start_idx': i,
                'end_idx': i + 1,
                'range_ratio': ratio,
                'confirmed': True,
                'pending': False,
                'direction': 'neutral',
                'confidence': _contraction_confidence(ratio, 4)
            })

    return patterns


def find_outside_day(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Outside Day: current bar engulfs prior day's range."""
    patterns: List[Dict[str, Any]] = []
    start = data.chart_start_index
    end = min(data.chart_end_index, len(data.highs) - 2)

    for i in range(start, end + 1):
        first_range = _bar_range(data.highs, data.lows, i)
        second_range = _bar_range(data.highs, data.lows, i + 1)
        if first_range <= 0 or second_range <= 0:
            continue

        if data.highs[i] < data.highs[i + 1] and data.lows[i] > data.lows[i + 1]:
            ratio = second_range / first_range
            patterns.append({
                'pattern': 'Outside Day',
                'start_idx': i,
                'end_idx': i + 1,
                'range_ratio': ratio,
                'confirmed': True,
                'pending': False,
                'direction': 'neutral',
                'confidence': _expansion_confidence(ratio, 2)
            })

    return patterns


def find_nr4(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Narrow Range 4: smallest range of the last four sessions."""
    patterns: List[Dict[str, Any]] = []
    start = max(data.chart_start_index + 3, 3)
    end = data.chart_end_index

    for i in range(start, end + 1):
        cur_range = _bar_range(data.highs, data.lows, i)
        window = [_bar_range(data.highs, data.lows, j) for j in range(i - 3, i)]
        if cur_range <= 0 or any(r <= 0 for r in window):
            continue
        if all(cur_range < r for r in window):
            avg_prev = float(np.mean(window))
            patterns.append({
                'pattern': 'NR4',
                'start_idx': i - 3,
                'end_idx': i,
                'range_ratio': cur_range / avg_prev,
                'confirmed': True,
                'pending': False,
                'direction': 'neutral',
                'confidence': _contraction_confidence(cur_range / avg_prev, 4)
            })

    return patterns


def find_nr7(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Narrow Range 7: smallest range of the last seven sessions."""
    patterns: List[Dict[str, Any]] = []
    start = max(data.chart_start_index + 6, 6)
    end = data.chart_end_index

    for i in range(start, end + 1):
        cur_range = _bar_range(data.highs, data.lows, i)
        window = [_bar_range(data.highs, data.lows, j) for j in range(i - 6, i)]
        if cur_range <= 0 or any(r <= 0 for r in window):
            continue
        if all(cur_range < r for r in window):
            avg_prev = float(np.mean(window))
            patterns.append({
                'pattern': 'NR7',
                'start_idx': i - 6,
                'end_idx': i,
                'range_ratio': cur_range / avg_prev,
                'confirmed': True,
                'pending': False,
                'direction': 'neutral',
                'confidence': _contraction_confidence(cur_range / avg_prev, 7)
            })

    return patterns


def find_wide_range_up(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Wide Range Up: large bullish bar after a downtrend."""
    patterns: List[Dict[str, Any]] = []
    start = max(data.chart_start_index + 2, 2)
    end = data.chart_end_index

    for i in range(start, end + 1):
        rng = _bar_range(data.highs, data.lows, i)
        if rng <= 0:
            continue

        top_quarter = data.highs[i] - rng * 0.25
        if data.closes[i] <= top_quarter:
            continue

        avg_range = helpers.wide_range_average(data.highs, data.lows, i - 1)
        if avg_range <= 0 or rng <= 3 * avg_range:
            continue

        trend = helpers.hl_regression(data.highs, data.lows, i - 1, lookback=5)
        if trend != -1:
            continue

        patterns.append({
            'pattern': 'Wide Range Up',
            'start_idx': i,
            'end_idx': i,
            'range': rng,
            'avg_range': avg_range,
            'direction': 'bullish',
            'confirmed': True,
            'pending': False,
            'confidence': _wide_range_confidence(rng, avg_range, _close_position(data.highs, data.lows, data.closes, i))
        })

    return patterns


def find_wide_range_down(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Wide Range Down: large bearish bar after an uptrend."""
    patterns: List[Dict[str, Any]] = []
    start = max(data.chart_start_index + 2, 2)
    end = data.chart_end_index

    for i in range(start, end + 1):
        rng = _bar_range(data.highs, data.lows, i)
        if rng <= 0:
            continue

        bottom_quarter = data.lows[i] + rng * 0.25
        if data.closes[i] >= bottom_quarter:
            continue

        avg_range = helpers.wide_range_average(data.highs, data.lows, i - 1)
        if avg_range <= 0 or rng <= 3 * avg_range:
            continue

        trend = helpers.hl_regression(data.highs, data.lows, i - 1, lookback=5)
        if trend != 1:
            continue

        patterns.append({
            'pattern': 'Wide Range Down',
            'start_idx': i,
            'end_idx': i,
            'range': rng,
            'avg_range': avg_range,
            'direction': 'bearish',
            'confirmed': True,
            'pending': False,
            'confidence': _wide_range_confidence(rng, avg_range, 1 - _close_position(data.highs, data.lows, data.closes, i))
        })

    return patterns


def find_spike_down(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Spike Down: isolated bar with deep tail that closes near the top."""
    patterns: List[Dict[str, Any]] = []
    start = max(data.chart_start_index + 1, 1)
    end = min(data.chart_end_index, len(data.highs) - 2)

    for i in range(start, end + 1):
        rng = _bar_range(data.highs, data.lows, i)
        if rng <= 0:
            continue

        half = rng * 0.5
        if not (data.lows[i - 1] > data.highs[i] - half and data.lows[i + 1] > data.highs[i] - half):
            continue

        if data.closes[i] <= data.highs[i] - rng * 0.25:
            continue

        avg_range = helpers.wide_range_average(data.highs, data.lows, i - 1)
        if avg_range <= 0 or rng <= avg_range:
            continue

        trend = helpers.hl_regression(data.highs, data.lows, i - 1, lookback=5)
        if trend != -1:
            continue

        patterns.append({
            'pattern': 'Spike Down',
            'start_idx': i,
            'end_idx': i,
            'range': rng,
            'avg_range': avg_range,
            'direction': 'bullish',
            'confirmed': True,
            'pending': False,
            'confidence': _spike_confidence(rng, avg_range, data.opens[i], data.closes[i])
        })

    return patterns


def find_spike_up(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Spike Up: isolated bar with upper shadow that closes near the low."""
    patterns: List[Dict[str, Any]] = []
    start = max(data.chart_start_index + 1, 1)
    end = min(data.chart_end_index, len(data.highs) - 2)

    for i in range(start, end + 1):
        rng = _bar_range(data.highs, data.lows, i)
        if rng <= 0:
            continue

        half = rng * 0.5
        if not (data.highs[i - 1] < data.lows[i] + half and data.highs[i + 1] < data.lows[i] + half):
            continue

        if data.closes[i] >= data.lows[i] + rng * 0.25:
            continue

        avg_range = helpers.wide_range_average(data.highs, data.lows, i - 1)
        if avg_range <= 0 or rng <= avg_range:
            continue

        trend = helpers.hl_regression(data.highs, data.lows, i - 1, lookback=5)
        if trend != 1:
            continue

        patterns.append({
            'pattern': 'Spike Up',
            'start_idx': i,
            'end_idx': i,
            'range': rng,
            'avg_range': avg_range,
            'direction': 'bearish',
            'confirmed': True,
            'pending': False,
            'confidence': _spike_confidence(rng, avg_range, data.opens[i], data.closes[i])
        })

    return patterns


def find_three_bar(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """3-Bar bullish reversal pattern."""
    patterns: List[Dict[str, Any]] = []
    start = max(data.chart_start_index + 1, 1)
    end = min(data.chart_end_index - 2, len(data.highs) - 3)

    for i in range(start, end + 1):
        if data.closes[i - 1] <= data.closes[i]:
            continue

        if not (data.lows[i + 1] < data.lows[i] and data.lows[i + 1] < data.lows[i + 2]):
            continue

        if helpers.strict_patterns:
            breakout = data.closes[i + 2] > data.highs[i] and data.closes[i + 2] > data.highs[i + 1]
        else:
            breakout = data.closes[i + 2] > data.highs[i + 1]

        if breakout:
            rng = _bar_range(data.highs, data.lows, i + 2)
            patterns.append({
                'pattern': '3-Bar',
                'start_idx': i,
                'end_idx': i + 2,
                'direction': 'bullish',
                'confirmed': True,
                'pending': False,
                'confidence': _breakout_confidence(data.closes[i + 2], data.highs[i + 1], rng)
            })

    return patterns


def find_cpr_down(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Close Price Reversal Down (bullish reversal after decline)."""
    patterns: List[Dict[str, Any]] = []
    start = max(data.chart_start_index + 1, 1)
    end = data.chart_end_index

    for i in range(start, end + 1):
        rng = _bar_range(data.highs, data.lows, i)
        if rng <= 0:
            continue

        quarter = rng * 0.25
        if not (data.opens[i] < data.lows[i] + quarter and data.closes[i] > data.highs[i] - quarter):
            continue

        if data.closes[i - 1] >= data.closes[i]:
            continue

        trend = helpers.hl_regression(data.highs, data.lows, i - 1, lookback=5)
        if trend != -1:
            continue

        patterns.append({
            'pattern': 'CPRD',
            'start_idx': i,
            'end_idx': i,
            'direction': 'bullish',
            'confirmed': True,
            'pending': False,
            'confidence': _reversal_confidence(data.opens[i], data.closes[i], rng)
        })

    return patterns


def find_cpr_up(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Close Price Reversal Up (bearish reversal after advance)."""
    patterns: List[Dict[str, Any]] = []
    start = max(data.chart_start_index + 1, 1)
    end = data.chart_end_index

    for i in range(start, end + 1):
        rng = _bar_range(data.highs, data.lows, i)
        if rng <= 0:
            continue

        quarter = rng * 0.25
        if not (data.opens[i] > data.highs[i] - quarter and data.closes[i] < data.lows[i] + quarter):
            continue

        if data.closes[i - 1] <= data.closes[i]:
            continue

        trend = helpers.hl_regression(data.highs, data.lows, i - 1, lookback=5)
        if trend != 1:
            continue

        patterns.append({
            'pattern': 'CPRU',
            'start_idx': i,
            'end_idx': i,
            'direction': 'bearish',
            'confirmed': True,
            'pending': False,
            'confidence': _reversal_confidence(data.opens[i], data.closes[i], rng)
        })

    return patterns


def find_ocr_down(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Opening Close Reversal Down (bullish response after decline)."""
    patterns: List[Dict[str, Any]] = []
    start = max(data.chart_start_index + 2, 2)
    end = data.chart_end_index

    for i in range(start, end + 1):
        rng = _bar_range(data.highs, data.lows, i)
        if rng <= 0:
            continue

        quarter = rng * 0.25
        if not (data.opens[i] < data.lows[i] + quarter and data.closes[i] > data.highs[i] - quarter):
            continue

        if data.closes[i] >= data.closes[i - 1]:
            continue

        trend = helpers.hl_regression(data.highs, data.lows, i - 1, lookback=5)
        if trend != -1:
            continue

        patterns.append({
            'pattern': 'OCRD',
            'start_idx': i,
            'end_idx': i,
            'direction': 'bullish',
            'confirmed': True,
            'pending': False,
            'confidence': _reversal_confidence(data.opens[i], data.closes[i], rng)
        })

    return patterns


def find_ocr_up(data: PatternData, helpers: PatternHelpers) -> List[Dict[str, Any]]:
    """Opening Close Reversal Up (bearish response after advance)."""
    patterns: List[Dict[str, Any]] = []
    start = max(data.chart_start_index + 2, 2)
    end = data.chart_end_index

    for i in range(start, end + 1):
        rng = _bar_range(data.highs, data.lows, i)
        if rng <= 0:
            continue

        quarter = rng * 0.25
        if not (data.opens[i] > data.highs[i] - quarter and data.closes[i] < data.lows[i] + quarter):
            continue

        if data.closes[i] <= data.closes[i - 1]:
            continue

        trend = helpers.hl_regression(data.highs, data.lows, i - 1, lookback=5)
        if trend != 1:
            continue

        patterns.append({
            'pattern': 'OCRU',
            'start_idx': i,
            'end_idx': i,
            'direction': 'bearish',
            'confirmed': True,
            'pending': False,
            'confidence': _reversal_confidence(data.opens[i], data.closes[i], rng)
        })

    return patterns


def _bar_range(highs: np.ndarray, lows: np.ndarray, idx: int) -> float:
    return float(highs[idx] - lows[idx])


def _close_position(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, idx: int) -> float:
    rng = _bar_range(highs, lows, idx)
    if rng <= 0:
        return 0.5
    return float((closes[idx] - lows[idx]) / rng)


def _clamp_confidence(value: float) -> float:
    return float(max(0.0, min(1.0, value)))


def _contraction_confidence(ratio: float, window: int) -> float:
    return _clamp_confidence(0.7 - min(ratio, 2.0) * 0.3 + min(window, 7) * 0.01)


def _expansion_confidence(ratio: float, window: int) -> float:
    return _clamp_confidence(0.55 + min(max(ratio - 1.0, 0.0), 2.5) * 0.18 + min(window, 7) * 0.01)


def _wide_range_confidence(rng: float, avg_range: float, close_pos: float) -> float:
    stretch = rng / avg_range if avg_range > 0 else 1.0
    return _clamp_confidence(0.6 + min(stretch / 3.0, 2.0) * 0.2 + (close_pos - 0.5) * 0.2)


def _spike_confidence(rng: float, avg_range: float, open_price: float, close_price: float) -> float:
    stretch = rng / avg_range if avg_range > 0 else 1.0
    body = abs(close_price - open_price) / rng if rng > 0 else 0.0
    shadow = 1.0 - min(body, 1.0)
    return _clamp_confidence(0.55 + min(stretch - 1.0, 2.0) * 0.1 + shadow * 0.15)


def _breakout_confidence(close_price: float, trigger: float, rng: float) -> float:
    if rng <= 0:
        return 0.5
    distance = (close_price - trigger) / rng
    return _clamp_confidence(0.6 + min(distance, 1.5) * 0.2)


def _reversal_confidence(open_price: float, close_price: float, rng: float) -> float:
    if rng <= 0:
        return 0.5
    body = abs(close_price - open_price) / rng
    return _clamp_confidence(0.55 + min(body, 1.0) * 0.3)
