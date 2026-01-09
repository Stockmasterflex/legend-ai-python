from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Tuple

import numpy as np


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    try:
        return float(np.clip(value, minimum, maximum))
    except Exception:
        return 0.0


@dataclass
class ScoreComponents:
    """Breakdown of the 10-point scoring system."""

    trend_start: float = 0.0
    trend_quality: float = 0.0
    flat_base: float = 0.0
    hcr: float = 0.0
    yearly_range: float = 0.0
    pattern_height: float = 0.0
    volume_trend: float = 0.0
    throwback: float = 0.0
    breakout_gap: float = 0.0
    market_cap: float = 0.0

    def total_score(self) -> float:
        return round(
            self.trend_start
            + self.trend_quality
            + self.flat_base
            + self.hcr
            + self.yearly_range
            + self.pattern_height
            + self.volume_trend
            + self.throwback
            + self.breakout_gap
            + self.market_cap,
            2,
        )

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


class PatternScorer:
    """
    Lightweight scoring system inspired by Patternz scoring inputs.
    Each component is normalized to 0-1, yielding a 0-10 total.
    """

    # Priority patterns for portfolio scanner (get 1.5-point boost)
    PRIORITY_PATTERNS = {
        "VCP", "MMU", "Cup & Handle", "Cup",
        "Bull Flag", "Flag", "Pennant",
        "Triangle Ascending", "Ascending Triangle",
        "Falling Wedge", "Wedge Falling"
    }

    def score_pattern(self, pattern: Dict[str, Any]) -> Tuple[ScoreComponents, float]:
        """Score a single pattern using heuristic criteria."""
        metadata = pattern.get("metadata") or {}
        components = ScoreComponents(
            trend_start=self._score_trend_start(pattern, metadata),
            trend_quality=self._score_trend_quality(pattern, metadata),
            flat_base=self._score_flat_base(pattern, metadata),
            hcr=self._score_hcr(pattern, metadata),
            yearly_range=self._score_yearly_range(pattern, metadata),
            pattern_height=self._score_pattern_height(pattern, metadata),
            volume_trend=self._score_volume(pattern, metadata),
            throwback=self._score_throwback(metadata),
            breakout_gap=self._score_breakout_gap(pattern, metadata),
            market_cap=self._score_market_cap(pattern),
        )

        return components, components.total_score()

    def apply_priority_boost(self, pattern_name: str, base_score: float) -> float:
        """
        Apply 1.5-point boost to priority patterns for portfolio scanner.

        Priority patterns: VCP, Cup & Handle, Flags, Pennants,
        Ascending Triangles, and Falling Wedges.
        """
        for priority in self.PRIORITY_PATTERNS:
            if priority.lower() in pattern_name.lower():
                boosted = base_score + 1.5
                return min(10.0, boosted)  # Cap at 10.0
        return base_score

    def score_patterns(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score multiple patterns and return them sorted by score."""
        scored: List[Dict[str, Any]] = []
        for pattern in patterns:
            components, total = self.score_pattern(pattern)

            # Apply priority boost for portfolio scanner
            pattern_name = pattern.get("pattern", "")
            total = self.apply_priority_boost(pattern_name, total)

            enriched = dict(pattern)
            enriched["score"] = total
            enriched["score_components"] = components.to_dict()
            scored.append(enriched)

        scored.sort(key=lambda item: item.get("score", 0.0), reverse=True)
        return scored

    # ------------------------------------------------------------------ #
    # Component scoring helpers
    # ------------------------------------------------------------------ #
    def _score_trend_start(self, pattern: Dict[str, Any], metadata: Dict[str, Any]) -> float:
        """
        Reward early uptrends that already established momentum.
        Uses percentage off lows or recent trend strength if provided.
        """
        pct_off_low = metadata.get("trend_start_pct") or pattern.get("trend_start_pct")
        if pct_off_low is not None:
            return _clamp(pct_off_low / 30.0)

        trend_days = metadata.get("trend_days") or pattern.get("trend_days") or 0
        return 0.8 if trend_days >= 30 else 0.5 if trend_days >= 15 else 0.2

    def _score_trend_quality(self, pattern: Dict[str, Any], metadata: Dict[str, Any]) -> float:
        """Favor clean, higher-high/higher-low trends or high confidence detectors."""
        strength = (
            metadata.get("trend_strength")
            or metadata.get("trend_quality")
            or pattern.get("confidence")
            or 0.0
        )
        return _clamp(strength)

    def _score_flat_base(self, pattern: Dict[str, Any], metadata: Dict[str, Any]) -> float:
        """Prefer shallow consolidations with reasonable duration."""
        depth_pct = metadata.get("base_depth_pct") or pattern.get("base_depth_pct")
        if depth_pct is not None:
            # Sweet spot: 5-25% depth
            if 0.05 <= depth_pct <= 0.25:
                return _clamp(1 - abs(depth_pct - 0.15) / 0.2)
            return _clamp(depth_pct)

        width = pattern.get("width") or metadata.get("width") or 0
        return _clamp(min(width, 60) / 60.0)

    def _score_hcr(self, pattern: Dict[str, Any], metadata: Dict[str, Any]) -> float:
        """High/close relationship: closes near highs score better."""
        hcr = metadata.get("hcr") or pattern.get("hcr")
        if hcr is not None:
            return _clamp(hcr)

        close = pattern.get("current_price") or pattern.get("close")
        high = metadata.get("recent_high") or pattern.get("recent_high")
        if high and close:
            return _clamp((close or 0) / high)

        return 0.0

    def _score_yearly_range(self, pattern: Dict[str, Any], metadata: Dict[str, Any]) -> float:
        """Check where current price sits relative to the yearly range."""
        current = pattern.get("current_price") or pattern.get("close")
        year_high = metadata.get("year_high") or pattern.get("year_high")
        year_low = metadata.get("year_low") or pattern.get("year_low")

        if current and year_high and year_low and year_high > year_low:
            position = (current - year_low) / (year_high - year_low)
            # Bias toward upper half of the yearly range
            return _clamp(position)

        return 0.0

    def _score_pattern_height(self, pattern: Dict[str, Any], metadata: Dict[str, Any]) -> float:
        """Reward patterns with proportional height/depth."""
        height_pct = (
            pattern.get("height_pct")
            or metadata.get("height_pct")
            or pattern.get("pattern_height_pct")
        )
        if height_pct is None:
            return 0.0

        # Ideal depth around 10-20%
        return _clamp(1 - abs(height_pct - 0.15) / 0.2)

    def _score_volume(self, pattern: Dict[str, Any], metadata: Dict[str, Any]) -> float:
        """Declining volume through the base is constructive."""
        slope = metadata.get("volume_trend") or pattern.get("volume_trend_slope")
        if slope is None:
            return 0.5 if pattern.get("volume") else 0.0

        # Negative slope (declining volume) scores higher
        return _clamp((-slope) / 5.0 + 0.5)

    def _score_throwback(self, metadata: Dict[str, Any]) -> float:
        """Reward orderly pullbacks/throwbacks after breakout."""
        throwback_pct = metadata.get("throwback_pct")
        if throwback_pct is None:
            return 0.0
        return _clamp(1 - throwback_pct / 0.15)

    def _score_breakout_gap(self, pattern: Dict[str, Any], metadata: Dict[str, Any]) -> float:
        """Gap ups on breakout add conviction."""
        gap_pct = metadata.get("breakout_gap_pct") or pattern.get("breakout_gap_pct")
        if gap_pct is None:
            return 0.0
        return _clamp(gap_pct / 0.1)

    def _score_market_cap(self, pattern: Dict[str, Any]) -> float:
        """Simple liquidity check based on market cap (favor mid/large caps)."""
        cap = pattern.get("market_cap")
        if cap is None:
            return 0.5  # Neutral if unknown
        # Normalize around $500M - $500B
        billions = cap / 1_000_000_000
        return _clamp((np.log10(billions + 1) / 3))
