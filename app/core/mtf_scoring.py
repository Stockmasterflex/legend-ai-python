"""
MTF Scoring System
Scores patterns and setups based on multi-timeframe alignment
"""
import logging
from typing import Dict, List, Tuple
from dataclasses import dataclass

from app.core.mtf_analyzer import TimeframeData, MTFAlignment, MTFDivergence

logger = logging.getLogger(__name__)


@dataclass
class MTFScore:
    """Multi-Timeframe Score Result"""
    overall_score: float  # 0-10
    category: str  # "Excellent", "Good", "Fair", "Poor", "Very Poor"

    # Component scores
    trend_alignment_score: float  # 0-10
    momentum_score: float  # 0-10
    volume_score: float  # 0-10
    pattern_score: float  # 0-10

    # Detailed breakdown
    score_breakdown: Dict[str, float]
    scoring_notes: List[str]


class MTFScoringEngine:
    """
    Advanced MTF Scoring Engine

    Scores setups on a 0-10 scale:
    - 10: All timeframes bullish, strong trends, high volume
    - 8-9: Strong alignment, minor conflicts
    - 6-7: Good alignment, some mixed signals
    - 4-5: Mixed signals, neutral
    - 2-3: Poor alignment, conflicting signals
    - 0-1: All timeframes bearish, strong downtrends
    """

    # Score categories
    SCORE_CATEGORIES = {
        (9.0, 10.0): "Excellent",
        (7.5, 9.0): "Good",
        (5.5, 7.5): "Fair",
        (3.0, 5.5): "Poor",
        (0.0, 3.0): "Very Poor"
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def calculate_mtf_score(
        self,
        timeframe_data: Dict[str, TimeframeData],
        alignment: MTFAlignment,
        divergences: List[MTFDivergence]
    ) -> MTFScore:
        """
        Calculate comprehensive MTF score

        Args:
            timeframe_data: Dictionary of TimeframeData
            alignment: MTF alignment analysis
            divergences: List of detected divergences

        Returns:
            MTFScore with detailed breakdown
        """
        # Calculate component scores
        trend_score = self._score_trend_alignment(timeframe_data, alignment)
        momentum_score = self._score_momentum(timeframe_data)
        volume_score = self._score_volume(timeframe_data)
        pattern_score = self._score_patterns(timeframe_data)

        # Apply divergence adjustments
        divergence_adjustment = self._calculate_divergence_adjustment(divergences)

        # Calculate weighted overall score
        overall_score = (
            trend_score * 0.40 +      # Trend alignment is most important
            momentum_score * 0.25 +    # Momentum indicators
            volume_score * 0.20 +      # Volume confirmation
            pattern_score * 0.15       # Pattern quality
        )

        # Apply divergence adjustment
        overall_score = max(0.0, min(10.0, overall_score + divergence_adjustment))

        # Determine category
        category = self._get_score_category(overall_score)

        # Build score breakdown
        score_breakdown = {
            "Trend Alignment": trend_score,
            "Momentum": momentum_score,
            "Volume": volume_score,
            "Patterns": pattern_score,
            "Divergence Adj": divergence_adjustment,
            "Overall": overall_score
        }

        # Generate scoring notes
        scoring_notes = self._generate_scoring_notes(
            timeframe_data, alignment, divergences,
            trend_score, momentum_score, volume_score, pattern_score
        )

        return MTFScore(
            overall_score=round(overall_score, 1),
            category=category,
            trend_alignment_score=round(trend_score, 1),
            momentum_score=round(momentum_score, 1),
            volume_score=round(volume_score, 1),
            pattern_score=round(pattern_score, 1),
            score_breakdown=score_breakdown,
            scoring_notes=scoring_notes
        )

    def _score_trend_alignment(
        self,
        timeframe_data: Dict[str, TimeframeData],
        alignment: MTFAlignment
    ) -> float:
        """
        Score trend alignment across timeframes (0-10)

        10 = All timeframes aligned in strong uptrend
        5 = Mixed/neutral
        0 = All timeframes aligned in strong downtrend
        """
        base_score = alignment.alignment_score

        # Bonus for perfect alignment
        if alignment.alignment_type == "all_bullish":
            base_score = min(10.0, base_score + 1.0)

        # Penalty for conflicts
        if len(alignment.conflicts) > 0:
            base_score = max(0.0, base_score - len(alignment.conflicts) * 0.5)

        # Bonus for higher timeframe agreement
        if alignment.trend_agreement:
            base_score = min(10.0, base_score + 0.5)

        return base_score

    def _score_momentum(self, timeframe_data: Dict[str, TimeframeData]) -> float:
        """
        Score momentum indicators across timeframes (0-10)

        Considers RSI, MACD across all timeframes
        """
        total_score = 0.0
        total_weight = 0.0

        for tf_key, tf_data in timeframe_data.items():
            tf_score = 5.0  # Neutral baseline

            # RSI scoring
            if tf_data.rsi is not None:
                if 50 <= tf_data.rsi <= 70:
                    # Bullish but not overbought
                    tf_score += 2.5
                elif 30 <= tf_data.rsi < 50:
                    # Neutral to slightly bearish
                    tf_score += 0.0
                elif tf_data.rsi > 70:
                    # Overbought - cautiously bullish
                    tf_score += 1.0
                else:
                    # Oversold - bearish but potential reversal
                    tf_score -= 1.0

            # MACD scoring
            if tf_data.macd_histogram is not None:
                if tf_data.macd_histogram > 0:
                    tf_score += 1.5
                else:
                    tf_score -= 1.5

            # Apply timeframe weight
            total_score += tf_score * tf_data.weight
            total_weight += tf_data.weight

        if total_weight > 0:
            return max(0.0, min(10.0, total_score / total_weight))
        return 5.0

    def _score_volume(self, timeframe_data: Dict[str, TimeframeData]) -> float:
        """
        Score volume confirmation across timeframes (0-10)

        Higher volume on uptrends = higher score
        """
        total_score = 0.0
        total_weight = 0.0

        for tf_key, tf_data in timeframe_data.items():
            tf_score = 5.0  # Neutral baseline

            # Volume trend scoring
            if tf_data.volume_trend == "increasing":
                if tf_data.trend_direction == "up":
                    # Volume confirming uptrend
                    tf_score = 5.0 + (tf_data.volume_strength * 5.0)
                elif tf_data.trend_direction == "down":
                    # Volume on downtrend (bearish)
                    tf_score = 5.0 - (tf_data.volume_strength * 3.0)
                else:
                    tf_score = 6.0

            elif tf_data.volume_trend == "decreasing":
                if tf_data.trend_direction == "up":
                    # Weak volume on uptrend (concerning)
                    tf_score = 4.0
                elif tf_data.trend_direction == "down":
                    # Weak volume on downtrend (less bearish)
                    tf_score = 6.0
                else:
                    tf_score = 5.0

            # Apply timeframe weight
            total_score += tf_score * tf_data.weight
            total_weight += tf_data.weight

        if total_weight > 0:
            return max(0.0, min(10.0, total_score / total_weight))
        return 5.0

    def _score_patterns(self, timeframe_data: Dict[str, TimeframeData]) -> float:
        """
        Score pattern quality across timeframes (0-10)
        """
        total_score = 0.0
        total_weight = 0.0

        for tf_key, tf_data in timeframe_data.items():
            tf_score = 5.0  # Neutral baseline

            # Pattern detection bonus
            if tf_data.pattern_detected:
                # Higher confidence = higher score
                pattern_bonus = tf_data.pattern_confidence * 5.0
                tf_score = 5.0 + pattern_bonus

            # Price position relative to SMAs
            if tf_data.price_position == "above_both":
                tf_score += 1.0
            elif tf_data.price_position == "below_both":
                tf_score -= 1.0

            # Apply timeframe weight
            total_score += tf_score * tf_data.weight
            total_weight += tf_data.weight

        if total_weight > 0:
            return max(0.0, min(10.0, total_score / total_weight))
        return 5.0

    def _calculate_divergence_adjustment(
        self,
        divergences: List[MTFDivergence]
    ) -> float:
        """
        Calculate score adjustment based on divergences

        Bullish divergences increase score
        Bearish divergences decrease score
        """
        adjustment = 0.0

        for div in divergences:
            if div.divergence_type == "bullish":
                # Bullish divergence is positive
                if div.severity == "strong":
                    adjustment += 1.5
                elif div.severity == "moderate":
                    adjustment += 1.0
                else:
                    adjustment += 0.5

            elif div.divergence_type == "bearish":
                # Bearish divergence is negative
                if div.severity == "strong":
                    adjustment -= 1.5
                elif div.severity == "moderate":
                    adjustment -= 1.0
                else:
                    adjustment -= 0.5

        # Cap adjustment at +/- 3.0
        return max(-3.0, min(3.0, adjustment))

    def _get_score_category(self, score: float) -> str:
        """Get category label for score"""
        for (min_score, max_score), category in self.SCORE_CATEGORIES.items():
            if min_score <= score < max_score:
                return category

        # Fallback
        if score >= 9.0:
            return "Excellent"
        else:
            return "Very Poor"

    def _generate_scoring_notes(
        self,
        timeframe_data: Dict[str, TimeframeData],
        alignment: MTFAlignment,
        divergences: List[MTFDivergence],
        trend_score: float,
        momentum_score: float,
        volume_score: float,
        pattern_score: float
    ) -> List[str]:
        """Generate human-readable scoring notes"""
        notes = []

        # Trend alignment notes
        if trend_score >= 8.0:
            notes.append(f"✅ Excellent trend alignment ({trend_score}/10)")
        elif trend_score >= 6.0:
            notes.append(f"✅ Good trend alignment ({trend_score}/10)")
        elif trend_score >= 4.0:
            notes.append(f"⚠️ Fair trend alignment ({trend_score}/10)")
        else:
            notes.append(f"❌ Poor trend alignment ({trend_score}/10)")

        # Alignment type
        if alignment.alignment_type == "all_bullish":
            notes.append("🎯 All timeframes bullish - STRONG BUY signal")
        elif alignment.alignment_type == "all_bearish":
            notes.append("🎯 All timeframes bearish - STRONG SELL signal")
        elif "bullish" in alignment.alignment_type:
            notes.append(f"📊 Majority bullish ({len(alignment.bullish_timeframes)}/{len(timeframe_data)} TFs)")
        elif "bearish" in alignment.alignment_type:
            notes.append(f"📊 Majority bearish ({len(alignment.bearish_timeframes)}/{len(timeframe_data)} TFs)")

        # Momentum notes
        if momentum_score >= 7.0:
            notes.append(f"💪 Strong momentum ({momentum_score}/10)")
        elif momentum_score < 4.0:
            notes.append(f"⚠️ Weak momentum ({momentum_score}/10)")

        # Volume notes
        if volume_score >= 7.0:
            notes.append(f"📈 Strong volume confirmation ({volume_score}/10)")
        elif volume_score < 4.0:
            notes.append(f"⚠️ Weak volume ({volume_score}/10)")

        # Pattern notes
        if pattern_score >= 7.0:
            notes.append(f"📐 Quality patterns detected ({pattern_score}/10)")

        # Divergence notes
        for div in divergences:
            if div.severity == "strong":
                notes.append(f"⚡ {div.description.upper()}")
            else:
                notes.append(f"📍 {div.description}")

        # Conflict warnings
        for conflict in alignment.conflicts:
            notes.append(f"⚠️ {conflict}")

        return notes

    def get_trade_recommendation(self, score: MTFScore) -> str:
        """
        Get trade recommendation based on score

        Returns: "Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"
        """
        if score.overall_score >= 8.5:
            return "Strong Buy"
        elif score.overall_score >= 7.0:
            return "Buy"
        elif score.overall_score >= 4.5:
            return "Hold"
        elif score.overall_score >= 3.0:
            return "Sell"
        else:
            return "Strong Sell"
