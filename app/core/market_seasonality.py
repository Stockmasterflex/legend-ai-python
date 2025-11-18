"""
Market Patterns and Seasonality Analysis

This module provides comprehensive analysis of historical patterns and seasonality effects
including seasonal trends, election cycles, options expiration, earnings patterns, and
market cycle detection.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
import statistics
import math
from collections import defaultdict


class MarketRegime(Enum):
    """Market regime classifications"""
    BULL_STRONG = "bull_strong"
    BULL_WEAK = "bull_weak"
    BEAR_STRONG = "bear_strong"
    BEAR_WEAK = "bear_weak"
    ACCUMULATION = "accumulation"
    DISTRIBUTION = "distribution"
    SIDEWAYS = "sideways"
    UNKNOWN = "unknown"


class ElectionCyclePhase(Enum):
    """Presidential election cycle phases"""
    PRE_ELECTION = "pre_election"
    POST_ELECTION = "post_election"
    MID_TERM_PRE = "mid_term_pre"
    MID_TERM_POST = "mid_term_post"
    YEAR_1 = "year_1"  # Post-election year
    YEAR_2 = "year_2"  # Mid-term year
    YEAR_3 = "year_3"  # Pre-election year
    YEAR_4 = "year_4"  # Election year


@dataclass
class SeasonalPattern:
    """Results of seasonal pattern analysis"""
    best_months: List[Tuple[str, float]]  # Month name and avg return
    worst_months: List[Tuple[str, float]]
    best_quarters: List[Tuple[str, float]]
    worst_quarters: List[Tuple[str, float]]
    best_weeks_of_month: List[Tuple[int, float]]  # Week number and avg return
    worst_weeks_of_month: List[Tuple[int, float]]
    best_days_of_week: List[Tuple[str, float]]
    worst_days_of_week: List[Tuple[str, float]]
    monthly_stats: Dict[str, Dict[str, float]]  # Month -> {mean, std, win_rate, etc}
    quarterly_stats: Dict[str, Dict[str, float]]
    week_of_month_stats: Dict[int, Dict[str, float]]
    day_of_week_stats: Dict[str, Dict[str, float]]
    current_month_rank: int  # 1-12, where 1 is best
    current_quarter_rank: int  # 1-4
    current_week_rank: int  # 1-5
    current_day_rank: int  # 1-5


@dataclass
class ElectionCycleAnalysis:
    """Election cycle performance analysis"""
    current_phase: ElectionCyclePhase
    years_until_election: int
    phase_performance: Dict[ElectionCyclePhase, Dict[str, float]]
    current_phase_avg_return: float
    current_phase_volatility: float
    pre_election_pattern: bool  # True if showing pre-election strength
    post_election_pattern: bool  # True if showing post-election weakness
    policy_impact_score: float  # 0-10 score for policy-driven volatility
    historical_accuracy: float  # How often the pattern holds


@dataclass
class OptionsExpirationAnalysis:
    """Options expiration effects analysis"""
    is_opex_week: bool
    days_to_opex: int
    is_triple_witching: bool  # Third Friday of March, June, Sept, Dec
    opex_drift_pattern: str  # "bullish", "bearish", "neutral"
    pre_opex_avg_return: float
    post_opex_avg_return: float
    opex_week_volatility: float
    pin_risk_levels: Dict[float, float]  # Strike -> probability
    max_pain_price: Optional[float]
    gamma_exposure: Optional[float]


@dataclass
class EarningsSeasonAnalysis:
    """Earnings season pattern analysis"""
    current_season: str  # "Q1", "Q2", "Q3", "Q4"
    is_peak_earnings_week: bool
    days_into_season: int
    season_performance: Dict[str, Dict[str, float]]  # Season -> stats
    pre_announcement_drift: float  # Avg drift before earnings
    post_announcement_drift: float  # Avg drift after earnings
    beat_rate_this_season: Optional[float]  # % of beats so far
    sector_rotation_signal: Dict[str, str]  # Sector -> "accumulate"/"distribute"/"hold"
    earnings_volatility_premium: float


@dataclass
class MarketCycleDetection:
    """Market cycle and regime detection"""
    current_regime: MarketRegime
    regime_confidence: float  # 0-100
    days_in_regime: int
    regime_history: List[Tuple[datetime, MarketRegime]]  # Last N regime changes
    bull_bear_score: float  # -100 (bear) to +100 (bull)
    accumulation_distribution_score: float  # -100 (distribution) to +100 (accumulation)
    trend_strength: float  # 0-100
    volatility_regime: str  # "low", "normal", "high", "extreme"
    transition_probability: Dict[MarketRegime, float]  # Probability of transitioning
    support_levels: List[float]
    resistance_levels: List[float]


@dataclass
class ComprehensiveSeasonalityReport:
    """Complete seasonality and patterns report"""
    ticker: str
    analysis_date: datetime
    seasonal_patterns: SeasonalPattern
    election_cycle: ElectionCycleAnalysis
    options_expiration: OptionsExpirationAnalysis
    earnings_season: EarningsSeasonAnalysis
    market_cycle: MarketCycleDetection
    composite_score: float  # Overall seasonality favorability score
    key_insights: List[str]
    warnings: List[str]


class MarketSeasonalityAnalyzer:
    """
    Comprehensive market seasonality and historical pattern analyzer
    """

    # Constants
    MONTH_NAMES = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    QUARTER_NAMES = ["Q1", "Q2", "Q3", "Q4"]

    # Triple witching months (March, June, September, December)
    TRIPLE_WITCHING_MONTHS = [3, 6, 9, 12]

    def __init__(self):
        """Initialize the analyzer"""
        pass

    async def analyze_complete_seasonality(
        self,
        ticker: str,
        price_data: Dict[str, Any],
        dates: List[datetime],
        current_date: Optional[datetime] = None,
        options_data: Optional[Dict[str, Any]] = None,
        earnings_dates: Optional[List[datetime]] = None
    ) -> ComprehensiveSeasonalityReport:
        """
        Perform comprehensive seasonality analysis

        Args:
            ticker: Stock symbol
            price_data: OHLCV data
            dates: Corresponding dates for price data
            current_date: Date of analysis (defaults to now)
            options_data: Optional options chain data
            earnings_dates: Optional historical earnings dates

        Returns:
            Complete seasonality report
        """
        if current_date is None:
            current_date = datetime.now()

        # Extract price data
        closes = price_data.get("c", [])
        highs = price_data.get("h", [])
        lows = price_data.get("l", [])
        volumes = price_data.get("v", [])

        # Analyze each component
        seasonal_patterns = self.analyze_seasonal_patterns(closes, dates, current_date)
        election_cycle = self.analyze_election_cycle(closes, dates, current_date)
        options_expiration = self.analyze_options_expiration(
            closes, dates, current_date, options_data
        )
        earnings_season = self.analyze_earnings_season(
            closes, dates, current_date, earnings_dates
        )
        market_cycle = self.detect_market_cycle(
            closes, highs, lows, volumes, dates, current_date
        )

        # Calculate composite score
        composite_score = self._calculate_composite_score(
            seasonal_patterns, election_cycle, options_expiration,
            earnings_season, market_cycle
        )

        # Generate insights and warnings
        insights, warnings = self._generate_insights_and_warnings(
            seasonal_patterns, election_cycle, options_expiration,
            earnings_season, market_cycle
        )

        return ComprehensiveSeasonalityReport(
            ticker=ticker,
            analysis_date=current_date,
            seasonal_patterns=seasonal_patterns,
            election_cycle=election_cycle,
            options_expiration=options_expiration,
            earnings_season=earnings_season,
            market_cycle=market_cycle,
            composite_score=composite_score,
            key_insights=insights,
            warnings=warnings
        )

    def analyze_seasonal_patterns(
        self,
        closes: List[float],
        dates: List[datetime],
        current_date: datetime
    ) -> SeasonalPattern:
        """
        Analyze seasonal patterns (monthly, quarterly, weekly, daily)
        """
        if len(closes) < 252:  # Need at least 1 year of data
            return self._empty_seasonal_pattern()

        # Calculate returns
        returns = self._calculate_returns(closes)

        # Monthly analysis
        monthly_returns = self._group_by_month(returns, dates)
        monthly_stats = self._calculate_period_stats(monthly_returns)
        best_months = sorted(
            [(self.MONTH_NAMES[i], monthly_stats[self.MONTH_NAMES[i]]["mean"])
             for i in range(12)],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        worst_months = sorted(
            [(self.MONTH_NAMES[i], monthly_stats[self.MONTH_NAMES[i]]["mean"])
             for i in range(12)],
            key=lambda x: x[1]
        )[:3]

        # Quarterly analysis
        quarterly_returns = self._group_by_quarter(returns, dates)
        quarterly_stats = self._calculate_period_stats(quarterly_returns)
        best_quarters = sorted(
            [(self.QUARTER_NAMES[i], quarterly_stats[self.QUARTER_NAMES[i]]["mean"])
             for i in range(4)],
            key=lambda x: x[1],
            reverse=True
        )[:2]
        worst_quarters = sorted(
            [(self.QUARTER_NAMES[i], quarterly_stats[self.QUARTER_NAMES[i]]["mean"])
             for i in range(4)],
            key=lambda x: x[1]
        )[:2]

        # Week of month analysis
        week_of_month_returns = self._group_by_week_of_month(returns, dates)
        week_of_month_stats = self._calculate_period_stats(week_of_month_returns)
        best_weeks = sorted(
            [(week, week_of_month_stats[week]["mean"])
             for week in week_of_month_stats.keys()],
            key=lambda x: x[1],
            reverse=True
        )[:2]
        worst_weeks = sorted(
            [(week, week_of_month_stats[week]["mean"])
             for week in week_of_month_stats.keys()],
            key=lambda x: x[1]
        )[:2]

        # Day of week analysis
        day_of_week_returns = self._group_by_day_of_week(returns, dates)
        day_of_week_stats = self._calculate_period_stats(day_of_week_returns)
        best_days = sorted(
            [(self.DAY_NAMES[i], day_of_week_stats[self.DAY_NAMES[i]]["mean"])
             for i in range(5)],
            key=lambda x: x[1],
            reverse=True
        )[:2]
        worst_days = sorted(
            [(self.DAY_NAMES[i], day_of_week_stats[self.DAY_NAMES[i]]["mean"])
             for i in range(5)],
            key=lambda x: x[1]
        )[:2]

        # Current rankings
        current_month = self.MONTH_NAMES[current_date.month - 1]
        current_quarter = self.QUARTER_NAMES[(current_date.month - 1) // 3]
        current_week = self._get_week_of_month(current_date)
        current_day = self.DAY_NAMES[current_date.weekday()]

        current_month_rank = sorted(
            monthly_stats.items(),
            key=lambda x: x[1]["mean"],
            reverse=True
        ).index((current_month, monthly_stats[current_month])) + 1

        current_quarter_rank = sorted(
            quarterly_stats.items(),
            key=lambda x: x[1]["mean"],
            reverse=True
        ).index((current_quarter, quarterly_stats[current_quarter])) + 1

        current_week_rank = sorted(
            week_of_month_stats.items(),
            key=lambda x: x[1]["mean"],
            reverse=True
        ).index((current_week, week_of_month_stats[current_week])) + 1 if current_week in week_of_month_stats else 3

        current_day_rank = sorted(
            day_of_week_stats.items(),
            key=lambda x: x[1]["mean"],
            reverse=True
        ).index((current_day, day_of_week_stats[current_day])) + 1

        return SeasonalPattern(
            best_months=best_months,
            worst_months=worst_months,
            best_quarters=best_quarters,
            worst_quarters=worst_quarters,
            best_weeks_of_month=best_weeks,
            worst_weeks_of_month=worst_weeks,
            best_days_of_week=best_days,
            worst_days_of_week=worst_days,
            monthly_stats=monthly_stats,
            quarterly_stats=quarterly_stats,
            week_of_month_stats=week_of_month_stats,
            day_of_week_stats=day_of_week_stats,
            current_month_rank=current_month_rank,
            current_quarter_rank=current_quarter_rank,
            current_week_rank=current_week_rank,
            current_day_rank=current_day_rank
        )

    def analyze_election_cycle(
        self,
        closes: List[float],
        dates: List[datetime],
        current_date: datetime
    ) -> ElectionCycleAnalysis:
        """
        Analyze election cycle effects on market performance
        """
        # Determine current phase
        current_phase = self._get_election_cycle_phase(current_date)
        years_until_election = self._years_until_next_election(current_date)

        # Calculate returns for each phase
        returns = self._calculate_returns(closes)
        phase_returns = self._group_by_election_phase(returns, dates)
        phase_performance = {}

        for phase in ElectionCyclePhase:
            if phase.value in phase_returns and phase_returns[phase.value]:
                phase_performance[phase] = {
                    "mean": statistics.mean(phase_returns[phase.value]),
                    "std": statistics.stdev(phase_returns[phase.value]) if len(phase_returns[phase.value]) > 1 else 0,
                    "win_rate": sum(1 for r in phase_returns[phase.value] if r > 0) / len(phase_returns[phase.value]),
                    "count": len(phase_returns[phase.value])
                }
            else:
                phase_performance[phase] = {"mean": 0, "std": 0, "win_rate": 0.5, "count": 0}

        # Current phase statistics
        current_phase_avg_return = phase_performance[current_phase]["mean"]
        current_phase_volatility = phase_performance[current_phase]["std"]

        # Pattern detection
        pre_election_pattern = self._detect_pre_election_strength(closes, dates, current_date)
        post_election_pattern = self._detect_post_election_weakness(closes, dates, current_date)

        # Policy impact score (based on recent volatility and news)
        policy_impact_score = self._calculate_policy_impact_score(closes, dates, current_date)

        # Historical accuracy
        historical_accuracy = self._calculate_election_cycle_accuracy(phase_returns)

        return ElectionCycleAnalysis(
            current_phase=current_phase,
            years_until_election=years_until_election,
            phase_performance=phase_performance,
            current_phase_avg_return=current_phase_avg_return,
            current_phase_volatility=current_phase_volatility,
            pre_election_pattern=pre_election_pattern,
            post_election_pattern=post_election_pattern,
            policy_impact_score=policy_impact_score,
            historical_accuracy=historical_accuracy
        )

    def analyze_options_expiration(
        self,
        closes: List[float],
        dates: List[datetime],
        current_date: datetime,
        options_data: Optional[Dict[str, Any]] = None
    ) -> OptionsExpirationAnalysis:
        """
        Analyze options expiration effects
        """
        # Find next OPEX date (third Friday of the month)
        next_opex = self._get_next_opex_date(current_date)
        days_to_opex = (next_opex - current_date).days
        is_opex_week = 0 <= days_to_opex <= 5

        # Check if triple witching (March, June, Sept, Dec)
        is_triple_witching = next_opex.month in self.TRIPLE_WITCHING_MONTHS

        # Analyze historical OPEX patterns
        returns = self._calculate_returns(closes)
        opex_patterns = self._analyze_opex_patterns(returns, dates)

        pre_opex_avg_return = opex_patterns.get("pre_opex_return", 0.0)
        post_opex_avg_return = opex_patterns.get("post_opex_return", 0.0)
        opex_week_volatility = opex_patterns.get("opex_volatility", 0.0)

        # Determine drift pattern
        if pre_opex_avg_return > 0.002 and post_opex_avg_return < -0.001:
            opex_drift_pattern = "bullish_pre_bearish_post"
        elif pre_opex_avg_return > 0.001:
            opex_drift_pattern = "bullish"
        elif pre_opex_avg_return < -0.001:
            opex_drift_pattern = "bearish"
        else:
            opex_drift_pattern = "neutral"

        # Pin risk analysis (if options data available)
        pin_risk_levels = {}
        max_pain_price = None
        gamma_exposure = None

        if options_data:
            pin_risk_levels = self._calculate_pin_risk(options_data, closes[-1])
            max_pain_price = self._calculate_max_pain(options_data)
            gamma_exposure = self._calculate_gamma_exposure(options_data, closes[-1])

        return OptionsExpirationAnalysis(
            is_opex_week=is_opex_week,
            days_to_opex=days_to_opex,
            is_triple_witching=is_triple_witching,
            opex_drift_pattern=opex_drift_pattern,
            pre_opex_avg_return=pre_opex_avg_return,
            post_opex_avg_return=post_opex_avg_return,
            opex_week_volatility=opex_week_volatility,
            pin_risk_levels=pin_risk_levels,
            max_pain_price=max_pain_price,
            gamma_exposure=gamma_exposure
        )

    def analyze_earnings_season(
        self,
        closes: List[float],
        dates: List[datetime],
        current_date: datetime,
        earnings_dates: Optional[List[datetime]] = None
    ) -> EarningsSeasonAnalysis:
        """
        Analyze earnings season patterns
        """
        # Determine current earnings season
        month = current_date.month
        if month in [1, 2]:
            current_season = "Q4"
            days_into_season = (current_date - datetime(current_date.year, 1, 1)).days
        elif month in [4, 5]:
            current_season = "Q1"
            days_into_season = (current_date - datetime(current_date.year, 4, 1)).days
        elif month in [7, 8]:
            current_season = "Q2"
            days_into_season = (current_date - datetime(current_date.year, 7, 1)).days
        elif month in [10, 11]:
            current_season = "Q3"
            days_into_season = (current_date - datetime(current_date.year, 10, 1)).days
        else:
            current_season = "Q" + str((month - 1) // 3 + 1)
            days_into_season = 0

        # Peak earnings weeks (typically 3-5 weeks into the period)
        is_peak_earnings_week = 15 <= days_into_season <= 35

        # Analyze seasonal performance
        returns = self._calculate_returns(closes)
        season_performance = self._group_by_earnings_season(returns, dates)
        season_stats = self._calculate_period_stats(season_performance)

        # Pre and post earnings drift
        pre_announcement_drift = 0.0
        post_announcement_drift = 0.0

        if earnings_dates and len(earnings_dates) > 0:
            pre_drift, post_drift = self._calculate_earnings_drift(
                closes, dates, earnings_dates
            )
            pre_announcement_drift = pre_drift
            post_announcement_drift = post_drift

        # Sector rotation signals (simplified)
        sector_rotation_signal = self._analyze_sector_rotation(current_season, returns, dates)

        # Earnings volatility premium
        earnings_volatility_premium = self._calculate_earnings_vol_premium(
            closes, dates, current_date
        )

        return EarningsSeasonAnalysis(
            current_season=current_season,
            is_peak_earnings_week=is_peak_earnings_week,
            days_into_season=days_into_season,
            season_performance=season_stats,
            pre_announcement_drift=pre_announcement_drift,
            post_announcement_drift=post_announcement_drift,
            beat_rate_this_season=None,  # Would need earnings results data
            sector_rotation_signal=sector_rotation_signal,
            earnings_volatility_premium=earnings_volatility_premium
        )

    def detect_market_cycle(
        self,
        closes: List[float],
        highs: List[float],
        lows: List[float],
        volumes: List[float],
        dates: List[datetime],
        current_date: datetime
    ) -> MarketCycleDetection:
        """
        Detect current market cycle and regime
        """
        if len(closes) < 200:
            return self._empty_market_cycle_detection()

        # Calculate trend indicators
        sma_50 = self._sma(closes, 50)
        sma_200 = self._sma(closes, 200)
        price = closes[-1]

        # Bull/Bear score
        bull_bear_score = self._calculate_bull_bear_score(
            closes, sma_50, sma_200
        )

        # Accumulation/Distribution score
        acc_dist_score = self._calculate_accumulation_distribution(
            closes, volumes
        )

        # Determine regime
        current_regime, confidence = self._classify_market_regime(
            bull_bear_score, acc_dist_score, closes, volumes
        )

        # Regime history
        regime_history = self._build_regime_history(
            closes, highs, lows, volumes, dates
        )

        # Days in current regime
        days_in_regime = self._calculate_days_in_regime(regime_history, current_regime)

        # Trend strength
        trend_strength = abs(bull_bear_score)

        # Volatility regime
        volatility_regime = self._classify_volatility_regime(closes)

        # Transition probabilities
        transition_probability = self._calculate_transition_probabilities(
            current_regime, bull_bear_score, acc_dist_score, trend_strength
        )

        # Support and resistance levels
        support_levels = self._identify_support_levels(closes, lows)
        resistance_levels = self._identify_resistance_levels(closes, highs)

        return MarketCycleDetection(
            current_regime=current_regime,
            regime_confidence=confidence,
            days_in_regime=days_in_regime,
            regime_history=regime_history[-10:],  # Last 10 changes
            bull_bear_score=bull_bear_score,
            accumulation_distribution_score=acc_dist_score,
            trend_strength=trend_strength,
            volatility_regime=volatility_regime,
            transition_probability=transition_probability,
            support_levels=support_levels,
            resistance_levels=resistance_levels
        )

    # ==================== Helper Methods ====================

    def _calculate_returns(self, closes: List[float]) -> List[float]:
        """Calculate daily returns"""
        returns = []
        for i in range(1, len(closes)):
            ret = (closes[i] - closes[i-1]) / closes[i-1] if closes[i-1] != 0 else 0
            returns.append(ret)
        return returns

    def _group_by_month(self, returns: List[float], dates: List[datetime]) -> Dict[str, List[float]]:
        """Group returns by month"""
        monthly = defaultdict(list)
        for i, date in enumerate(dates[1:]):  # Skip first date since returns start at index 1
            month_name = self.MONTH_NAMES[date.month - 1]
            if i < len(returns):
                monthly[month_name].append(returns[i])
        return dict(monthly)

    def _group_by_quarter(self, returns: List[float], dates: List[datetime]) -> Dict[str, List[float]]:
        """Group returns by quarter"""
        quarterly = defaultdict(list)
        for i, date in enumerate(dates[1:]):
            quarter = f"Q{(date.month - 1) // 3 + 1}"
            if i < len(returns):
                quarterly[quarter].append(returns[i])
        return dict(quarterly)

    def _group_by_week_of_month(self, returns: List[float], dates: List[datetime]) -> Dict[int, List[float]]:
        """Group returns by week of month (1-5)"""
        weekly = defaultdict(list)
        for i, date in enumerate(dates[1:]):
            week = self._get_week_of_month(date)
            if i < len(returns):
                weekly[week].append(returns[i])
        return dict(weekly)

    def _group_by_day_of_week(self, returns: List[float], dates: List[datetime]) -> Dict[str, List[float]]:
        """Group returns by day of week"""
        daily = defaultdict(list)
        for i, date in enumerate(dates[1:]):
            if date.weekday() < 5:  # Only weekdays
                day_name = self.DAY_NAMES[date.weekday()]
                if i < len(returns):
                    daily[day_name].append(returns[i])
        return dict(daily)

    def _get_week_of_month(self, date: datetime) -> int:
        """Get week of month (1-5)"""
        return (date.day - 1) // 7 + 1

    def _calculate_period_stats(self, period_returns: Dict[str, List[float]]) -> Dict[str, Dict[str, float]]:
        """Calculate statistics for each period"""
        stats = {}
        for period, returns in period_returns.items():
            if returns and len(returns) > 0:
                stats[period] = {
                    "mean": statistics.mean(returns),
                    "std": statistics.stdev(returns) if len(returns) > 1 else 0,
                    "win_rate": sum(1 for r in returns if r > 0) / len(returns),
                    "count": len(returns),
                    "max": max(returns),
                    "min": min(returns)
                }
            else:
                stats[period] = {
                    "mean": 0, "std": 0, "win_rate": 0.5,
                    "count": 0, "max": 0, "min": 0
                }
        return stats

    def _get_election_cycle_phase(self, date: datetime) -> ElectionCyclePhase:
        """Determine current election cycle phase"""
        year = date.year
        # Presidential elections are on years divisible by 4
        years_since_election = year % 4

        if years_since_election == 0:
            # Election year
            if date.month < 11:
                return ElectionCyclePhase.PRE_ELECTION
            else:
                return ElectionCyclePhase.YEAR_4
        elif years_since_election == 1:
            return ElectionCyclePhase.YEAR_1
        elif years_since_election == 2:
            # Mid-term year
            if date.month < 11:
                return ElectionCyclePhase.MID_TERM_PRE
            else:
                return ElectionCyclePhase.YEAR_2
        else:  # years_since_election == 3
            return ElectionCyclePhase.YEAR_3

    def _years_until_next_election(self, date: datetime) -> int:
        """Calculate years until next presidential election"""
        year = date.year
        next_election_year = year + (4 - (year % 4))
        return next_election_year - year

    def _group_by_election_phase(self, returns: List[float], dates: List[datetime]) -> Dict[str, List[float]]:
        """Group returns by election cycle phase"""
        phase_returns = defaultdict(list)
        for i, date in enumerate(dates[1:]):
            phase = self._get_election_cycle_phase(date)
            if i < len(returns):
                phase_returns[phase.value].append(returns[i])
        return dict(phase_returns)

    def _detect_pre_election_strength(self, closes: List[float], dates: List[datetime], current_date: datetime) -> bool:
        """Detect if showing pre-election year strength"""
        phase = self._get_election_cycle_phase(current_date)
        if phase != ElectionCyclePhase.YEAR_3:
            return False

        # Check recent performance
        if len(closes) < 60:
            return False

        recent_return = (closes[-1] - closes[-60]) / closes[-60]
        return recent_return > 0.05  # 5% gain in last 60 days

    def _detect_post_election_weakness(self, closes: List[float], dates: List[datetime], current_date: datetime) -> bool:
        """Detect if showing post-election year weakness"""
        phase = self._get_election_cycle_phase(current_date)
        if phase != ElectionCyclePhase.YEAR_1:
            return False

        if len(closes) < 60:
            return False

        recent_return = (closes[-1] - closes[-60]) / closes[-60]
        return recent_return < -0.03  # -3% loss in last 60 days

    def _calculate_policy_impact_score(self, closes: List[float], dates: List[datetime], current_date: datetime) -> float:
        """Calculate policy impact score based on volatility"""
        if len(closes) < 30:
            return 5.0

        # Recent volatility vs historical
        recent_volatility = statistics.stdev(closes[-20:]) / statistics.mean(closes[-20:]) if len(closes) >= 20 else 0
        historical_volatility = statistics.stdev(closes[-252:]) / statistics.mean(closes[-252:]) if len(closes) >= 252 else recent_volatility

        if historical_volatility == 0:
            return 5.0

        ratio = recent_volatility / historical_volatility
        # Score 0-10, where 10 is very high policy impact
        score = min(10, max(0, (ratio - 0.5) * 10))
        return score

    def _calculate_election_cycle_accuracy(self, phase_returns: Dict[str, List[float]]) -> float:
        """Calculate historical accuracy of election cycle patterns"""
        # Simplified: check if Year 3 is best and Year 1 is worst
        if not phase_returns:
            return 0.5

        phase_means = {}
        for phase_name, returns in phase_returns.items():
            if returns:
                phase_means[phase_name] = statistics.mean(returns)

        if not phase_means:
            return 0.5

        # Check if Year 3 > Year 1
        year_3_mean = phase_means.get(ElectionCyclePhase.YEAR_3.value, 0)
        year_1_mean = phase_means.get(ElectionCyclePhase.YEAR_1.value, 0)

        if year_3_mean > year_1_mean:
            return 0.75
        else:
            return 0.25

    def _get_next_opex_date(self, current_date: datetime) -> datetime:
        """Get next monthly options expiration date (3rd Friday)"""
        # Start with current month
        year = current_date.year
        month = current_date.month

        # Find 3rd Friday
        first_day = datetime(year, month, 1)
        first_friday = first_day + timedelta(days=(4 - first_day.weekday() + 7) % 7)
        third_friday = first_friday + timedelta(days=14)

        # If we've passed it, get next month's
        if current_date > third_friday:
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
            first_day = datetime(year, month, 1)
            first_friday = first_day + timedelta(days=(4 - first_day.weekday() + 7) % 7)
            third_friday = first_friday + timedelta(days=14)

        return third_friday

    def _analyze_opex_patterns(self, returns: List[float], dates: List[datetime]) -> Dict[str, float]:
        """Analyze historical OPEX patterns"""
        pre_opex_returns = []
        post_opex_returns = []
        opex_week_vols = []

        for i, date in enumerate(dates[1:]):
            if i >= len(returns):
                break

            # Find if this is near OPEX
            next_opex = self._get_next_opex_date(date)
            days_to_opex = (next_opex - date).days

            if 1 <= days_to_opex <= 5:  # Week before OPEX
                pre_opex_returns.append(returns[i])
            elif -5 <= days_to_opex <= -1:  # Week after OPEX
                post_opex_returns.append(returns[i])

        return {
            "pre_opex_return": statistics.mean(pre_opex_returns) if pre_opex_returns else 0.0,
            "post_opex_return": statistics.mean(post_opex_returns) if post_opex_returns else 0.0,
            "opex_volatility": statistics.stdev(pre_opex_returns + post_opex_returns) if (pre_opex_returns + post_opex_returns) else 0.0
        }

    def _calculate_pin_risk(self, options_data: Dict[str, Any], current_price: float) -> Dict[float, float]:
        """Calculate pin risk at various strike prices"""
        # Simplified pin risk based on open interest
        pin_risk = {}

        # This would use actual options data
        # For now, return strikes near current price
        strikes = [
            current_price * 0.95,
            current_price,
            current_price * 1.05
        ]

        for strike in strikes:
            # Probability proportional to distance
            distance = abs(strike - current_price) / current_price
            probability = max(0, 1 - distance * 10)  # Simplified
            pin_risk[strike] = probability

        return pin_risk

    def _calculate_max_pain(self, options_data: Dict[str, Any]) -> Optional[float]:
        """Calculate max pain price"""
        # This would calculate the strike where option holders lose most
        # Simplified implementation
        return None

    def _calculate_gamma_exposure(self, options_data: Dict[str, Any], current_price: float) -> Optional[float]:
        """Calculate market maker gamma exposure"""
        # This would calculate dealer gamma exposure
        # Simplified implementation
        return None

    def _group_by_earnings_season(self, returns: List[float], dates: List[datetime]) -> Dict[str, List[float]]:
        """Group returns by earnings season"""
        season_returns = defaultdict(list)

        for i, date in enumerate(dates[1:]):
            month = date.month
            if month in [1, 2]:
                season = "Q4"
            elif month in [4, 5]:
                season = "Q1"
            elif month in [7, 8]:
                season = "Q2"
            elif month in [10, 11]:
                season = "Q3"
            else:
                continue

            if i < len(returns):
                season_returns[season].append(returns[i])

        return dict(season_returns)

    def _calculate_earnings_drift(
        self,
        closes: List[float],
        dates: List[datetime],
        earnings_dates: List[datetime]
    ) -> Tuple[float, float]:
        """Calculate pre and post earnings drift"""
        pre_drift_values = []
        post_drift_values = []

        for earnings_date in earnings_dates:
            # Find the closest date in our data
            closest_idx = None
            min_diff = timedelta(days=999999)

            for i, date in enumerate(dates):
                diff = abs(date - earnings_date)
                if diff < min_diff:
                    min_diff = diff
                    closest_idx = i

            if closest_idx is None or min_diff.days > 5:
                continue

            # Pre-earnings drift (10 days before)
            if closest_idx >= 10:
                pre_drift = (closes[closest_idx] - closes[closest_idx - 10]) / closes[closest_idx - 10]
                pre_drift_values.append(pre_drift)

            # Post-earnings drift (10 days after)
            if closest_idx + 10 < len(closes):
                post_drift = (closes[closest_idx + 10] - closes[closest_idx]) / closes[closest_idx]
                post_drift_values.append(post_drift)

        avg_pre_drift = statistics.mean(pre_drift_values) if pre_drift_values else 0.0
        avg_post_drift = statistics.mean(post_drift_values) if post_drift_values else 0.0

        return avg_pre_drift, avg_post_drift

    def _analyze_sector_rotation(self, current_season: str, returns: List[float], dates: List[datetime]) -> Dict[str, str]:
        """Analyze sector rotation signals"""
        # Simplified sector rotation analysis
        # In reality, would need sector-specific data
        rotation_signals = {
            "Technology": "hold",
            "Healthcare": "hold",
            "Financials": "hold",
            "Energy": "hold",
            "Consumer": "hold"
        }

        # Q4 earnings: Tech often strong
        if current_season == "Q4":
            rotation_signals["Technology"] = "accumulate"
        # Q1 earnings: Financials often strong
        elif current_season == "Q1":
            rotation_signals["Financials"] = "accumulate"

        return rotation_signals

    def _calculate_earnings_vol_premium(self, closes: List[float], dates: List[datetime], current_date: datetime) -> float:
        """Calculate earnings volatility premium"""
        if len(closes) < 60:
            return 0.0

        # Compare recent volatility to longer-term
        recent_vol = statistics.stdev(closes[-20:]) if len(closes) >= 20 else 0
        longer_vol = statistics.stdev(closes[-60:]) if len(closes) >= 60 else recent_vol

        if longer_vol == 0:
            return 0.0

        premium = (recent_vol - longer_vol) / longer_vol
        return premium

    def _sma(self, values: List[float], period: int) -> List[Optional[float]]:
        """Simple Moving Average"""
        result = []
        for i in range(len(values)):
            if i < period - 1:
                result.append(None)
            else:
                avg = sum(values[i-period+1:i+1]) / period
                result.append(avg)
        return result

    def _calculate_bull_bear_score(
        self,
        closes: List[float],
        sma_50: List[Optional[float]],
        sma_200: List[Optional[float]]
    ) -> float:
        """Calculate bull/bear score (-100 to +100)"""
        price = closes[-1]
        score = 0.0

        # Price vs moving averages
        if sma_50[-1] and price > sma_50[-1]:
            score += 25
        elif sma_50[-1] and price < sma_50[-1]:
            score -= 25

        if sma_200[-1] and price > sma_200[-1]:
            score += 25
        elif sma_200[-1] and price < sma_200[-1]:
            score -= 25

        # MA alignment
        if sma_50[-1] and sma_200[-1]:
            if sma_50[-1] > sma_200[-1]:
                score += 20
            else:
                score -= 20

        # Momentum
        if len(closes) >= 20:
            momentum = (closes[-1] - closes[-20]) / closes[-20]
            score += momentum * 100  # Scale to -/+ 30 range

        return max(-100, min(100, score))

    def _calculate_accumulation_distribution(self, closes: List[float], volumes: List[float]) -> float:
        """Calculate accumulation/distribution score"""
        if len(closes) < 20 or len(volumes) < 20:
            return 0.0

        # Simplified A/D calculation
        score = 0.0

        for i in range(len(closes) - 20, len(closes)):
            if i < 1:
                continue

            # Price up + volume up = accumulation
            price_change = closes[i] - closes[i-1]
            if i < len(volumes):
                vol_ratio = volumes[i] / volumes[i-1] if i > 0 and volumes[i-1] > 0 else 1

                if price_change > 0 and vol_ratio > 1.1:
                    score += 5  # Accumulation
                elif price_change < 0 and vol_ratio > 1.1:
                    score -= 5  # Distribution

        return max(-100, min(100, score))

    def _classify_market_regime(
        self,
        bull_bear_score: float,
        acc_dist_score: float,
        closes: List[float],
        volumes: List[float]
    ) -> Tuple[MarketRegime, float]:
        """Classify market regime with confidence"""

        # Strong bull
        if bull_bear_score > 60:
            return MarketRegime.BULL_STRONG, 85.0
        # Weak bull
        elif bull_bear_score > 20:
            return MarketRegime.BULL_WEAK, 70.0
        # Strong bear
        elif bull_bear_score < -60:
            return MarketRegime.BEAR_STRONG, 85.0
        # Weak bear
        elif bull_bear_score < -20:
            return MarketRegime.BEAR_WEAK, 70.0
        # Accumulation
        elif acc_dist_score > 30:
            return MarketRegime.ACCUMULATION, 65.0
        # Distribution
        elif acc_dist_score < -30:
            return MarketRegime.DISTRIBUTION, 65.0
        # Sideways
        elif abs(bull_bear_score) < 20:
            return MarketRegime.SIDEWAYS, 60.0
        else:
            return MarketRegime.UNKNOWN, 40.0

    def _build_regime_history(
        self,
        closes: List[float],
        highs: List[float],
        lows: List[float],
        volumes: List[float],
        dates: List[datetime]
    ) -> List[Tuple[datetime, MarketRegime]]:
        """Build regime history"""
        history = []

        # Sample every 30 days
        for i in range(200, len(closes), 30):
            window_closes = closes[max(0, i-200):i]
            window_volumes = volumes[max(0, i-200):i]

            sma_50 = self._sma(window_closes, 50)
            sma_200 = self._sma(window_closes, 200)

            bb_score = self._calculate_bull_bear_score(window_closes, sma_50, sma_200)
            ad_score = self._calculate_accumulation_distribution(window_closes, window_volumes)

            regime, _ = self._classify_market_regime(bb_score, ad_score, window_closes, window_volumes)
            history.append((dates[i], regime))

        return history

    def _calculate_days_in_regime(self, regime_history: List[Tuple[datetime, MarketRegime]], current_regime: MarketRegime) -> int:
        """Calculate days in current regime"""
        if not regime_history:
            return 0

        days = 0
        for date, regime in reversed(regime_history):
            if regime == current_regime:
                days += 30  # Approximation
            else:
                break

        return days

    def _classify_volatility_regime(self, closes: List[float]) -> str:
        """Classify volatility regime"""
        if len(closes) < 30:
            return "normal"

        recent_vol = statistics.stdev(closes[-20:]) / statistics.mean(closes[-20:]) if len(closes) >= 20 else 0
        historical_vol = statistics.stdev(closes[-252:]) / statistics.mean(closes[-252:]) if len(closes) >= 252 else recent_vol

        if historical_vol == 0:
            return "normal"

        ratio = recent_vol / historical_vol

        if ratio > 2.0:
            return "extreme"
        elif ratio > 1.5:
            return "high"
        elif ratio < 0.7:
            return "low"
        else:
            return "normal"

    def _calculate_transition_probabilities(
        self,
        current_regime: MarketRegime,
        bull_bear_score: float,
        acc_dist_score: float,
        trend_strength: float
    ) -> Dict[MarketRegime, float]:
        """Calculate transition probabilities"""
        probabilities = {}

        # Initialize all to low probability
        for regime in MarketRegime:
            probabilities[regime] = 5.0

        # Current regime has highest probability
        probabilities[current_regime] = 60.0

        # Adjust based on scores
        if current_regime == MarketRegime.BULL_STRONG:
            if bull_bear_score < 40:  # Weakening
                probabilities[MarketRegime.BULL_WEAK] = 25.0
            if acc_dist_score < -20:  # Distribution
                probabilities[MarketRegime.DISTRIBUTION] = 15.0
        elif current_regime == MarketRegime.BEAR_STRONG:
            if bull_bear_score > -40:  # Weakening
                probabilities[MarketRegime.BEAR_WEAK] = 25.0
            if acc_dist_score > 20:  # Accumulation
                probabilities[MarketRegime.ACCUMULATION] = 15.0

        # Normalize
        total = sum(probabilities.values())
        for regime in probabilities:
            probabilities[regime] = (probabilities[regime] / total) * 100

        return probabilities

    def _identify_support_levels(self, closes: List[float], lows: List[float]) -> List[float]:
        """Identify key support levels"""
        if len(lows) < 60:
            return []

        # Find local minima in last 60 days
        support_levels = []
        window = lows[-60:]

        for i in range(5, len(window) - 5):
            if window[i] == min(window[i-5:i+5]):
                support_levels.append(window[i])

        # Remove duplicates (within 1%)
        unique_supports = []
        for level in sorted(support_levels):
            if not unique_supports or abs(level - unique_supports[-1]) / unique_supports[-1] > 0.01:
                unique_supports.append(level)

        return unique_supports[-3:]  # Return top 3

    def _identify_resistance_levels(self, closes: List[float], highs: List[float]) -> List[float]:
        """Identify key resistance levels"""
        if len(highs) < 60:
            return []

        # Find local maxima in last 60 days
        resistance_levels = []
        window = highs[-60:]

        for i in range(5, len(window) - 5):
            if window[i] == max(window[i-5:i+5]):
                resistance_levels.append(window[i])

        # Remove duplicates (within 1%)
        unique_resistance = []
        for level in sorted(resistance_levels):
            if not unique_resistance or abs(level - unique_resistance[-1]) / unique_resistance[-1] > 0.01:
                unique_resistance.append(level)

        return unique_resistance[-3:]  # Return top 3

    def _calculate_composite_score(
        self,
        seasonal: SeasonalPattern,
        election: ElectionCycleAnalysis,
        options: OptionsExpirationAnalysis,
        earnings: EarningsSeasonAnalysis,
        market_cycle: MarketCycleDetection
    ) -> float:
        """Calculate composite seasonality favorability score"""
        score = 50.0  # Start neutral

        # Seasonal contribution (20 points)
        if seasonal.current_month_rank <= 4:
            score += 5
        elif seasonal.current_month_rank >= 9:
            score -= 5

        if seasonal.current_quarter_rank <= 2:
            score += 5
        else:
            score -= 3

        # Election cycle contribution (15 points)
        if election.current_phase in [ElectionCyclePhase.YEAR_3, ElectionCyclePhase.YEAR_4]:
            score += 10  # Pre-election years typically strong
        elif election.current_phase == ElectionCyclePhase.YEAR_1:
            score -= 5  # Post-election year typically weak

        # Options expiration contribution (10 points)
        if options.opex_drift_pattern == "bullish":
            score += 5
        elif options.opex_drift_pattern == "bearish":
            score -= 5

        # Market cycle contribution (25 points)
        if market_cycle.current_regime in [MarketRegime.BULL_STRONG, MarketRegime.ACCUMULATION]:
            score += 15
        elif market_cycle.current_regime in [MarketRegime.BEAR_STRONG, MarketRegime.DISTRIBUTION]:
            score -= 15

        # Earnings season contribution (10 points)
        if earnings.is_peak_earnings_week:
            score += 5

        return max(0, min(100, score))

    def _generate_insights_and_warnings(
        self,
        seasonal: SeasonalPattern,
        election: ElectionCycleAnalysis,
        options: OptionsExpirationAnalysis,
        earnings: EarningsSeasonAnalysis,
        market_cycle: MarketCycleDetection
    ) -> Tuple[List[str], List[str]]:
        """Generate key insights and warnings"""
        insights = []
        warnings = []

        # Seasonal insights
        if seasonal.current_month_rank <= 3:
            insights.append(f"Historically strong month (ranked #{seasonal.current_month_rank})")
        elif seasonal.current_month_rank >= 10:
            warnings.append(f"Historically weak month (ranked #{seasonal.current_month_rank})")

        # Election cycle insights
        if election.current_phase == ElectionCyclePhase.YEAR_3:
            insights.append("Year 3 of presidential cycle - historically strongest year")
        elif election.current_phase == ElectionCyclePhase.YEAR_1:
            warnings.append("Post-election year - historically weakest year")

        # Options expiration
        if options.is_triple_witching:
            warnings.append("Triple witching week - expect elevated volatility")
        if options.is_opex_week and options.opex_drift_pattern == "bullish_pre_bearish_post":
            insights.append("OPEX week with bullish pre-expiration drift pattern")

        # Market cycle
        if market_cycle.current_regime == MarketRegime.BULL_STRONG:
            insights.append(f"Strong bull market regime ({market_cycle.regime_confidence:.0f}% confidence)")
        elif market_cycle.current_regime == MarketRegime.BEAR_STRONG:
            warnings.append(f"Strong bear market regime ({market_cycle.regime_confidence:.0f}% confidence)")

        if market_cycle.volatility_regime == "extreme":
            warnings.append("Extreme volatility regime detected")

        # Distribution warning
        if market_cycle.current_regime == MarketRegime.DISTRIBUTION:
            warnings.append("Distribution phase detected - smart money may be selling")

        return insights, warnings

    def _empty_seasonal_pattern(self) -> SeasonalPattern:
        """Return empty seasonal pattern"""
        return SeasonalPattern(
            best_months=[],
            worst_months=[],
            best_quarters=[],
            worst_quarters=[],
            best_weeks_of_month=[],
            worst_weeks_of_month=[],
            best_days_of_week=[],
            worst_days_of_week=[],
            monthly_stats={},
            quarterly_stats={},
            week_of_month_stats={},
            day_of_week_stats={},
            current_month_rank=6,
            current_quarter_rank=2,
            current_week_rank=3,
            current_day_rank=3
        )

    def _empty_market_cycle_detection(self) -> MarketCycleDetection:
        """Return empty market cycle detection"""
        return MarketCycleDetection(
            current_regime=MarketRegime.UNKNOWN,
            regime_confidence=0.0,
            days_in_regime=0,
            regime_history=[],
            bull_bear_score=0.0,
            accumulation_distribution_score=0.0,
            trend_strength=0.0,
            volatility_regime="normal",
            transition_probability={},
            support_levels=[],
            resistance_levels=[]
        )
