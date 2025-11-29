"""
Relative Strength Rating Service (Minervini SEPA Methodology)

Implements Mark Minervini's RS Rating calculation as described in
"Trade Like a Stock Market Wizard" and "Think & Trade Like a Champion".

RS Rating Scale: 0-99 (percentile rank)
- 90+: Top 10% strongest stocks (🔥)
- 70-89: Strong relative strength (🟢)
- 50-69: Above average (🟡)
- <50: Below average (⚪)

Formula:
RS = 0.4 * Q4_performance + 0.2 * Q3_performance + 0.2 * Q2_performance + 0.2 * Q1_performance
Percentile = rank among all stocks in universe (0-99)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@dataclass
class RSRating:
    """Relative Strength Rating result"""

    rs_rating: int  # 0-99 percentile rank
    raw_score: float  # Weighted performance score
    q1_performance: float  # Quarters 1 performance %
    q2_performance: float  # Quarter 2 performance %
    q3_performance: float  # Quarter 3 performance %
    q4_performance: float  # Quarter 4 (most recent) performance %
    one_year_performance: float  # Total 1-year performance %
    percentile: float  # Exact percentile (0-100)
    universe_rank: int  # Rank within universe (1 = strongest)
    universe_size: int  # Total stocks in universe
    timestamp: datetime  # When calculated

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "rs_rating": self.rs_rating,
            "raw_score": round(self.raw_score, 2),
            "q1_performance": round(self.q1_performance, 2),
            "q2_performance": round(self.q2_performance, 2),
            "q3_performance": round(self.q3_performance, 2),
            "q4_performance": round(self.q4_performance, 2),
            "one_year_performance": round(self.one_year_performance, 2),
            "percentile": round(self.percentile, 2),
            "universe_rank": self.universe_rank,
            "universe_size": self.universe_size,
            "timestamp": self.timestamp.isoformat(),
        }

    @property
    def emoji(self) -> str:
        """Get emoji indicator for RS rating"""
        if self.rs_rating >= 90:
            return "🔥"  # Top 10%
        elif self.rs_rating >= 70:
            return "🟢"  # Strong
        elif self.rs_rating >= 50:
            return "🟡"  # Above average
        else:
            return "⚪"  # Below average


class RelativeStrengthCalculator:
    """
    Calculate Minervini-style RS ratings.

    The RS rating weighs recent performance more heavily:
    - Q4 (most recent quarter): 40% weight
    - Q3 (2nd quarter back): 20% weight
    - Q2 (3rd quarter back): 20% weight
    - Q1 (oldest quarter): 20% weight
    """

    # Trading days per quarter (approximately)
    DAYS_PER_QUARTER = 63  # ~252 trading days / 4
    DAYS_PER_YEAR = 252

    # Minimum data requirements
    MIN_DAYS_FOR_RS = 252  # Need full year of data

    def __init__(self, db_session: Optional[Session] = None):
        """
        Initialize RS calculator.

        Args:
            db_session: Optional database session for storing RS history
        """
        self.db_session = db_session

    def calculate_rs_rating(
        self,
        symbol: str,
        prices: np.ndarray,
        universe_prices: Dict[str, np.ndarray],
        dates: Optional[np.ndarray] = None,
    ) -> Optional[RSRating]:
        """
        Calculate RS rating for a symbol against universe.

        Args:
            symbol: Stock symbol
            prices: Price array (typically close prices)
            universe_prices: Dict of {symbol: prices} for all universe stocks
            dates: Optional date array for validation

        Returns:
            RSRating object or None if insufficient data
        """
        # Validate input
        if len(prices) < self.MIN_DAYS_FOR_RS:
            logger.warning(
                f"{symbol}: Insufficient data ({len(prices)} days, need {self.MIN_DAYS_FOR_RS})"
            )
            return None

        # Calculate quarterly performance for this stock
        quarterly_perf = self._calculate_quarterly_performance(prices)
        if quarterly_perf is None:
            return None

        q1, q2, q3, q4 = quarterly_perf

        # Calculate weighted score (Minervini formula)
        raw_score = (
            0.4 * q4  # Most recent quarter (40% weight)
            + 0.2 * q3
            + 0.2 * q2
            + 0.2 * q1
        )

        # Calculate 1-year performance
        one_year_perf = (
            (prices[-1] - prices[-self.DAYS_PER_YEAR]) / prices[-self.DAYS_PER_YEAR]
        ) * 100

        # Calculate RS scores for entire universe
        universe_scores = self._calculate_universe_scores(universe_prices)

        # Remove the target symbol from universe if present
        if symbol in universe_scores:
            del universe_scores[symbol]

        # Rank this stock against universe
        percentile, rank = self._calculate_percentile_rank(raw_score, universe_scores)

        # Convert percentile to 0-99 scale (RS rating)
        rs_rating = int(round(percentile))

        return RSRating(
            rs_rating=rs_rating,
            raw_score=raw_score,
            q1_performance=q1,
            q2_performance=q2,
            q3_performance=q3,
            q4_performance=q4,
            one_year_performance=one_year_perf,
            percentile=percentile,
            universe_rank=rank,
            universe_size=len(universe_scores) + 1,  # +1 for target stock
            timestamp=datetime.utcnow(),
        )

    def _calculate_quarterly_performance(
        self, prices: np.ndarray
    ) -> Optional[Tuple[float, float, float, float]]:
        """
        Calculate performance for each quarter (Q1=oldest, Q4=newest).

        Returns:
            Tuple of (Q1%, Q2%, Q3%, Q4%) or None if insufficient data
        """
        if len(prices) < self.DAYS_PER_YEAR:
            return None

        # Get last 252 days
        year_prices = prices[-self.DAYS_PER_YEAR :]

        # Quarter boundaries (working backwards from most recent)
        q4_start = -self.DAYS_PER_QUARTER  # Most recent quarter
        q3_start = q4_start - self.DAYS_PER_QUARTER
        q2_start = q3_start - self.DAYS_PER_QUARTER
        q1_start = -self.DAYS_PER_YEAR  # Oldest quarter

        # Calculate performance for each quarter
        try:
            # Q4 (most recent): Days -63 to -1
            q4_perf = (
                (year_prices[-1] - year_prices[q4_start]) / year_prices[q4_start]
            ) * 100

            # Q3: Days -126 to -64
            q3_perf = (
                (year_prices[q4_start] - year_prices[q3_start]) / year_prices[q3_start]
            ) * 100

            # Q2: Days -189 to -127
            q2_perf = (
                (year_prices[q3_start] - year_prices[q2_start]) / year_prices[q2_start]
            ) * 100

            # Q1 (oldest): Days -252 to -190
            q1_perf = (
                (year_prices[q2_start] - year_prices[q1_start]) / year_prices[q1_start]
            ) * 100

            return (q1_perf, q2_perf, q3_perf, q4_perf)

        except (ZeroDivisionError, IndexError) as e:
            logger.error(f"Error calculating quarterly performance: {e}")
            return None

    def _calculate_universe_scores(
        self, universe_prices: Dict[str, np.ndarray]
    ) -> Dict[str, float]:
        """
        Calculate RS scores for all stocks in universe.

        Args:
            universe_prices: Dict of {symbol: prices}

        Returns:
            Dict of {symbol: rs_score}
        """
        scores = {}

        for symbol, prices in universe_prices.items():
            # Skip if insufficient data
            if len(prices) < self.DAYS_PER_YEAR:
                continue

            # Calculate quarterly performance
            quarterly = self._calculate_quarterly_performance(prices)
            if quarterly is None:
                continue

            q1, q2, q3, q4 = quarterly

            # Calculate weighted score
            score = 0.4 * q4 + 0.2 * q3 + 0.2 * q2 + 0.2 * q1
            scores[symbol] = score

        return scores

    def _calculate_percentile_rank(
        self, target_score: float, universe_scores: Dict[str, float]
    ) -> Tuple[float, int]:
        """
        Calculate percentile rank of target score within universe.

        Args:
            target_score: Score to rank
            universe_scores: Dict of all universe scores

        Returns:
            Tuple of (percentile 0-99, rank 1-N)
        """
        if not universe_scores:
            return (50.0, 1)  # Default to median if no universe

        # Get all scores including target
        all_scores = list(universe_scores.values()) + [target_score]
        all_scores_sorted = sorted(all_scores, reverse=True)  # Highest to lowest

        # Find rank (1 = strongest)
        rank = all_scores_sorted.index(target_score) + 1

        # Calculate percentile (0-99)
        # Percentile = (# stocks below / total stocks) * 100
        num_below = len([s for s in all_scores if s < target_score])
        percentile = (num_below / len(all_scores)) * 100

        # Ensure 0-99 range
        percentile = max(0.0, min(99.0, percentile))

        return (percentile, rank)

    def calculate_rs_simple(
        self, symbol: str, prices: np.ndarray, benchmark_prices: np.ndarray
    ) -> Optional[float]:
        """
        Simple RS calculation vs benchmark (SPY) for backward compatibility.

        This is NOT the full Minervini RS rating, just relative performance vs SPY.

        Args:
            symbol: Stock symbol
            prices: Stock price array
            benchmark_prices: Benchmark (SPY) price array

        Returns:
            RS percentage vs benchmark or None
        """
        min_len = min(len(prices), len(benchmark_prices))
        if min_len < 61:  # Need at least ~3 months
            return None

        stock_prices = prices[-min_len:]
        bench_prices = benchmark_prices[-min_len:]

        # Calculate 60-day performance
        stock_return = (
            (stock_prices[-1] - stock_prices[-61]) / stock_prices[-61]
        ) * 100
        bench_return = (
            (bench_prices[-1] - bench_prices[-61]) / bench_prices[-61]
        ) * 100

        # Relative strength = stock performance - benchmark performance
        rs = stock_return - bench_return

        return round(rs, 2)


def get_rs_emoji(rs_rating: int) -> str:
    """
    Get emoji indicator for RS rating.

    Args:
        rs_rating: RS rating 0-99

    Returns:
        Emoji string
    """
    if rs_rating >= 90:
        return "🔥"  # Top 10%
    elif rs_rating >= 70:
        return "🟢"  # Strong
    elif rs_rating >= 50:
        return "🟡"  # Above average
    else:
        return "⚪"  # Below average


def filter_by_rs_threshold(patterns: List[Dict], min_rs: int = 70) -> List[Dict]:
    """
    Filter patterns by RS rating threshold.

    Args:
        patterns: List of pattern dictionaries
        min_rs: Minimum RS rating (default 70)

    Returns:
        Filtered list of patterns
    """
    return [
        p
        for p in patterns
        if p.get("rs_rating") is not None and p["rs_rating"] >= min_rs
    ]


__all__ = [
    "RelativeStrengthCalculator",
    "RSRating",
    "get_rs_emoji",
    "filter_by_rs_threshold",
]
