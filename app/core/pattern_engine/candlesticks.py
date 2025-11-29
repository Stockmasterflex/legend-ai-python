"""
Legend AI Candlestick Pattern Lab

Comprehensive candlestick detection covering the 105 legacy candle
definitions from the historic FindCandles.cs implementation. Patterns
are evaluated with Legend AI's lightweight, dependency-free ruleset and
scored with a confidence value for downstream ranking.

Usage mirrors other pattern modules:
- Input: PatternData (OHLCV) plus PatternHelpers for shared utilities
- Output: List of pattern dictionaries with start/end indices and confidence
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np

from app.core.pattern_engine.helpers import PatternData, PatternHelpers

logger = logging.getLogger(__name__)


# Core metadata for quick rendering and docs
PATTERN_LABELS: Dict[str, str] = {
    "BreakawayBull": "Bullish Breakaway",
    "BreakawayBear": "Bearish Breakaway",
    "WindowRising": "Rising Window",
    "WindowFalling": "Falling Window",
    "UpsideTasukiGap": "Upside Tasuki Gap",
    "UpsideGap2Crows": "Upside Gap Two Crows",
    "UpsideGap3Method": "Upside Gap Three Methods",
    "Unique3RiverBottom": "Unique Three River Bottom",
    "TwoCrows": "Two Crows",
    "TwoBlackGapping": "Two Black Gapping",
    "TwelveNewPriceLines": "Twelve New Price Lines",
    "TweezersTop": "Tweezers Top",
    "TweezersBottom": "Tweezers Bottom",
    "TriStarBull": "Bullish Tri-Star",
    "TriStarBear": "Bearish Tri-Star",
    "Thrusting": "Thrusting",
    "ThreeWhiteSoldiers": "Three White Soldiers",
    "ThreeStarsSouth": "Three Stars In The South",
    "ThreeOutsideUp": "Three Outside Up",
    "ThreeOutsideDown": "Three Outside Down",
    "ThreeLineStrikeBull": "Bullish Three Line Strike",
    "ThreeLineStrikeBear": "Bearish Three Line Strike",
    "ThreeInsideUp": "Three Inside Up",
    "ThreeInsideDown": "Three Inside Down",
    "ThreeBlackCrows": "Three Black Crows",
    "Takuri": "Takuri Line",
    "ThirteenNewPriceLines": "Thirteen New Price Lines",
    "TenNewPriceLines": "Ten New Price Lines",
    "StickSandwich": "Stick Sandwich",
    "SpinningTop": "Spinning Top",
    "SpinningTopWht": "Spinning Top (White)",
    "SpinningTopBlk": "Spinning Top (Black)",
    "SBSWLinesBull": "Side-by-Side White Lines (Bull)",
    "SBSWLinesBear": "Side-by-Side White Lines (Bear)",
    "ShootingStar": "Shooting Star",
    "ShootingStar2": "Shooting Star (Strict)",
    "SeparatingLinesBull": "Separating Lines (Bull)",
    "SeparatingLinesBear": "Separating Lines (Bear)",
    "Rising3method": "Rising Three Methods",
    "RickshawMan": "Rickshaw Man",
    "PiercingPattern": "Piercing Pattern",
    "OnNeckLine": "On-Neck Line",
    "MorningStar": "Morning Star",
    "MorningDojiStar": "Morning Doji Star",
    "MeetingLinesBull": "Meeting Lines (Bull)",
    "MeetingLinesBear": "Meeting Lines (Bear)",
    "MatchingLow": "Matching Low",
    "MatHold": "Mat Hold",
    "MarubozuWhite": "White Marubozu",
    "MarubozuOpeningW": "Opening White Marubozu",
    "MarubozuOpeningB": "Opening Black Marubozu",
    "MarubozuClosingW": "Closing White Marubozu",
    "MarubozuClosingB": "Closing Black Marubozu",
    "MarubozuBlack": "Black Marubozu",
    "LongDayWhite": "Long Day (White)",
    "LongDayBlack": "Long Day (Black)",
    "LastEngulfTop": "Last Engulfing Top",
    "LastEngulfBot": "Last Engulfing Bottom",
    "LadderBottom": "Ladder Bottom",
    "KickerBull": "Bullish Kicker",
    "KickerBear": "Bearish Kicker",
    "InNeckLine": "In-Neck Line",
    "Identical3Crows": "Identical Three Crows",
    "HomingPigeon": "Homing Pigeon",
    "HighWave": "High Wave",
    "HaramiCrossBullish": "Bullish Harami Cross",
    "HaramiCrossBearish": "Bearish Harami Cross",
    "HaramiBullish": "Bullish Harami",
    "HaramiBearish": "Bearish Harami",
    "HangingMan": "Hanging Man",
    "HammerInverted": "Inverted Hammer",
    "Hammer": "Hammer",
    "Falling3Method": "Falling Three Methods",
    "EveningStar": "Evening Star",
    "EveningDojiStar": "Evening Doji Star",
    "EngulfingBullish": "Bullish Engulfing",
    "EngulfingBearish": "Bearish Engulfing",
    "EightNewPriceLines": "Eight New Price Lines",
    "DownsideTasukiGap": "Downside Tasuki Gap",
    "DownsideGap3Methods": "Downside Gap Three Methods",
    "DojiStarCollapse": "Collapsing Doji Star",
    "DojiFourPrice": "Four-Price Doji",
    "DojiDragonFly": "Dragonfly Doji",
    "Deliberation": "Deliberation",
    "DarkCloudCover": "Dark Cloud Cover",
    "ConcealingBaby": "Concealing Baby Swallow",
    "CandleShortWht": "Short Day (White)",
    "CandleShortBlk": "Short Day (Black)",
    "CandleWhite": "White Candle",
    "DojiStarBull": "Bullish Doji Star",
    "DojiStarBear": "Bearish Doji Star",
    "DojiSouthern": "Southern Doji",
    "DojiNorthern": "Northern Doji",
    "DojiLongLegged": "Long-Legged Doji",
    "DojiGravestone": "Gravestone Doji",
    "DojiGappingUp": "Gapping Up Doji",
    "DojiGappingDn": "Gapping Down Doji",
    "CandleBlack": "Black Candle",
    "BeltholdBullish": "Bullish Belt Hold",
    "BeltholdBearish": "Bearish Belt Hold",
    "BelowStomach": "Below the Stomach",
    "Advanceblock": "Advance Block",
    "AboveStomach": "Above the Stomach",
    "Abandonedbabybull": "Bullish Abandoned Baby",
    "Abandonedbabybear": "Bearish Abandoned Baby",
}


@dataclass
class CandleContext:
    """Precomputed candle measurements for performance and clarity."""

    opens: np.ndarray
    highs: np.ndarray
    lows: np.ndarray
    closes: np.ndarray
    bodies: np.ndarray
    ranges: np.ndarray
    uppers: np.ndarray
    lowers: np.ndarray
    colors: np.ndarray  # 1 bull, -1 bear, 0 doji-like
    avg_body: float
    avg_range: float
    long_body_level: float
    short_body_level: float
    doji_level: np.ndarray

    @property
    def size(self) -> int:
        return len(self.opens)

    def is_gap_up(self, idx: int) -> bool:
        """True when bar gaps above previous high."""
        if idx == 0:
            return False
        return self.lows[idx] > self.highs[idx - 1]

    def is_gap_down(self, idx: int) -> bool:
        """True when bar gaps below previous low."""
        if idx == 0:
            return False
        return self.highs[idx] < self.lows[idx - 1]


def _build_context(data: PatternData, strict: bool) -> CandleContext:
    """
    Precompute candle geometry and thresholds.

    Strict mode tightens body/doji thresholds to mirror Patternz' strict flag.
    """
    opens = data.opens
    highs = data.highs
    lows = data.lows
    closes = data.closes

    bodies = np.abs(closes - opens)
    ranges = np.maximum(highs - lows, 1e-9)  # avoid divide-by-zero
    uppers = highs - np.maximum(opens, closes)
    lowers = np.minimum(opens, closes) - lows

    avg_body = float(np.mean(bodies[-60:])) if len(bodies) >= 1 else 0.0
    avg_range = float(np.mean(ranges[-60:])) if len(ranges) >= 1 else 0.0

    body_multiplier_long = 1.5 if strict else 1.3
    body_multiplier_short = 0.5 if strict else 0.7

    long_body_level = avg_body * body_multiplier_long
    short_body_level = avg_body * body_multiplier_short

    # Dynamic doji tolerance: blend absolute and relative width
    doji_ratio = 0.05 if strict else 0.1
    doji_floor = avg_body * (0.08 if strict else 0.12)
    doji_level = np.maximum(ranges * doji_ratio, doji_floor)

    # Color assignment using doji threshold
    colors = np.zeros_like(opens, dtype=np.int8)
    for i in range(len(opens)):
        if bodies[i] <= doji_level[i]:
            colors[i] = 0
        elif closes[i] > opens[i]:
            colors[i] = 1
        else:
            colors[i] = -1

    return CandleContext(
        opens=opens,
        highs=highs,
        lows=lows,
        closes=closes,
        bodies=bodies,
        ranges=ranges,
        uppers=uppers,
        lowers=lowers,
        colors=colors,
        avg_body=avg_body,
        avg_range=avg_range,
        long_body_level=long_body_level,
        short_body_level=short_body_level,
        doji_level=doji_level,
    )


def _trend(closes: np.ndarray, idx: int, lookback: int = 5) -> float:
    """Approximate slope over lookback bars (positive = uptrend)."""
    start = max(0, idx - lookback + 1)
    window = closes[start : idx + 1]
    if len(window) < 2:
        return 0.0
    x = np.arange(len(window))
    slope, _ = np.polyfit(x, window, 1)
    # Normalize by price to keep scores comparable
    base = np.mean(window) if np.mean(window) != 0 else 1.0
    return float(slope / base)


def _score(base: float, *factors: float) -> float:
    """
    Blend factors into a 0-1 confidence.

    base: starting value (0.45-0.7 recommended)
    factors: evidence in 0-1 range
    """
    evidence = np.mean(factors) if factors else 0.0
    confidence = base + 0.25 * (evidence - 0.5)
    return float(np.clip(confidence, 0.35, 0.98))


def _add_pattern(
    patterns: List[Dict[str, Any]],
    name: str,
    start_idx: int,
    end_idx: int,
    confidence: float,
    direction: Optional[str] = None,
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """Normalize appended pattern dictionaries."""
    label = PATTERN_LABELS.get(name, name)
    patterns.append(
        {
            "pattern": label,
            "key": name,
            "start_idx": int(start_idx),
            "mid_idx": int((start_idx + end_idx) // 2),
            "end_idx": int(end_idx),
            "direction": direction,
            "confidence": round(float(confidence), 4),
            "description": description or f"Legend AI detection for {label}",
            "metadata": metadata or {},
        }
    )


def find_candlesticks(
    data: PatternData,
    helpers: PatternHelpers,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """
    Detect all 105 candlestick patterns defined in the legacy Legend AI library.

    Args:
        data: PatternData with OHLCV arrays.
        helpers: PatternHelpers instance (reserved for future shared checks).
        strict: Tighter geometry thresholds if True.

    Returns:
        List of pattern dictionaries with start/end indices and confidence.
    """
    ctx = _build_context(data, strict)
    patterns: List[Dict[str, Any]] = []

    _detect_single_candles(ctx, patterns, strict)
    _detect_two_candle_patterns(ctx, patterns, strict)
    _detect_three_candle_patterns(ctx, patterns, strict)
    _detect_gap_and_run_patterns(ctx, patterns, strict)
    _detect_multi_session_patterns(ctx, patterns, strict)

    logger.info("Detected %d candlestick patterns", len(patterns))
    return patterns


def _detect_single_candles(
    ctx: CandleContext,
    patterns: List[Dict[str, Any]],
    strict: bool,
) -> None:
    """Single-bar morphologies and context-aware one-candle reversals."""
    for idx in range(ctx.size):
        body = ctx.bodies[idx]
        rng = ctx.ranges[idx]
        upper = ctx.uppers[idx]
        lower = ctx.lowers[idx]
        color = ctx.colors[idx]
        body_pct = body / rng if rng > 0 else 0.0
        upper_pct = upper / rng if rng > 0 else 0.0
        lower_pct = lower / rng if rng > 0 else 0.0
        trend_now = _trend(ctx.closes, idx, lookback=6)

        is_doji = body <= ctx.doji_level[idx]
        long_upper = upper_pct >= (0.55 if strict else 0.5)
        long_lower = lower_pct >= (0.55 if strict else 0.5)
        long_body = body >= ctx.long_body_level
        short_body = body <= ctx.short_body_level

        # Base candles
        if color == 1:
            _add_pattern(
                patterns,
                "CandleWhite",
                idx,
                idx,
                _score(0.55, body_pct),
                direction="bullish",
                metadata={"body_pct": body_pct},
            )
        elif color == -1:
            _add_pattern(
                patterns,
                "CandleBlack",
                idx,
                idx,
                _score(0.55, body_pct),
                direction="bearish",
                metadata={"body_pct": body_pct},
            )

        if short_body and color == 1:
            _add_pattern(
                patterns,
                "CandleShortWht",
                idx,
                idx,
                _score(0.52, 1 - body_pct),
                direction="neutral",
            )
        if short_body and color == -1:
            _add_pattern(
                patterns,
                "CandleShortBlk",
                idx,
                idx,
                _score(0.52, 1 - body_pct),
                direction="neutral",
            )

        if long_body and color == 1:
            _add_pattern(
                patterns,
                "LongDayWhite",
                idx,
                idx,
                _score(0.6, body_pct),
                direction="bullish",
            )
        if long_body and color == -1:
            _add_pattern(
                patterns,
                "LongDayBlack",
                idx,
                idx,
                _score(0.6, body_pct),
                direction="bearish",
            )

        # Marubozu suite
        if long_body and upper_pct < 0.05 and lower_pct < 0.05:
            if color == 1:
                _add_pattern(
                    patterns,
                    "MarubozuWhite",
                    idx,
                    idx,
                    _score(0.68, body_pct),
                    direction="bullish",
                )
            elif color == -1:
                _add_pattern(
                    patterns,
                    "MarubozuBlack",
                    idx,
                    idx,
                    _score(0.68, body_pct),
                    direction="bearish",
                )
        if long_body and lower_pct < 0.02 and color == 1:
            _add_pattern(
                patterns,
                "MarubozuOpeningW",
                idx,
                idx,
                _score(0.62, body_pct),
                direction="bullish",
            )
        if long_body and upper_pct < 0.02 and color == 1:
            _add_pattern(
                patterns,
                "MarubozuClosingW",
                idx,
                idx,
                _score(0.62, body_pct),
                direction="bullish",
            )
        if long_body and lower_pct < 0.02 and color == -1:
            _add_pattern(
                patterns,
                "MarubozuOpeningB",
                idx,
                idx,
                _score(0.62, body_pct),
                direction="bearish",
            )
        if long_body and upper_pct < 0.02 and color == -1:
            _add_pattern(
                patterns,
                "MarubozuClosingB",
                idx,
                idx,
                _score(0.62, body_pct),
                direction="bearish",
            )

        # Spinning tops / high wave
        if short_body and (upper_pct > 0.25 and lower_pct > 0.25):
            _add_pattern(
                patterns,
                "SpinningTop",
                idx,
                idx,
                _score(0.55, upper_pct, lower_pct),
                direction="neutral",
            )
            if color == 1:
                _add_pattern(
                    patterns,
                    "SpinningTopWht",
                    idx,
                    idx,
                    _score(0.56, upper_pct, lower_pct),
                    direction="neutral",
                )
            elif color == -1:
                _add_pattern(
                    patterns,
                    "SpinningTopBlk",
                    idx,
                    idx,
                    _score(0.56, upper_pct, lower_pct),
                    direction="neutral",
                )
        if short_body and upper_pct > 0.4 and lower_pct > 0.4:
            _add_pattern(
                patterns,
                "HighWave",
                idx,
                idx,
                _score(0.58, upper_pct, lower_pct),
                direction="neutral",
            )

        # Belt holds (one bar but trend aware)
        if long_body and lower_pct < 0.05 and color == 1:
            if trend_now < 0:
                _add_pattern(
                    patterns,
                    "BeltholdBullish",
                    idx,
                    idx,
                    _score(0.65, body_pct, -trend_now),
                    direction="bullish",
                )
        if long_body and upper_pct < 0.05 and color == -1:
            if trend_now > 0:
                _add_pattern(
                    patterns,
                    "BeltholdBearish",
                    idx,
                    idx,
                    _score(0.65, body_pct, trend_now),
                    direction="bearish",
                )

        # Doji family
        if is_doji:
            _add_pattern(
                patterns,
                "DojiLongLegged",
                idx,
                idx,
                _score(0.58, upper_pct, lower_pct),
                direction="neutral",
            )
            if upper_pct < 0.05 and lower_pct < 0.05:
                _add_pattern(
                    patterns,
                    "DojiFourPrice",
                    idx,
                    idx,
                    _score(0.62, 1 - upper_pct, 1 - lower_pct),
                    direction="neutral",
                )
            if long_lower and upper_pct < 0.1:
                _add_pattern(
                    patterns,
                    "DojiDragonFly",
                    idx,
                    idx,
                    _score(0.63, lower_pct),
                    direction="bullish",
                )
            if long_upper and lower_pct < 0.1:
                _add_pattern(
                    patterns,
                    "DojiGravestone",
                    idx,
                    idx,
                    _score(0.63, upper_pct),
                    direction="bearish",
                )
            if trend_now > 0:
                _add_pattern(
                    patterns,
                    "DojiNorthern",
                    idx,
                    idx,
                    _score(0.55, trend_now),
                    direction="bearish",
                )
            if trend_now < 0:
                _add_pattern(
                    patterns,
                    "DojiSouthern",
                    idx,
                    idx,
                    _score(0.55, -trend_now),
                    direction="bullish",
                )

        # Rickshaw man (doji with very long shadows)
        if is_doji and upper_pct > 0.45 and lower_pct > 0.45:
            _add_pattern(
                patterns,
                "RickshawMan",
                idx,
                idx,
                _score(0.6, upper_pct, lower_pct),
                direction="neutral",
            )

        # Short shadows combined with gap = gapping doji
        if is_doji and idx > 0:
            if ctx.is_gap_up(idx):
                _add_pattern(
                    patterns,
                    "DojiGappingUp",
                    idx - 1,
                    idx,
                    _score(0.65, abs(trend_now)),
                    direction="bearish",
                )
            if ctx.is_gap_down(idx):
                _add_pattern(
                    patterns,
                    "DojiGappingDn",
                    idx - 1,
                    idx,
                    _score(0.65, abs(trend_now)),
                    direction="bullish",
                )

        # Hammer family (context aware)
        if body_pct < 0.4 and long_lower and upper_pct < 0.25:
            if trend_now < 0:
                _add_pattern(
                    patterns,
                    "Hammer",
                    idx,
                    idx,
                    _score(0.7, lower_pct, -trend_now),
                    direction="bullish",
                )
                _add_pattern(
                    patterns,
                    "Takuri",
                    idx,
                    idx,
                    _score(0.72, lower_pct),
                    direction="bullish",
                )
            elif trend_now > 0:
                _add_pattern(
                    patterns,
                    "HangingMan",
                    idx,
                    idx,
                    _score(0.64, lower_pct, trend_now),
                    direction="bearish",
                )
        if body_pct < 0.4 and long_upper and lower_pct < 0.2:
            if trend_now < 0:
                _add_pattern(
                    patterns,
                    "HammerInverted",
                    idx,
                    idx,
                    _score(0.66, upper_pct, -trend_now),
                    direction="bullish",
                )
            elif trend_now > 0:
                _add_pattern(
                    patterns,
                    "ShootingStar",
                    idx,
                    idx,
                    _score(0.7, upper_pct, trend_now),
                    direction="bearish",
                )
                _add_pattern(
                    patterns,
                    "ShootingStar2",
                    idx,
                    idx,
                    _score(0.72, upper_pct, trend_now),
                    direction="bearish",
                )

        # Advance block / deliberation (trend exhaustion)
        if idx >= 2:
            prev = idx - 1
            prev2 = idx - 2
            if (
                color == 1
                and ctx.colors[prev] == 1
                and ctx.colors[prev2] == 1
                and ctx.closes[idx] > ctx.closes[prev] > ctx.closes[prev2]
                and ctx.uppers[idx] > ctx.bodies[idx]
            ):
                # Diminishing body sizes point to advance block
                shrinking = ctx.bodies[idx] < ctx.bodies[prev] < ctx.bodies[prev2]
                long_wicks = (
                    ctx.uppers[idx] > ctx.bodies[idx]
                    and ctx.uppers[prev] > ctx.bodies[prev]
                )
                if shrinking or long_wicks:
                    _add_pattern(
                        patterns,
                        "Advanceblock",
                        prev2,
                        idx,
                        _score(0.65, trend_now, upper_pct),
                        direction="bearish",
                    )
            if (
                color == 1
                and ctx.colors[prev] == 1
                and ctx.colors[prev2] == 1
                and ctx.closes[idx] > ctx.closes[prev] > ctx.closes[prev2]
                and ctx.bodies[idx] < ctx.bodies[prev] * (0.8 if strict else 0.9)
            ):
                _add_pattern(
                    patterns,
                    "Deliberation",
                    prev2,
                    idx,
                    _score(0.63, trend_now, 1 - body_pct),
                    direction="bearish",
                )


def _detect_two_candle_patterns(
    ctx: CandleContext,
    patterns: List[Dict[str, Any]],
    strict: bool,
) -> None:
    """Two-bar combinations and their close relatives."""
    for idx in range(1, ctx.size):
        prev = idx - 1
        body = ctx.bodies[idx]
        prev_body = ctx.bodies[prev]
        trend_before = _trend(ctx.closes, prev, lookback=6)

        # Engulfing
        if ctx.colors[prev] == -1 and ctx.colors[idx] == 1:
            engulf = (
                ctx.opens[idx] <= ctx.closes[prev]
                and ctx.closes[idx] >= ctx.opens[prev]
            )
            if engulf:
                _add_pattern(
                    patterns,
                    "EngulfingBullish",
                    prev,
                    idx,
                    _score(0.72, body / (prev_body + 1e-9), -trend_before),
                    direction="bullish",
                )
        if ctx.colors[prev] == 1 and ctx.colors[idx] == -1:
            engulf = (
                ctx.opens[idx] >= ctx.closes[prev]
                and ctx.closes[idx] <= ctx.opens[prev]
            )
            if engulf:
                _add_pattern(
                    patterns,
                    "EngulfingBearish",
                    prev,
                    idx,
                    _score(0.72, body / (prev_body + 1e-9), trend_before),
                    direction="bearish",
                )

        # Harami (inside body)
        inside = min(ctx.opens[idx], ctx.closes[idx]) >= min(
            ctx.opens[prev], ctx.closes[prev]
        ) and max(ctx.opens[idx], ctx.closes[idx]) <= max(
            ctx.opens[prev], ctx.closes[prev]
        )
        if inside and ctx.colors[prev] == -1 and ctx.colors[idx] == 1:
            _add_pattern(
                patterns,
                "HaramiBullish",
                prev,
                idx,
                _score(0.64, body / (prev_body + 1e-9), -trend_before),
                direction="bullish",
            )
            if ctx.bodies[idx] <= ctx.doji_level[idx]:
                _add_pattern(
                    patterns,
                    "HaramiCrossBullish",
                    prev,
                    idx,
                    _score(0.65, -trend_before),
                    direction="bullish",
                )
        if inside and ctx.colors[prev] == 1 and ctx.colors[idx] == -1:
            _add_pattern(
                patterns,
                "HaramiBearish",
                prev,
                idx,
                _score(0.64, body / (prev_body + 1e-9), trend_before),
                direction="bearish",
            )
            if ctx.bodies[idx] <= ctx.doji_level[idx]:
                _add_pattern(
                    patterns,
                    "HaramiCrossBearish",
                    prev,
                    idx,
                    _score(0.65, trend_before),
                    direction="bearish",
                )

        # Piercing / Dark Cloud Cover
        mid_prev = min(ctx.opens[prev], ctx.closes[prev]) + prev_body / 2
        if (
            ctx.colors[prev] == -1
            and ctx.colors[idx] == 1
            and ctx.opens[idx] < ctx.lows[prev]
            and ctx.closes[idx] > mid_prev
        ):
            _add_pattern(
                patterns,
                "PiercingPattern",
                prev,
                idx,
                _score(0.7, -trend_before),
                direction="bullish",
            )
        if (
            ctx.colors[prev] == 1
            and ctx.colors[idx] == -1
            and ctx.opens[idx] > ctx.highs[prev]
            and ctx.closes[idx] < mid_prev
        ):
            _add_pattern(
                patterns,
                "DarkCloudCover",
                prev,
                idx,
                _score(0.7, trend_before),
                direction="bearish",
            )

        # Thrusting / On-Neck / In-Neck (continuations after downtrend)
        if ctx.colors[prev] == -1 and ctx.colors[idx] == 1 and trend_before < 0:
            close_pos = (ctx.closes[idx] - ctx.lows[prev]) / (
                ctx.highs[prev] - ctx.lows[prev] + 1e-9
            )
            if close_pos < 0.15:
                _add_pattern(
                    patterns,
                    "InNeckLine",
                    prev,
                    idx,
                    _score(0.63, -trend_before),
                    direction="bearish",
                )
            elif close_pos < 0.35:
                _add_pattern(
                    patterns,
                    "OnNeckLine",
                    prev,
                    idx,
                    _score(0.64, -trend_before),
                    direction="bearish",
                )
            elif close_pos < 0.55:
                _add_pattern(
                    patterns,
                    "Thrusting",
                    prev,
                    idx,
                    _score(0.64, -trend_before),
                    direction="bearish",
                )

        # Meeting lines (counter-attack)
        close_near = (
            abs(ctx.closes[idx] - ctx.closes[prev]) <= abs(ctx.closes[prev]) * 0.003
        )
        if ctx.colors[prev] == -1 and ctx.colors[idx] == 1 and close_near:
            _add_pattern(
                patterns,
                "MeetingLinesBull",
                prev,
                idx,
                _score(0.62, -trend_before),
                direction="bullish",
            )
        if ctx.colors[prev] == 1 and ctx.colors[idx] == -1 and close_near:
            _add_pattern(
                patterns,
                "MeetingLinesBear",
                prev,
                idx,
                _score(0.62, trend_before),
                direction="bearish",
            )

        # Separating lines
        open_equal = abs(ctx.opens[idx] - ctx.opens[prev]) <= max(
            ctx.avg_range * 0.05, abs(ctx.opens[prev]) * 0.002
        )
        if (
            open_equal
            and ctx.colors[prev] == -1
            and ctx.colors[idx] == 1
            and trend_before > 0
        ):
            _add_pattern(
                patterns,
                "SeparatingLinesBull",
                prev,
                idx,
                _score(0.6, trend_before),
                direction="bullish",
            )
        if (
            open_equal
            and ctx.colors[prev] == 1
            and ctx.colors[idx] == -1
            and trend_before < 0
        ):
            _add_pattern(
                patterns,
                "SeparatingLinesBear",
                prev,
                idx,
                _score(0.6, -trend_before),
                direction="bearish",
            )

        # Kicker (dramatic sentiment flip with gap)
        if ctx.is_gap_up(idx) and ctx.colors[prev] == -1 and ctx.colors[idx] == 1:
            _add_pattern(
                patterns,
                "KickerBull",
                prev,
                idx,
                _score(0.72, abs(trend_before)),
                direction="bullish",
            )
        if ctx.is_gap_down(idx) and ctx.colors[prev] == 1 and ctx.colors[idx] == -1:
            _add_pattern(
                patterns,
                "KickerBear",
                prev,
                idx,
                _score(0.72, abs(trend_before)),
                direction="bearish",
            )

        # Above/Below the stomach
        prev_mid = min(ctx.opens[prev], ctx.closes[prev]) + prev_body * 0.5
        if (
            ctx.colors[prev] == -1
            and ctx.colors[idx] == 1
            and ctx.opens[idx] > prev_mid
            and ctx.closes[idx] < ctx.opens[prev]
        ):
            _add_pattern(
                patterns,
                "AboveStomach",
                prev,
                idx,
                _score(0.6, -trend_before),
                direction="bullish",
            )
        if (
            ctx.colors[prev] == 1
            and ctx.colors[idx] == -1
            and ctx.opens[idx] < prev_mid
            and ctx.closes[idx] > ctx.opens[prev]
        ):
            _add_pattern(
                patterns,
                "BelowStomach",
                prev,
                idx,
                _score(0.6, trend_before),
                direction="bearish",
            )

        # Stick sandwich (bear-bull-bear with matching closes)
        if idx >= 2:
            prev2 = idx - 2
            if (
                ctx.colors[prev2] == -1
                and ctx.colors[prev] == 1
                and ctx.colors[idx] == -1
                and abs(ctx.closes[idx] - ctx.closes[prev2])
                <= max(ctx.avg_range * 0.02, abs(ctx.closes[prev2]) * 0.004)
                and ctx.closes[prev] > ctx.closes[prev2]
            ):
                _add_pattern(
                    patterns,
                    "StickSandwich",
                    prev2,
                    idx,
                    _score(0.64, -trend_before),
                    direction="bullish",
                )

        # Matching lows / tweezers
        if ctx.colors[prev] == -1 and ctx.colors[idx] == -1:
            if abs(ctx.closes[idx] - ctx.closes[prev]) <= max(
                ctx.avg_range * 0.01, abs(ctx.closes[prev]) * 0.002
            ):
                _add_pattern(
                    patterns,
                    "MatchingLow",
                    prev,
                    idx,
                    _score(0.6, -trend_before),
                    direction="bullish",
                )
            if abs(ctx.lows[idx] - ctx.lows[prev]) <= max(
                ctx.avg_range * 0.005, abs(ctx.lows[prev]) * 0.0015
            ):
                _add_pattern(
                    patterns,
                    "TweezersBottom",
                    prev,
                    idx,
                    _score(0.6, -trend_before),
                    direction="bullish",
                )
        if abs(ctx.highs[idx] - ctx.highs[prev]) <= max(
            ctx.avg_range * 0.005, abs(ctx.highs[prev]) * 0.0015
        ):
            _add_pattern(
                patterns,
                "TweezersTop",
                prev,
                idx,
                _score(0.6, trend_before),
                direction="bearish",
            )

        # Homing pigeon (inside black candle suggesting loss of momentum)
        if (
            ctx.colors[prev] == -1
            and ctx.colors[idx] == -1
            and trend_before < 0
            and ctx.opens[idx] > ctx.lows[prev]
            and ctx.closes[idx] > ctx.closes[prev]
            and ctx.opens[idx] < ctx.opens[prev]
            and ctx.closes[idx] < ctx.opens[prev]
        ):
            _add_pattern(
                patterns,
                "HomingPigeon",
                prev,
                idx,
                _score(0.6, -trend_before),
                direction="bullish",
            )


def _detect_three_candle_patterns(
    ctx: CandleContext,
    patterns: List[Dict[str, Any]],
    strict: bool,
) -> None:
    """Three-bar (and close cousins) formations."""
    for idx in range(2, ctx.size):
        c0, c1, c2 = idx - 2, idx - 1, idx
        trend_before = _trend(ctx.closes, c0, lookback=7)
        bodies = (ctx.bodies[c0], ctx.bodies[c1], ctx.bodies[c2])

        # Morning/Evening star family
        close_recovery = ctx.closes[c2] > (ctx.opens[c0] + ctx.closes[c0]) / 2
        close_breakdown = ctx.closes[c2] < (ctx.opens[c0] + ctx.closes[c0]) / 2

        if ctx.colors[c0] == -1 and ctx.colors[c2] == 1 and close_recovery:
            if ctx.bodies[c1] <= ctx.doji_level[c1]:
                _add_pattern(
                    patterns,
                    "MorningDojiStar",
                    c0,
                    c2,
                    _score(0.74, -trend_before),
                    direction="bullish",
                )
            elif bodies[1] < bodies[0] and bodies[2] > bodies[1]:
                _add_pattern(
                    patterns,
                    "MorningStar",
                    c0,
                    c2,
                    _score(0.72, -trend_before),
                    direction="bullish",
                )
        if ctx.colors[c0] == 1 and ctx.colors[c2] == -1 and close_breakdown:
            if ctx.bodies[c1] <= ctx.doji_level[c1]:
                _add_pattern(
                    patterns,
                    "EveningDojiStar",
                    c0,
                    c2,
                    _score(0.74, trend_before),
                    direction="bearish",
                )
            elif bodies[1] < bodies[0] and bodies[2] > bodies[1]:
                _add_pattern(
                    patterns,
                    "EveningStar",
                    c0,
                    c2,
                    _score(0.72, trend_before),
                    direction="bearish",
                )

        # Three inside / outside
        inside = min(ctx.opens[c1], ctx.closes[c1]) >= min(
            ctx.opens[c0], ctx.closes[c0]
        ) and max(ctx.opens[c1], ctx.closes[c1]) <= max(ctx.opens[c0], ctx.closes[c0])
        engulf = min(ctx.opens[c1], ctx.closes[c1]) <= min(
            ctx.opens[c0], ctx.closes[c0]
        ) and max(ctx.opens[c1], ctx.closes[c1]) >= max(ctx.opens[c0], ctx.closes[c0])
        if (
            inside
            and ctx.colors[c0] == -1
            and ctx.colors[c2] == 1
            and ctx.closes[c2] > ctx.opens[c0]
        ):
            _add_pattern(
                patterns,
                "ThreeInsideUp",
                c0,
                c2,
                _score(0.68, -trend_before),
                direction="bullish",
            )
        if (
            inside
            and ctx.colors[c0] == 1
            and ctx.colors[c2] == -1
            and ctx.closes[c2] < ctx.opens[c0]
        ):
            _add_pattern(
                patterns,
                "ThreeInsideDown",
                c0,
                c2,
                _score(0.68, trend_before),
                direction="bearish",
            )
        if (
            engulf
            and ctx.colors[c0] == -1
            and ctx.colors[c1] == 1
            and ctx.colors[c2] == 1
        ):
            _add_pattern(
                patterns,
                "ThreeOutsideUp",
                c0,
                c2,
                _score(0.7, -trend_before),
                direction="bullish",
            )
        if (
            engulf
            and ctx.colors[c0] == 1
            and ctx.colors[c1] == -1
            and ctx.colors[c2] == -1
        ):
            _add_pattern(
                patterns,
                "ThreeOutsideDown",
                c0,
                c2,
                _score(0.7, trend_before),
                direction="bearish",
            )

        # Three line strike
        if ctx.colors[c0] == ctx.colors[c1] == ctx.colors[c2]:
            same_color = ctx.colors[c0]
            if idx + 1 < ctx.size:
                c3 = idx + 1
                opp = ctx.colors[c3] == -same_color
                progress = (
                    (ctx.closes[c0] < ctx.closes[c1] < ctx.closes[c2])
                    if same_color == 1
                    else (ctx.closes[c0] > ctx.closes[c1] > ctx.closes[c2])
                )
                if opp and progress:
                    if same_color == 1:
                        _add_pattern(
                            patterns,
                            "ThreeLineStrikeBull",
                            c0,
                            c3,
                            _score(0.69, abs(trend_before)),
                            direction="bullish",
                        )
                    else:
                        _add_pattern(
                            patterns,
                            "ThreeLineStrikeBear",
                            c0,
                            c3,
                            _score(0.69, abs(trend_before)),
                            direction="bearish",
                        )

        # Soldiers / crows
        if ctx.colors[c0] == ctx.colors[c1] == ctx.colors[c2] == 1:
            if ctx.closes[c2] > ctx.closes[c1] > ctx.closes[c0]:
                _add_pattern(
                    patterns,
                    "ThreeWhiteSoldiers",
                    c0,
                    c2,
                    _score(0.75, -trend_before),
                    direction="bullish",
                )
        if ctx.colors[c0] == ctx.colors[c1] == ctx.colors[c2] == -1:
            if ctx.closes[c2] < ctx.closes[c1] < ctx.closes[c0]:
                _add_pattern(
                    patterns,
                    "ThreeBlackCrows",
                    c0,
                    c2,
                    _score(0.75, trend_before),
                    direction="bearish",
                )
                open_near = abs(ctx.opens[c1] - ctx.closes[c0]) <= max(
                    ctx.avg_range * 0.02, abs(ctx.closes[c0]) * 0.003
                ) and abs(ctx.opens[c2] - ctx.closes[c1]) <= max(
                    ctx.avg_range * 0.02, abs(ctx.closes[c1]) * 0.003
                )
                if open_near:
                    _add_pattern(
                        patterns,
                        "Identical3Crows",
                        c0,
                        c2,
                        _score(0.7, trend_before),
                        direction="bearish",
                    )

        # Three stars in the south (rare bullish reversal with shrinking black candles)
        if (
            ctx.colors[c0] == ctx.colors[c1] == ctx.colors[c2] == -1
            and trend_before < 0
        ):
            lower_shadows = [
                ctx.lowers[c0] / (ctx.ranges[c0] + 1e-9),
                ctx.lowers[c1] / (ctx.ranges[c1] + 1e-9),
                ctx.lowers[c2] / (ctx.ranges[c2] + 1e-9),
            ]
            if (
                lower_shadows[0] > 0.5
                and ctx.lows[c1] < ctx.lows[c0]
                and ctx.lows[c2] > ctx.lows[c1]
                and ctx.closes[c2] > ctx.closes[c1]
                and ctx.bodies[c2] < ctx.bodies[c1] < ctx.bodies[c0]
            ):
                _add_pattern(
                    patterns,
                    "ThreeStarsSouth",
                    c0,
                    c2,
                    _score(0.64, -trend_before),
                    direction="bullish",
                )

        # Tri-star (three doji with gaps)
        if (
            ctx.bodies[c0] <= ctx.doji_level[c0]
            and ctx.bodies[c1] <= ctx.doji_level[c1]
            and ctx.bodies[c2] <= ctx.doji_level[c2]
        ):
            if ctx.is_gap_up(c1) and ctx.is_gap_down(c2):
                _add_pattern(
                    patterns,
                    "TriStarBear",
                    c0,
                    c2,
                    _score(0.65, trend_before),
                    direction="bearish",
                )
            if ctx.is_gap_down(c1) and ctx.is_gap_up(c2):
                _add_pattern(
                    patterns,
                    "TriStarBull",
                    c0,
                    c2,
                    _score(0.65, -trend_before),
                    direction="bullish",
                )

        # Doji stars (with directional context)
        if ctx.bodies[c1] <= ctx.doji_level[c1]:
            if ctx.is_gap_down(c1) and ctx.colors[c0] == -1:
                _add_pattern(
                    patterns,
                    "DojiStarBull",
                    c0,
                    c1,
                    _score(0.63, -trend_before),
                    direction="bullish",
                )
            if ctx.is_gap_up(c1) and ctx.colors[c0] == 1:
                _add_pattern(
                    patterns,
                    "DojiStarBear",
                    c0,
                    c1,
                    _score(0.63, trend_before),
                    direction="bearish",
                )

        # Side-by-side white lines (bull and bear versions)
        if (
            ctx.colors[c0] == 1
            and ctx.colors[c1] == 1
            and ctx.colors[c2] == 1
            and ctx.is_gap_up(c1)
            and abs(ctx.bodies[c1] - ctx.bodies[c2]) <= ctx.avg_body * 0.25
        ):
            _add_pattern(
                patterns,
                "SBSWLinesBull",
                c0,
                c2,
                _score(0.66, trend_before),
                direction="bullish",
            )
        if (
            ctx.colors[c0] == -1
            and ctx.colors[c1] == 1
            and ctx.colors[c2] == 1
            and ctx.is_gap_down(c1)
            and abs(ctx.bodies[c1] - ctx.bodies[c2]) <= ctx.avg_body * 0.25
        ):
            _add_pattern(
                patterns,
                "SBSWLinesBear",
                c0,
                c2,
                _score(0.64, -trend_before),
                direction="bearish",
            )

        # Abandoned baby (handled as 3-bar star with isolated doji)
        if ctx.bodies[c1] <= ctx.doji_level[c1]:
            if ctx.is_gap_down(c1) and ctx.is_gap_up(c2):
                _add_pattern(
                    patterns,
                    "Abandonedbabybull",
                    c0,
                    c2,
                    _score(0.7, -trend_before),
                    direction="bullish",
                )
            if ctx.is_gap_up(c1) and ctx.is_gap_down(c2):
                _add_pattern(
                    patterns,
                    "Abandonedbabybear",
                    c0,
                    c2,
                    _score(0.7, trend_before),
                    direction="bearish",
                )

        # Two crows / upside gap two crows
        if (
            ctx.colors[c0] == 1
            and ctx.colors[c1] == -1
            and ctx.colors[c2] == -1
            and ctx.is_gap_up(c1)
            and ctx.closes[c2] < ctx.closes[c1] < ctx.closes[c0]
        ):
            _add_pattern(
                patterns,
                "TwoCrows",
                c0,
                c2,
                _score(0.67, trend_before),
                direction="bearish",
            )
            if ctx.closes[c2] > ctx.closes[c0]:
                _add_pattern(
                    patterns,
                    "UpsideGap2Crows",
                    c0,
                    c2,
                    _score(0.68, trend_before),
                    direction="bearish",
                )

        # Unique three river bottom (soft bullish turn)
        if (
            ctx.colors[c0] == -1
            and ctx.colors[c1] == -1
            and ctx.colors[c2] == 1
            and ctx.lows[c1] < ctx.lows[c0]
            and ctx.closes[c2] > ctx.opens[c1]
        ):
            _add_pattern(
                patterns,
                "Unique3RiverBottom",
                c0,
                c2,
                _score(0.63, -trend_before),
                direction="bullish",
            )

        # Last engulfing (contrarian engulf)
        if ctx.colors[c0] == 1 and ctx.colors[c1] == -1:
            engulf = ctx.opens[c1] >= ctx.closes[c0] and ctx.closes[c1] <= ctx.opens[c0]
            if engulf:
                _add_pattern(
                    patterns,
                    "LastEngulfTop",
                    c0,
                    c1,
                    _score(0.62, trend_before),
                    direction="bearish",
                )
        if ctx.colors[c0] == -1 and ctx.colors[c1] == 1:
            engulf = ctx.opens[c1] <= ctx.closes[c0] and ctx.closes[c1] >= ctx.opens[c0]
            if engulf:
                _add_pattern(
                    patterns,
                    "LastEngulfBot",
                    c0,
                    c1,
                    _score(0.62, -trend_before),
                    direction="bullish",
                )


def _detect_gap_and_run_patterns(
    ctx: CandleContext,
    patterns: List[Dict[str, Any]],
    strict: bool,
) -> None:
    """Gap-centric patterns and persistent price-line runs."""
    # New price lines (streaks of higher highs/lows)
    streak_up = 0
    streak_down = 0
    for idx in range(1, ctx.size):
        if ctx.closes[idx] > ctx.closes[idx - 1]:
            streak_up += 1
            streak_down = 0
        elif ctx.closes[idx] < ctx.closes[idx - 1]:
            streak_down += 1
            streak_up = 0
        else:
            streak_up = streak_down = 0

        if streak_up >= 8:
            _add_pattern(
                patterns,
                "EightNewPriceLines",
                idx - streak_up + 1,
                idx,
                _score(0.6, streak_up / 13),
                direction="bullish",
            )
        if streak_up >= 10:
            _add_pattern(
                patterns,
                "TenNewPriceLines",
                idx - streak_up + 1,
                idx,
                _score(0.62, streak_up / 13),
                direction="bullish",
            )
        if streak_up >= 12:
            _add_pattern(
                patterns,
                "TwelveNewPriceLines",
                idx - streak_up + 1,
                idx,
                _score(0.64, streak_up / 13),
                direction="bullish",
            )
        if streak_up >= 13:
            _add_pattern(
                patterns,
                "ThirteenNewPriceLines",
                idx - streak_up + 1,
                idx,
                _score(0.66, streak_up / 13),
                direction="bullish",
            )
        if streak_down >= 2:
            _add_pattern(
                patterns,
                "TwoBlackGapping",
                idx - streak_down + 1,
                idx,
                _score(0.6, streak_down / 5),
                direction="bearish",
            )

    # Windows and Tasuki gaps
    for idx in range(1, ctx.size):
        trend_before = _trend(ctx.closes, idx - 1, lookback=6)
        if ctx.is_gap_up(idx):
            _add_pattern(
                patterns,
                "WindowRising",
                idx - 1,
                idx,
                _score(0.6, trend_before),
                direction="bullish",
            )
            # Upside tasuki gap (gap up + red that partially fills)
            if (
                idx + 1 < ctx.size
                and ctx.colors[idx] == 1
                and ctx.colors[idx + 1] == -1
                and ctx.closes[idx + 1] > ctx.opens[idx - 1]
            ):
                _add_pattern(
                    patterns,
                    "UpsideTasukiGap",
                    idx - 1,
                    idx + 1,
                    _score(0.64, trend_before),
                    direction="bullish",
                )
            # Upside gap three methods (gap, two small pullbacks, continuation)
            if (
                idx + 2 < ctx.size
                and ctx.colors[idx] == 1
                and ctx.colors[idx + 1] == 1
                and ctx.colors[idx + 2] == 1
                and ctx.closes[idx + 2] > ctx.closes[idx]
            ):
                _add_pattern(
                    patterns,
                    "UpsideGap3Method",
                    idx - 1,
                    idx + 2,
                    _score(0.63, trend_before),
                    direction="bullish",
                )
        if ctx.is_gap_down(idx):
            _add_pattern(
                patterns,
                "WindowFalling",
                idx - 1,
                idx,
                _score(0.6, -trend_before),
                direction="bearish",
            )
            if (
                idx + 1 < ctx.size
                and ctx.colors[idx] == -1
                and ctx.colors[idx + 1] == 1
                and ctx.closes[idx + 1] < ctx.opens[idx - 1]
            ):
                _add_pattern(
                    patterns,
                    "DownsideTasukiGap",
                    idx - 1,
                    idx + 1,
                    _score(0.64, -trend_before),
                    direction="bearish",
                )
            if (
                idx + 2 < ctx.size
                and ctx.colors[idx] == -1
                and ctx.colors[idx + 1] == -1
                and ctx.colors[idx + 2] == -1
                and ctx.closes[idx + 2] < ctx.closes[idx]
            ):
                _add_pattern(
                    patterns,
                    "DownsideGap3Methods",
                    idx - 1,
                    idx + 2,
                    _score(0.63, -trend_before),
                    direction="bearish",
                )


def _detect_multi_session_patterns(
    ctx: CandleContext,
    patterns: List[Dict[str, Any]],
    strict: bool,
) -> None:
    """Four- and five-bar patterns plus complex sequences."""
    for idx in range(4, ctx.size):
        i0, i1, i2, i3, i4 = idx - 4, idx - 3, idx - 2, idx - 1, idx
        trend_before = _trend(ctx.closes, i0, lookback=10)

        # Breakaway patterns (gap followed by drift then reversal)
        if ctx.colors[i0] == -1 and ctx.is_gap_down(i1) and ctx.colors[i4] == 1:
            if (
                ctx.closes[i2] < ctx.closes[i0]
                and ctx.closes[i3] < ctx.closes[i0]
                and ctx.closes[i4] > ctx.opens[i1]
            ):
                _add_pattern(
                    patterns,
                    "BreakawayBull",
                    i0,
                    i4,
                    _score(0.64, -trend_before),
                    direction="bullish",
                )
        if ctx.colors[i0] == 1 and ctx.is_gap_up(i1) and ctx.colors[i4] == -1:
            if (
                ctx.closes[i2] > ctx.closes[i0]
                and ctx.closes[i3] > ctx.closes[i0]
                and ctx.closes[i4] < ctx.opens[i1]
            ):
                _add_pattern(
                    patterns,
                    "BreakawayBear",
                    i0,
                    i4,
                    _score(0.64, trend_before),
                    direction="bearish",
                )

        # Rising/Falling three methods
        if (
            ctx.colors[i0] == 1
            and ctx.colors[i4] == 1
            and ctx.closes[i4] > ctx.closes[i0]
            and ctx.colors[i1] == ctx.colors[i2] == ctx.colors[i3] == -1
        ):
            _add_pattern(
                patterns,
                "Rising3method",
                i0,
                i4,
                _score(0.68, trend_before),
                direction="bullish",
            )
        if (
            ctx.colors[i0] == -1
            and ctx.colors[i4] == -1
            and ctx.closes[i4] < ctx.closes[i0]
            and ctx.colors[i1] == ctx.colors[i2] == ctx.colors[i3] == 1
        ):
            _add_pattern(
                patterns,
                "Falling3Method",
                i0,
                i4,
                _score(0.68, -trend_before),
                direction="bearish",
            )

        # Mat hold (trend continuation with brief pause)
        if (
            ctx.colors[i0] == 1
            and ctx.is_gap_up(i1)
            and ctx.colors[i1] in (1, -1)
            and ctx.colors[i2] in (1, -1)
            and ctx.colors[i3] in (1, -1)
            and ctx.colors[i4] == 1
            and ctx.closes[i4] > ctx.highs[i0]
        ):
            _add_pattern(
                patterns,
                "MatHold",
                i0,
                i4,
                _score(0.67, trend_before),
                direction="bullish",
            )

        # Ladder bottom (series of lower closes then reversal gap)
        if (
            ctx.colors[i0] == -1
            and ctx.colors[i1] == -1
            and ctx.colors[i2] == -1
            and ctx.colors[i3] == -1
            and ctx.colors[i4] == 1
            and ctx.closes[i4] > ctx.opens[i2]
        ):
            _add_pattern(
                patterns,
                "LadderBottom",
                i0,
                i4,
                _score(0.65, -trend_before),
                direction="bullish",
            )

        # Concealing baby swallow (all black with gaps)
        if (
            ctx.colors[i0] == ctx.colors[i1] == ctx.colors[i2] == ctx.colors[i3] == -1
            and ctx.is_gap_down(i1)
            and ctx.is_gap_down(i2)
            and ctx.lows[i3] < ctx.lows[i2]
        ):
            _add_pattern(
                patterns,
                "ConcealingBaby",
                i0,
                i3,
                _score(0.64, -trend_before),
                direction="bullish",
            )

        # Advance block already in single-candle loop, but capture longer variants
        if (
            ctx.colors[i2] == ctx.colors[i3] == ctx.colors[i4] == 1
            and ctx.closes[i4] > ctx.closes[i3] > ctx.closes[i2]
            and ctx.uppers[i4] > ctx.bodies[i4]
        ):
            _add_pattern(
                patterns,
                "Advanceblock",
                i2,
                i4,
                _score(0.63, trend_before),
                direction="bearish",
            )

        # Doji star collapse (gap down doji then sharp move)
        if (
            ctx.bodies[i3] <= ctx.doji_level[i3]
            and ctx.is_gap_down(i3)
            and ctx.colors[i4] == 1
            and ctx.closes[i4] > ctx.opens[i2]
        ):
            _add_pattern(
                patterns,
                "DojiStarCollapse",
                i2,
                i4,
                _score(0.62, -trend_before),
                direction="bullish",
            )
