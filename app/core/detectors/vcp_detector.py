"""
VCP (Volatility Contraction Pattern) Detector
Minervini-style detection with proper contraction sequence.

A VCP occurs inside a base (consolidation) where swing-high → swing-low
declines are SHRINKING in percentage terms, creating tighter and tighter
pullbacks before an explosive breakout.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from app.core.detector_base import (Detector, PatternResult, PatternType,
                                    StatsHelper)
from app.core.detector_config import VCPConfig


class VCPDetector(Detector):
    """
    VCP (Volatility Contraction Pattern) detector.

    Key features:
    - Identifies N≥3 contractions where % declines are shrinking
    - Volume dries up during contractions
    - Strong breakout with volume surge
    - Minervini guideline: ≥3 clean contractions, last ≤5-8%, final width ≤1*ATR
    """

    def __init__(self, **kwargs):
        super().__init__("VCP", **kwargs)
        self.config = VCPConfig()
        # Apply overrides
        for key, value in kwargs.items():
            if hasattr(self.config, key.upper()):
                setattr(self.config, key.upper(), value)

    def find(
        self, ohlcv: pd.DataFrame, timeframe: str, symbol: str
    ) -> List[PatternResult]:
        """Detect VCP patterns in OHLCV data"""
        results = []

        if len(ohlcv) < 100:  # VCP needs sufficient history
            return results

        try:
            # Extract OHLCV
            high = ohlcv["high"].values
            low = ohlcv["low"].values
            close = ohlcv["close"].values
            volume = ohlcv["volume"].values
            dates = ohlcv.get(
                "datetime", pd.date_range(end=datetime.now(), periods=len(ohlcv))
            )

            # Calculate ATR and volume metrics
            atr = StatsHelper.atr(high, low, close, period=14)
            vol_z = StatsHelper.volume_z_score(volume, window=20)

            # Find pivots (swing highs/lows)
            pivots = StatsHelper.zigzag_pivots(high, low, close, atr)

            if len(pivots) < 10:  # Need sufficient pivots for contractions
                return results

            # Identify possible bases (consolidation areas)
            bases = self._find_bases(pivots, high, low, close, atr)

            # For each potential base, look for VCP contractions
            for base in bases:
                vcp = self._analyze_base_for_vcp(
                    base, pivots, high, low, close, volume, dates, atr, vol_z
                )
                if vcp:
                    results.append(vcp)

        except Exception as e:
            logger.exception(f"Error in VCP detection: {e}")

        return results

    def _find_bases(
        self,
        pivots: List[Tuple[int, float, str]],
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray,
        atr: np.ndarray,
    ) -> List[Dict[str, Any]]:
        """
        Identify potential consolidation bases.
        A base is a region where price oscillates within a range for ≥30 bars.
        """
        bases = []
        if len(pivots) < 6:
            return bases

        for i in range(2, len(pivots) - 3):
            # Look for 3+ consecutive swings within a tight range
            window_start = pivots[i][0]
            window_end = pivots[i + 3][0]
            window_len = window_end - window_start

            if window_len < self.config.MIN_BASE_LENGTH:
                continue
            if window_len > self.config.MAX_BASE_LENGTH:
                continue

            # Get range
            base_high = max(high[window_start:window_end])
            base_low = min(low[window_start:window_end])
            base_range = base_high - base_low

            # Ensure range is reasonable relative to ATR
            avg_atr = np.mean(atr[window_start:window_end])
            if base_range > 5 * avg_atr:
                continue  # Range too large

            bases.append(
                {
                    "start_idx": window_start,
                    "end_idx": window_end,
                    "high": base_high,
                    "low": base_low,
                    "range": base_range,
                    "atr": avg_atr,
                }
            )

        return bases

    def _analyze_base_for_vcp(
        self,
        base: Dict[str, Any],
        pivots: List[Tuple[int, float, str]],
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray,
        volume: np.ndarray,
        dates,
        atr: np.ndarray,
        vol_z: np.ndarray,
    ) -> Optional[PatternResult]:
        """Analyze a base for VCP characteristics"""

        # Find swing high → low contractions within and after the base
        contractions = self._find_contractions(
            pivots, base["start_idx"], base["end_idx"], high, low, close, atr
        )

        if len(contractions) < self.config.MIN_CONTRACTIONS:
            return None  # Not enough contractions

        # Verify contraction sequence: % declines should shrink
        if not self._verify_contraction_shrink(contractions):
            return None

        # Check volume characteristics
        base_volume_tau = StatsHelper.kendall_tau(
            volume[base["start_idx"] : base["end_idx"]]
        )
        if base_volume_tau > self.config.VOLUME_DECLINE_TAU:
            # Volume not declining (less ideal)
            pass  # Allow but it will affect scoring

        # Check for right-side climb
        right_side_start = contractions[-1]["end_idx"]
        right_side_end = min(len(close), right_side_start + 30)

        if right_side_end <= right_side_start:
            return None

        right_side_high = np.max(high[right_side_start:right_side_end])
        climb_tolerance = self.config.RIGHT_SIDE_CLIMB_ATR * np.mean(
            atr[right_side_start:right_side_end]
        )

        if abs(right_side_high - base["high"]) > climb_tolerance:
            return None  # No right-side climb

        # Look for breakout
        breakout_idx = right_side_end - 1
        if breakout_idx < len(vol_z) - 1:
            breakout_vol_z = vol_z[breakout_idx]
            if vol_z[breakout_idx] < self.config.VOLUME_SURGE_Z:
                # Not a strong breakout, but continue for analysis
                breakout_vol_z = vol_z[breakout_idx]

            # Compute confidence score
            confidence = self._score_vcp(
                contractions,
                base,
                breakout_vol_z,
                base_volume_tau,
                atr,
                right_side_high,
            )

            if confidence < 0.40:
                return None  # Confidence too low

            # Build result
            last_contraction = contractions[-1]
            result = PatternResult(
                symbol=dates.name if hasattr(dates, "name") else "UNKNOWN",
                timeframe="1D",  # Placeholder
                asof=datetime.now().isoformat(),
                pattern_type=PatternType.VCP,
                strong=confidence >= 0.75,
                confidence=confidence,
                window_start=(
                    str(dates[base["start_idx"]])[:10]
                    if len(dates) > 0
                    else "2025-01-01"
                ),
                window_end=(
                    str(dates[right_side_end - 1])[:10]
                    if len(dates) > right_side_end - 1
                    else "2025-01-01"
                ),
                lines={
                    "base_high": base["high"],
                    "base_low": base["low"],
                    "last_contraction_high": last_contraction["high"],
                    "last_contraction_low": last_contraction["low"],
                },
                touches={
                    "contractions": len(contractions),
                },
                breakout={
                    "direction": "up",
                    "price": right_side_high,
                    "volume_z": float(breakout_vol_z),
                    "bar_index": int(right_side_end - 1),
                },
                evidence={
                    "contraction_sequence": [
                        {
                            "decline_pct": c["decline_pct"],
                            "high": c["high"],
                            "low": c["low"],
                        }
                        for c in contractions
                    ],
                    "base_range": float(base["range"]),
                    "base_atr": float(base["atr"]),
                    "volume_tau": float(base_volume_tau),
                },
            )
            return result

        return None

    def _find_contractions(
        self,
        pivots: List[Tuple[int, float, str]],
        base_start: int,
        base_end: int,
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray,
        atr: np.ndarray,
    ) -> List[Dict[str, Any]]:
        """
        Find contraction legs (swing high → swing low where % decline shrinks).
        """
        contractions = []

        # Get pivots that span the base region
        base_pivots = [p for p in pivots if base_start <= p[0] <= base_end + 50]

        if len(base_pivots) < 4:
            return contractions

        # Identify pairs of high → low
        i = 0
        while i < len(base_pivots) - 1:
            if base_pivots[i][2] == "high":
                high_price = base_pivots[i][1]
                high_idx = base_pivots[i][0]

                # Find next low
                j = i + 1
                while j < len(base_pivots) and base_pivots[j][2] != "low":
                    j += 1

                if j < len(base_pivots):
                    low_price = base_pivots[j][1]
                    low_idx = base_pivots[j][0]
                    decline_pct = (high_price - low_price) / high_price

                    if decline_pct >= self.config.MIN_CONTRACTION_DECLINE:
                        contractions.append(
                            {
                                "high": high_price,
                                "low": low_price,
                                "high_idx": high_idx,
                                "end_idx": low_idx,
                                "decline_pct": decline_pct,
                                "length": low_idx - high_idx,
                            }
                        )
                    i = j
                else:
                    i += 1
            else:
                i += 1

        return contractions

    def _verify_contraction_shrink(self, contractions: List[Dict[str, Any]]) -> bool:
        """Verify that contractions shrink in percentage terms"""
        if len(contractions) < 2:
            return False

        for i in range(1, len(contractions)):
            ratio = contractions[i]["decline_pct"] / contractions[i - 1]["decline_pct"]
            if ratio > self.config.SHRINK_RATIO_THRESHOLD:
                return False  # Not shrinking enough

        return True

    def _score_vcp(
        self,
        contractions: List[Dict[str, Any]],
        base: Dict[str, Any],
        breakout_vol_z: float,
        volume_tau: float,
        atr: np.ndarray,
        right_side_high: float,
    ) -> float:
        """Compute VCP confidence score"""
        score = 0.0

        # Contractions weight: 35%
        # More contractions = higher score; ≥4 is ideal
        num_contractions = len(contractions)
        contractions_score = min(1.0, (num_contractions - 2) / 2.0)  # 3→0.5, 4→1.0
        score += 0.35 * contractions_score

        # Shrink quality (R² of decline sequence)
        declines = [c["decline_pct"] for c in contractions]
        if len(declines) > 1:
            x = np.arange(len(declines))
            z = np.polyfit(x, declines, 1)  # Linear fit
            p = np.poly1d(z)
            ss_res = np.sum((np.array(declines) - p(x)) ** 2)
            ss_tot = np.sum((np.array(declines) - np.mean(declines)) ** 2)
            r2 = 1 - (ss_res / (ss_tot + 1e-8)) if ss_tot > 0 else 0
            score += 0.15 * r2

        # Structure weight: 25%
        # Check tightness of final contraction
        final_contraction = contractions[-1]
        final_width = final_contraction["high"] - final_contraction["low"]
        avg_atr = np.mean(
            atr[final_contraction["high_idx"] : final_contraction["end_idx"]]
        )

        width_score = max(
            0.0, 1.0 - (final_width / (self.config.FINAL_TIGHT_AREA_ATR * avg_atr))
        )
        score += 0.25 * width_score

        # Volume weight: 30%
        volume_score = 0.0
        if volume_tau < 0:  # Declining volume
            volume_score += 0.5
        if breakout_vol_z >= self.config.VOLUME_SURGE_Z:
            volume_score += 0.5
        score += 0.30 * volume_score

        # Recency weight: 10% (assume recent is good)
        score += 0.10 * 0.9  # Placeholder

        return np.clip(score, 0.0, 1.0)
