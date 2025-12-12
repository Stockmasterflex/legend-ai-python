"""
Legend AI Pattern Detection Engine

Professional-grade pattern recognition system developed by Legend AI Research Team.
Advanced technical analysis algorithms for institutional-quality pattern detection.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

import numpy as np

from app.core.pattern_engine.candlesticks import find_candlesticks
from app.core.pattern_engine.helpers import PatternData, get_pattern_helpers
from app.core.pattern_engine.patterns import (find_ascending_triangle,
                                              find_broadening_formations,
                                              find_channels, find_cup,
                                              find_descending_triangle,
                                              find_double_bottoms, find_flags,
                                              find_head_shoulders_bottom,
                                              find_head_shoulders_top,
                                              find_ht_flag, find_mmd, find_mmu,
                                              find_pennants, find_rectangles,
                                              find_single_day_patterns,
                                              find_sym_triangle,
                                              find_triple_bottoms,
                                              find_triple_tops, find_wedges)

logger = logging.getLogger(__name__)


class PatternDetector:
    """
    Legend AI Pattern Detection Engine

    Advanced pattern recognition system integrating:
    - Minervini VCP/MMU patterns
    - Professional chart patterns (124+ patterns)
    - Candlestick patterns (105+ patterns)
    - Single-day patterns (15+ patterns)

    Provides institutional-grade pattern detection with precise entry/stop/target levels.
    """

    def __init__(self, strict: bool = False):
        """
        Initialize Legend AI Pattern Detection Engine.

        Args:
            strict: Use strict pattern detection rules (tighter tolerances)
        """
        self.helpers = get_pattern_helpers()
        self.helpers.strict_patterns = strict
        self.strict = strict

    def detect_all_patterns(
        self,
        ohlcv_data: Dict[str, Any],
        ticker: str = "UNKNOWN",
        include_candlesticks: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Detect all Bulkowski patterns in OHLCV data.

        Args:
            ohlcv_data: Dictionary with keys: 'o', 'h', 'l', 'c', 'v', 't'
            ticker: Stock ticker symbol
            include_candlesticks: Whether to include candlestick signals

        Returns:
            List of detected patterns with metadata
        """
        try:
            # Convert to PatternData format
            pattern_data = self._convert_to_pattern_data(ohlcv_data)
            data_len = len(pattern_data)

            if data_len < 5:
                logger.debug(f"Insufficient data for {ticker}: {data_len} bars")
                return []

            all_patterns = []

            # Run heavier swing detectors only when enough history exists
            if data_len >= 50:
                logger.debug(
                    f"Running Legend AI Pattern Engine on {ticker} with {data_len} bars"
                )

                # CRITICAL PATTERNS (Highest Value)
                # MMU/VCP - Mark Minervini's Volatility Contraction Pattern
                mmu_patterns = find_mmu(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(mmu_patterns)

                # MMD - Inverse VCP (Bearish)
                mmd_patterns = find_mmd(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(mmd_patterns)

                # High Tight Flag - Explosive breakout pattern
                htf_patterns = find_ht_flag(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    dates=pattern_data.timestamps,
                    helpers=self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(htf_patterns)

                # Flags - Bull and Bear flags
                flag_patterns = find_flags(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(flag_patterns)

                # Pennants - Symmetrical consolidation
                pennant_patterns = find_pennants(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(pennant_patterns)

                # Wedges - Rising and Falling
                wedge_patterns = find_wedges(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(wedge_patterns)

                # Triple Tops/Bottoms
                triple_bottoms = find_triple_bottoms(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(triple_bottoms)

                triple_tops = find_triple_tops(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(triple_tops)

                # Head & Shoulders
                hs_top = find_head_shoulders_top(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(hs_top)

                hs_bottom = find_head_shoulders_bottom(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(hs_bottom)

                # Rectangles
                rectangle_patterns = find_rectangles(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(rectangle_patterns)

                # Channels
                channel_patterns = find_channels(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(channel_patterns)

                # Broadening formations
                broadening_patterns = find_broadening_formations(
                    pattern_data.opens,
                    pattern_data.highs,
                    pattern_data.lows,
                    pattern_data.closes,
                    pattern_data.volumes,
                    self.helpers,
                    strict=self.strict,
                )
                all_patterns.extend(broadening_patterns)

                # CLASSIC PATTERNS
                # Cup & Handle
                cups = find_cup(pattern_data, self.helpers, strict=self.strict)
                all_patterns.extend(
                    [self._format_pattern(p, ticker, pattern_data) for p in cups]
                )

                # Double Bottoms (Adam/Eve variants)
                double_bottoms = find_double_bottoms(
                    pattern_data, self.helpers, find_variants=True
                )
                all_patterns.extend(
                    [
                        self._format_pattern(p, ticker, pattern_data)
                        for p in double_bottoms
                    ]
                )

                # Triangles - Ascending, Descending, Symmetrical
                asc_triangles = find_ascending_triangle(pattern_data, self.helpers)
                all_patterns.extend(
                    [
                        self._format_pattern(p, ticker, pattern_data)
                        for p in asc_triangles
                    ]
                )

                desc_triangles = find_descending_triangle(pattern_data, self.helpers)
                all_patterns.extend(
                    [
                        self._format_pattern(p, ticker, pattern_data)
                        for p in desc_triangles
                    ]
                )

                sym_triangles = find_sym_triangle(pattern_data, self.helpers)
                all_patterns.extend(
                    [
                        self._format_pattern(p, ticker, pattern_data)
                        for p in sym_triangles
                    ]
                )
            else:
                logger.debug(
                    "Skipping swing patterns for %s due to limited history (%d bars)",
                    ticker,
                    data_len,
                )

            # Single-day patterns (inside/outside day, NR4/NR7, spikes, CPR/OCR, etc.)
            single_day = find_single_day_patterns(pattern_data, self.helpers)
            all_patterns.extend(
                [self._format_pattern(p, ticker, pattern_data) for p in single_day]
            )

            # Candlestick suite (lightweight, works with short history)
            if include_candlesticks:
                candles = find_candlesticks(
                    pattern_data, self.helpers, strict=self.strict
                )
                all_patterns.extend(
                    [self._format_pattern(p, ticker, pattern_data) for p in candles]
                )

            logger.info(f"Found {len(all_patterns)} total patterns for {ticker}")
            return all_patterns

        except Exception as e:
            logger.exception(f"Error detecting patterns for {ticker}: {e}")
            return []

    def _convert_to_pattern_data(self, ohlcv_data: Dict[str, Any]) -> PatternData:
        """
        Convert Legend AI OHLCV format to Bulkowski PatternData format.

        Legend AI format:
        {
            'o': [opens],
            'h': [highs],
            'l': [lows],
            'c': [closes],
            'v': [volumes],
            't': [timestamps]
        }

        Bulkowski format:
        PatternData with nHLC[6, N] array
        """
        opens = np.array(ohlcv_data.get("o", []), dtype=np.float64)
        highs = np.array(ohlcv_data.get("h", []), dtype=np.float64)
        lows = np.array(ohlcv_data.get("l", []), dtype=np.float64)
        closes = np.array(ohlcv_data.get("c", []), dtype=np.float64)
        volumes = np.array(ohlcv_data.get("v", []), dtype=np.float64)
        timestamps = ohlcv_data.get("t", None)

        if timestamps is not None:
            timestamps = np.array(timestamps)

        return PatternData(opens, highs, lows, closes, volumes, timestamps)

    def _format_pattern(
        self, pattern: Dict[str, Any], ticker: str, data: PatternData
    ) -> Dict[str, Any]:
        """
        Format pattern output to Legend AI API format.

        Converts internal pattern representation to API-friendly format
        with entry/stop/target prices.
        """
        # Check if pattern already has entry/stop/target (new patterns)
        if "entry" in pattern and "stop" in pattern and "target" in pattern:
            # New pattern format (MMU/VCP, HTFlag, Flags, Wedges, etc.)
            return {
                "ticker": ticker,
                "pattern": pattern["pattern"],
                "pattern_type": pattern.get("type", pattern["pattern"]),
                "confidence": pattern["confidence"],
                "score": pattern.get("score", pattern["confidence"] * 10),
                "entry": round(pattern["entry"], 2),
                "stop": round(pattern["stop"], 2),
                "target": round(pattern["target"], 2),
                "current_price": round(
                    pattern.get("current_price", data.closes[-1]), 2
                ),
                "risk_reward": round(pattern.get("risk_reward", 0), 2),
                "confirmed": pattern.get("confirmed", False),
                "pending": not pattern.get("confirmed", False),
                "width": pattern.get("width", 0),
                "height": pattern.get("height", 0),
                "metadata": pattern.get("metadata", {}),
                "timestamp": datetime.now().isoformat(),
            }

        # Legacy pattern format (Cup, DB, Triangles)
        # Extract key indices
        start_idx = pattern["start_idx"]
        pattern.get("mid_idx", start_idx)
        end_idx = pattern["end_idx"]

        # Get current price
        current_price = data.closes[-1]

        # Calculate entry/stop/target based on pattern type
        entry, stop, target = self._calculate_levels(pattern, data)

        # Calculate risk/reward
        risk = entry - stop if entry > stop else 0.01
        reward = target - entry if target > entry else 0.01
        risk_reward = reward / risk if risk > 0 else 0

        # Format timestamps if available
        start_date = None
        end_date = None
        if data.timestamps is not None:
            start_date = (
                str(data.timestamps[start_idx])[:10]
                if start_idx < len(data.timestamps)
                else None
            )
            end_date = (
                str(data.timestamps[end_idx])[:10]
                if end_idx < len(data.timestamps)
                else None
            )

        return {
            "ticker": ticker,
            "pattern": pattern["pattern"],
            "pattern_type": pattern["pattern"],
            "confidence": pattern["confidence"],
            "score": pattern["confidence"] * 10,  # Convert 0-1 to 0-10 scale
            "entry": round(entry, 2),
            "stop": round(stop, 2),
            "target": round(target, 2),
            "current_price": round(current_price, 2),
            "risk_reward": round(risk_reward, 2),
            "confirmed": pattern.get("confirmed", False),
            "pending": pattern.get("pending", False),
            "start_idx": start_idx,
            "end_idx": end_idx,
            "start_date": start_date,
            "end_date": end_date,
            "width": pattern.get("width", end_idx - start_idx),
            "metadata": pattern,  # Include full pattern data
            "timestamp": datetime.now().isoformat(),
        }

    def _calculate_levels(
        self, pattern: Dict[str, Any], data: PatternData
    ) -> tuple[float, float, float]:
        """
        Calculate entry, stop, and target prices for a pattern.

        Returns:
            (entry, stop, target) tuple
        """
        pattern_name = pattern["pattern"]

        # Remove confirmation marker
        base_pattern = pattern_name.replace("?", "")

        # Pattern-specific logic
        if "Cup" in base_pattern:
            # Entry: Right rim high (breakout point)
            entry = pattern.get("right_rim", data.closes[-1])
            # Stop: Below bottom with buffer
            stop = pattern.get("bottom", entry * 0.92) * 0.98
            # Target: Measure move (pattern provides this)
            target = pattern.get("target", entry * 1.15)

        elif "DB" in base_pattern or "Double Bottom" in base_pattern:
            # Entry: Peak between bottoms (breakout point)
            entry = pattern.get("peak", data.closes[-1])
            # Stop: Below second bottom
            stop = pattern.get("bottom2", entry * 0.95) * 0.98
            # Target: Measure move
            target = pattern.get("target", entry * 1.10)

        elif "Triangle" in base_pattern:
            # Entry: Breakout level (resistance for ascending, support for descending)
            if "Ascending" in base_pattern:
                entry = pattern.get("resistance", data.closes[-1])
                stop = pattern.get("support_end", entry * 0.96)
            elif "Descending" in base_pattern:
                entry = pattern.get("support", data.closes[-1])
                stop = pattern.get("resistance_end", entry * 1.04)
            else:  # Symmetrical
                # Use current price as entry
                entry = data.closes[-1]
                # Stop depends on breakout direction
                if pattern.get("breakout_direction") == "up":
                    stop = pattern.get("support_end", entry * 0.96)
                elif pattern.get("breakout_direction") == "down":
                    stop = pattern.get("resistance_end", entry * 1.04)
                else:
                    # No breakout yet
                    stop = min(pattern.get("support_end", entry * 0.96), entry * 0.96)

            target = pattern.get("target", entry * 1.12)

        else:
            # Default: use 7% stop, 15% target
            entry = data.closes[-1]
            stop = entry * 0.93
            target = entry * 1.15

        return entry, stop, target


# Singleton instance
_pattern_detector = None


def get_pattern_detector(strict: bool = False) -> PatternDetector:
    """Get or create Legend AI Pattern Detector instance"""
    global _pattern_detector
    if _pattern_detector is None or _pattern_detector.strict != strict:
        _pattern_detector = PatternDetector(strict=strict)
    return _pattern_detector
