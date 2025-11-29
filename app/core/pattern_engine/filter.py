"""
Pattern filtering utilities that mirror Patternz FilterForm behavior.

This module adapts the checkbox/radio-button logic from Patternz
(`FilterForm.cs` and ListForm `FilterPatterns`) to work with the
Python pattern dictionaries returned by the Legend AI detectors.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List, Optional, Sequence

logger = logging.getLogger(__name__)


class PatternFilter:
    """
    Apply post-detection filters such as width, price, volume, height,
    breakout direction, and Weinstein stage. The methods intentionally
    mirror the semantics used in Patternz' filter UI.
    """

    # ---- Individual filters -------------------------------------------------
    def filter_by_width(
        self,
        patterns: Iterable[Dict[str, Any]],
        min_days: Optional[float] = None,
        max_days: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Keep patterns whose width is between min_days and max_days.

        Patternz logic:
        - "Less than" rejects widths >= threshold
        - "More than" rejects widths <= threshold
        - "Between" rejects widths <= low or >= high
        """
        if min_days is None and max_days is None:
            return list(patterns)

        filtered: List[Dict[str, Any]] = []
        for pat in patterns:
            width = self._get_width(pat)
            if width is None:
                logger.debug("Skipping width filter for pattern with no width: %s", pat.get("pattern"))
                continue

            if max_days is not None and width >= max_days:
                continue
            if min_days is not None and width <= min_days:
                continue
            filtered.append(pat)

        return filtered

    def filter_by_price(
        self,
        patterns: Iterable[Dict[str, Any]],
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Keep patterns whose current/last price is between the thresholds.

        Patternz logic:
        - "Less than" rejects prices >= threshold
        - "More than" rejects prices <= threshold
        - "Between" rejects prices <= low or >= high
        """
        if min_price is None and max_price is None:
            return list(patterns)

        filtered: List[Dict[str, Any]] = []
        for pat in patterns:
            price = self._get_price(pat)
            if price is None:
                logger.debug("Missing price; filtering out pattern %s", pat.get("pattern"))
                continue

            if max_price is not None and price >= max_price:
                continue
            if min_price is not None and price <= min_price:
                continue
            filtered.append(pat)

        return filtered

    def filter_by_volume(
        self,
        patterns: Iterable[Dict[str, Any]],
        threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Keep patterns whose average/recent volume exceeds threshold.

        Patternz logic:
        - Reject if user threshold >= pattern's average volume.
        """
        if threshold is None:
            return list(patterns)

        filtered: List[Dict[str, Any]] = []
        for pat in patterns:
            volume = self._get_volume(pat)
            if volume is None:
                logger.debug("Missing volume; filtering out pattern %s", pat.get("pattern"))
                continue

            if threshold >= volume:
                continue
            filtered.append(pat)

        return filtered

    def filter_by_height(
        self,
        patterns: Iterable[Dict[str, Any]],
        min_pct: Optional[float] = None,
        max_pct: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Keep patterns whose height (as % of price) falls in the range.

        Patternz logic classifies heights (tall/short); here we mirror
        the intent with a percentage-based range check using whatever
        height data is available in the pattern dictionary.
        """
        if min_pct is None and max_pct is None:
            return list(patterns)

        filtered: List[Dict[str, Any]] = []
        for pat in patterns:
            height_pct = self._get_height_pct(pat)
            if height_pct is None:
                logger.debug("Missing height; filtering out pattern %s", pat.get("pattern"))
                continue

            if max_pct is not None and height_pct >= max_pct:
                continue
            if min_pct is not None and height_pct <= min_pct:
                continue
            filtered.append(pat)

        return filtered

    def filter_by_breakout_direction(
        self,
        patterns: Iterable[Dict[str, Any]],
        direction: Optional[str] = None,
        include_none: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Keep patterns matching a breakout direction.

        Args:
            direction: 'up', 'down', 'both'/'either', 'none'/'pending', or None for no filter.
            include_none: If True, patterns with no breakout direction are included
                (matches the 'Include no breakout yet' checkbox in Patternz).
        """
        if direction is None:
            return list(patterns)

        direction = direction.lower()
        filtered: List[Dict[str, Any]] = []
        for pat in patterns:
            pat_dir = self._normalize_direction(pat)

            if pat_dir is None:
                if include_none or direction in {"none", "pending"}:
                    filtered.append(pat)
                continue

            if direction in {"both", "either"} and pat_dir in {"up", "down"}:
                filtered.append(pat)
            elif direction in {"none", "pending"} and pat_dir in {"none", "pending"}:
                filtered.append(pat)
            elif pat_dir == direction:
                filtered.append(pat)
            elif include_none and pat_dir in {"none", "pending"}:
                filtered.append(pat)

        return filtered

    def filter_by_stage(
        self,
        patterns: Iterable[Dict[str, Any]],
        weinstein_stage: Optional[Sequence[int] | int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Keep patterns that belong to the requested Weinstein stage(s).
        """
        if weinstein_stage is None:
            return list(patterns)

        allowed = {weinstein_stage} if isinstance(weinstein_stage, int) else set(weinstein_stage)

        filtered: List[Dict[str, Any]] = []
        for pat in patterns:
            stage = self._get_stage(pat)
            if stage is None:
                logger.debug("Missing stage; filtering out pattern %s", pat.get("pattern"))
                continue
            if stage in allowed:
                filtered.append(pat)

        return filtered

    # ---- Composite application ---------------------------------------------
    def apply_filters(
        self,
        patterns: Iterable[Dict[str, Any]],
        filter_config: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Apply all enabled filters to a pattern list.

        Supported filter_config keys (all optional):
        - use_filters: master switch (default True)
        - min_width / max_width: width limits (days)
        - min_price / max_price: price limits
        - min_volume: average/recent volume threshold
        - min_height_pct / max_height_pct: height as percent of price
        - breakout_direction: 'up' | 'down' | 'both' | 'none'
        - include_no_breakout: bool, include patterns with no breakout info
        - stage: int or iterable of Weinstein stages (1-4)
        """
        if filter_config is None:
            filter_config = {}

        if not filter_config.get("use_filters", True):
            return list(patterns)

        filtered = list(patterns)

        filtered = self.filter_by_width(
            filtered,
            min_days=filter_config.get("min_width"),
            max_days=filter_config.get("max_width"),
        )
        filtered = self.filter_by_price(
            filtered,
            min_price=filter_config.get("min_price"),
            max_price=filter_config.get("max_price"),
        )
        filtered = self.filter_by_volume(
            filtered,
            threshold=filter_config.get("min_volume"),
        )
        filtered = self.filter_by_height(
            filtered,
            min_pct=filter_config.get("min_height_pct"),
            max_pct=filter_config.get("max_height_pct"),
        )
        filtered = self.filter_by_breakout_direction(
            filtered,
            direction=filter_config.get("breakout_direction"),
            include_none=filter_config.get("include_no_breakout", True),
        )
        filtered = self.filter_by_stage(
            filtered,
            weinstein_stage=filter_config.get("stage"),
        )

        return filtered

    # ---- Helper extraction methods -----------------------------------------
    def _get_width(self, pattern: Dict[str, Any]) -> Optional[float]:
        """Resolve width from common pattern fields."""
        width = pattern.get("width")
        if width is None and {"start_idx", "end_idx"} <= pattern.keys():
            try:
                width = (pattern["end_idx"] - pattern["start_idx"]) + 1
            except Exception:
                width = None

        if width is None and "cup_width" in pattern:
            width = pattern.get("cup_width")

        try:
            return float(width) if width is not None else None
        except (TypeError, ValueError):
            return None

    def _get_price(self, pattern: Dict[str, Any]) -> Optional[float]:
        """Resolve current/last price from common fields."""
        for key in (
            "current_price",
            "price",
            "close",
            "last_close",
            "entry",
            "target",
        ):
            if key in pattern and pattern[key] not in (None, 0):
                try:
                    return float(pattern[key])
                except (TypeError, ValueError):
                    continue
        return None

    def _get_volume(self, pattern: Dict[str, Any]) -> Optional[float]:
        """Resolve average volume from common fields."""
        for key in (
            "avg_volume",
            "average_volume",
            "volume",
            "vol",
            "recent_volume",
        ):
            if key in pattern and pattern[key] not in (None, 0):
                try:
                    return float(pattern[key])
                except (TypeError, ValueError):
                    continue
        return None

    def _get_height_pct(self, pattern: Dict[str, Any]) -> Optional[float]:
        """Estimate pattern height as a percentage of price."""
        height = pattern.get("height")
        if height is None:
            # Try other semantic equivalents
            for key in ("cup_depth", "depth", "range"):
                if key in pattern:
                    height = pattern.get(key)
                    break

        base_price = self._get_price(pattern)

        # If missing height but we have two bounds, derive it
        if height is None:
            bounds = [
                ("resistance", "support"),
                ("resistance_start", "support_start"),
                ("resistance_end", "support_end"),
            ]
            for high_key, low_key in bounds:
                high = pattern.get(high_key)
                low = pattern.get(low_key)
                if high is not None and low is not None:
                    try:
                        height = float(high) - float(low)
                        if base_price is None:
                            base_price = max(float(high), float(low))
                        break
                    except (TypeError, ValueError):
                        continue

        try:
            height_val = float(height) if height is not None else None
        except (TypeError, ValueError):
            height_val = None

        if height_val is None or base_price in (None, 0):
            return None

        return abs(height_val) / float(base_price) * 100.0

    def _normalize_direction(self, pattern: Dict[str, Any]) -> Optional[str]:
        """Normalize breakout direction strings to 'up', 'down', 'none', or 'pending'."""
        for key in ("breakout_direction", "bkout_direction", "direction"):
            if key in pattern and pattern[key] is not None:
                value = str(pattern[key]).strip().lower()
                if value in {"up", "down", "none", "pending"}:
                    return value
                if value in {"na", "n/a", ""}:
                    return "none"
        return None

    def _get_stage(self, pattern: Dict[str, Any]) -> Optional[int]:
        """Extract Weinstein stage if present."""
        for key in ("stage", "weinstein_stage"):
            if key in pattern and pattern[key] not in (None, ""):
                try:
                    return int(pattern[key])
                except (TypeError, ValueError):
                    continue
        return None
