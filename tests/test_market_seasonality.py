"""
Tests for Market Seasonality Analysis Module
"""

import pytest
from datetime import datetime, timedelta
from app.core.market_seasonality import (
    MarketSeasonalityAnalyzer,
    MarketRegime,
    ElectionCyclePhase,
    SeasonalPattern,
    ElectionCycleAnalysis,
    OptionsExpirationAnalysis,
    EarningsSeasonAnalysis,
    MarketCycleDetection,
    ComprehensiveSeasonalityReport
)


@pytest.fixture
def analyzer():
    """Create analyzer instance"""
    return MarketSeasonalityAnalyzer()


@pytest.fixture
def sample_price_data():
    """Generate sample price data for testing"""
    # Generate 2 years of daily data
    dates = []
    closes = []
    highs = []
    lows = []
    volumes = []

    base_price = 100.0
    current_date = datetime(2024, 1, 1)

    for i in range(504):  # 2 years of trading days
        # Skip weekends
        while current_date.weekday() >= 5:
            current_date += timedelta(days=1)

        dates.append(current_date)

        # Generate realistic price action
        daily_return = (i % 20 - 10) / 1000  # Oscillating returns
        base_price *= (1 + daily_return)

        closes.append(base_price)
        highs.append(base_price * 1.01)
        lows.append(base_price * 0.99)
        volumes.append(1000000 + (i % 100) * 10000)

        current_date += timedelta(days=1)

    return {
        "c": closes,
        "h": highs,
        "l": lows,
        "v": volumes,
        "dates": dates
    }


@pytest.fixture
def earnings_dates():
    """Generate sample earnings dates"""
    return [
        datetime(2023, 1, 15),
        datetime(2023, 4, 15),
        datetime(2023, 7, 15),
        datetime(2023, 10, 15),
        datetime(2024, 1, 15),
        datetime(2024, 4, 15),
    ]


class TestSeasonalPatterns:
    """Test seasonal pattern analysis"""

    def test_analyze_seasonal_patterns_basic(self, analyzer, sample_price_data):
        """Test basic seasonal pattern analysis"""
        result = analyzer.analyze_seasonal_patterns(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        assert isinstance(result, SeasonalPattern)
        assert len(result.best_months) == 3
        assert len(result.worst_months) == 3
        assert len(result.best_quarters) == 2
        assert len(result.worst_quarters) == 2
        assert 1 <= result.current_month_rank <= 12
        assert 1 <= result.current_quarter_rank <= 4

    def test_monthly_stats_calculation(self, analyzer, sample_price_data):
        """Test monthly statistics calculation"""
        result = analyzer.analyze_seasonal_patterns(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        # Should have stats for all 12 months
        assert len(result.monthly_stats) == 12

        for month_stats in result.monthly_stats.values():
            assert "mean" in month_stats
            assert "std" in month_stats
            assert "win_rate" in month_stats
            assert 0 <= month_stats["win_rate"] <= 1

    def test_quarterly_stats_calculation(self, analyzer, sample_price_data):
        """Test quarterly statistics calculation"""
        result = analyzer.analyze_seasonal_patterns(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        # Should have stats for all 4 quarters
        assert len(result.quarterly_stats) == 4

        for quarter_stats in result.quarterly_stats.values():
            assert "mean" in quarter_stats
            assert "std" in quarter_stats
            assert "win_rate" in quarter_stats

    def test_day_of_week_analysis(self, analyzer, sample_price_data):
        """Test day of week performance analysis"""
        result = analyzer.analyze_seasonal_patterns(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        # Should have stats for weekdays
        assert len(result.day_of_week_stats) == 5  # Mon-Fri

        for day_name in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            assert day_name in result.day_of_week_stats

    def test_week_of_month_analysis(self, analyzer, sample_price_data):
        """Test week of month analysis"""
        result = analyzer.analyze_seasonal_patterns(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        # Should have stats for weeks 1-5
        assert len(result.week_of_month_stats) > 0
        assert all(1 <= week <= 5 for week in result.week_of_month_stats.keys())

    def test_insufficient_data_handling(self, analyzer):
        """Test handling of insufficient data"""
        # Less than 1 year of data
        dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(100)]
        closes = [100.0 + i * 0.1 for i in range(100)]

        result = analyzer.analyze_seasonal_patterns(closes, dates, datetime(2024, 6, 15))

        # Should return empty pattern
        assert len(result.best_months) == 0
        assert len(result.monthly_stats) == 0


class TestElectionCycle:
    """Test election cycle analysis"""

    def test_election_phase_detection(self, analyzer):
        """Test election cycle phase detection"""
        # Year 1 (2021 - post election)
        phase = analyzer._get_election_cycle_phase(datetime(2021, 6, 1))
        assert phase == ElectionCyclePhase.YEAR_1

        # Year 2 (2022 - mid-term)
        phase = analyzer._get_election_cycle_phase(datetime(2022, 6, 1))
        assert phase == ElectionCyclePhase.MID_TERM_PRE

        # Year 3 (2023 - pre-election)
        phase = analyzer._get_election_cycle_phase(datetime(2023, 6, 1))
        assert phase == ElectionCyclePhase.YEAR_3

        # Year 4 (2024 - election year)
        phase = analyzer._get_election_cycle_phase(datetime(2024, 6, 1))
        assert phase == ElectionCyclePhase.PRE_ELECTION

    def test_years_until_election(self, analyzer):
        """Test years until next election calculation"""
        # 2023 -> 2024 election
        years = analyzer._years_until_next_election(datetime(2023, 1, 1))
        assert years == 1

        # 2021 -> 2024 election
        years = analyzer._years_until_next_election(datetime(2021, 1, 1))
        assert years == 3

    def test_analyze_election_cycle(self, analyzer, sample_price_data):
        """Test complete election cycle analysis"""
        result = analyzer.analyze_election_cycle(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        assert isinstance(result, ElectionCycleAnalysis)
        assert isinstance(result.current_phase, ElectionCyclePhase)
        assert result.years_until_election >= 0
        assert len(result.phase_performance) > 0
        assert 0 <= result.policy_impact_score <= 10
        assert 0 <= result.historical_accuracy <= 1

    def test_pre_election_strength_detection(self, analyzer, sample_price_data):
        """Test pre-election year strength detection"""
        # Modify data to show strong returns
        closes = sample_price_data["c"]
        dates = sample_price_data["dates"]

        # Make last 60 days show 6% gain
        for i in range(len(closes) - 60, len(closes)):
            closes[i] = closes[len(closes) - 61] * (1 + 0.06 * (i - (len(closes) - 61)) / 60)

        result = analyzer._detect_pre_election_strength(
            closes, dates, datetime(2023, 6, 15)
        )

        assert isinstance(result, bool)


class TestOptionsExpiration:
    """Test options expiration analysis"""

    def test_next_opex_date_calculation(self, analyzer):
        """Test next OPEX date calculation (3rd Friday)"""
        # Test for various months
        current_date = datetime(2024, 1, 5)
        next_opex = analyzer._get_next_opex_date(current_date)

        # Should be 3rd Friday of January
        assert next_opex.month == 1
        assert next_opex.weekday() == 4  # Friday
        assert 15 <= next_opex.day <= 21  # 3rd week

    def test_triple_witching_detection(self, analyzer, sample_price_data):
        """Test triple witching detection"""
        # March - triple witching month
        result = analyzer.analyze_options_expiration(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 3, 15)
        )

        assert isinstance(result, OptionsExpirationAnalysis)
        assert result.is_triple_witching == True

        # April - not triple witching
        result = analyzer.analyze_options_expiration(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 4, 15)
        )

        assert result.is_triple_witching == False

    def test_opex_week_detection(self, analyzer, sample_price_data):
        """Test OPEX week detection"""
        next_opex = analyzer._get_next_opex_date(datetime(2024, 6, 1))

        # Test day before OPEX
        opex_minus_1 = next_opex - timedelta(days=1)
        result = analyzer.analyze_options_expiration(
            sample_price_data["c"],
            sample_price_data["dates"],
            opex_minus_1
        )

        assert result.is_opex_week == True
        assert result.days_to_opex <= 5

    def test_opex_drift_pattern_analysis(self, analyzer, sample_price_data):
        """Test OPEX drift pattern analysis"""
        result = analyzer.analyze_options_expiration(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        assert result.opex_drift_pattern in [
            "bullish", "bearish", "neutral", "bullish_pre_bearish_post"
        ]
        assert isinstance(result.pre_opex_avg_return, float)
        assert isinstance(result.post_opex_avg_return, float)

    def test_pin_risk_calculation(self, analyzer):
        """Test pin risk calculation"""
        options_data = {}  # Simplified
        current_price = 100.0

        pin_risk = analyzer._calculate_pin_risk(options_data, current_price)

        assert isinstance(pin_risk, dict)
        assert len(pin_risk) > 0

        # All probabilities should be 0-1
        for strike, prob in pin_risk.items():
            assert 0 <= prob <= 1


class TestEarningsSeason:
    """Test earnings season analysis"""

    def test_earnings_season_detection(self, analyzer, sample_price_data, earnings_dates):
        """Test earnings season detection"""
        # Q1 earnings (April-May)
        result = analyzer.analyze_earnings_season(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 4, 15),
            earnings_dates
        )

        assert isinstance(result, EarningsSeasonAnalysis)
        assert result.current_season == "Q1"

        # Q4 earnings (Jan-Feb)
        result = analyzer.analyze_earnings_season(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 1, 15),
            earnings_dates
        )

        assert result.current_season == "Q4"

    def test_peak_earnings_week_detection(self, analyzer, sample_price_data, earnings_dates):
        """Test peak earnings week detection"""
        # 3 weeks into earnings season should be peak
        result = analyzer.analyze_earnings_season(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 4, 22),  # ~3 weeks into Q1
            earnings_dates
        )

        assert result.is_peak_earnings_week == True

    def test_earnings_drift_calculation(self, analyzer, sample_price_data, earnings_dates):
        """Test earnings drift calculation"""
        pre_drift, post_drift = analyzer._calculate_earnings_drift(
            sample_price_data["c"],
            sample_price_data["dates"],
            earnings_dates
        )

        assert isinstance(pre_drift, float)
        assert isinstance(post_drift, float)

    def test_sector_rotation_analysis(self, analyzer):
        """Test sector rotation analysis"""
        returns = [0.001] * 100
        dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(100)]

        rotation = analyzer._analyze_sector_rotation("Q4", returns, dates)

        assert isinstance(rotation, dict)
        assert "Technology" in rotation
        assert all(signal in ["accumulate", "distribute", "hold"] for signal in rotation.values())

    def test_earnings_volatility_premium(self, analyzer, sample_price_data):
        """Test earnings volatility premium calculation"""
        premium = analyzer._calculate_earnings_vol_premium(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        assert isinstance(premium, float)


class TestMarketCycleDetection:
    """Test market cycle detection"""

    def test_bull_bear_score_calculation(self, analyzer):
        """Test bull/bear score calculation"""
        # Create bullish scenario
        closes = [100 + i * 0.5 for i in range(252)]  # Uptrend
        sma_50 = analyzer._sma(closes, 50)
        sma_200 = analyzer._sma(closes, 200)

        score = analyzer._calculate_bull_bear_score(closes, sma_50, sma_200)

        # Should be positive for uptrend
        assert score > 0
        assert -100 <= score <= 100

    def test_accumulation_distribution_score(self, analyzer):
        """Test accumulation/distribution score calculation"""
        closes = [100 + i * 0.1 for i in range(100)]
        volumes = [1000000 + i * 10000 for i in range(100)]

        score = analyzer._calculate_accumulation_distribution(closes, volumes)

        assert -100 <= score <= 100

    def test_market_regime_classification(self, analyzer):
        """Test market regime classification"""
        closes = [100 + i * 0.5 for i in range(252)]  # Strong uptrend
        volumes = [1000000] * 252

        regime, confidence = analyzer._classify_market_regime(
            bull_bear_score=80,
            acc_dist_score=40,
            closes=closes,
            volumes=volumes
        )

        assert isinstance(regime, MarketRegime)
        assert 0 <= confidence <= 100

    def test_volatility_regime_classification(self, analyzer):
        """Test volatility regime classification"""
        # Low volatility
        closes = [100.0] * 252
        regime = analyzer._classify_volatility_regime(closes)
        assert regime in ["low", "normal", "high", "extreme"]

        # High volatility
        closes = [100 + (i % 2) * 10 for i in range(252)]
        regime = analyzer._classify_volatility_regime(closes)
        assert regime in ["low", "normal", "high", "extreme"]

    def test_support_resistance_identification(self, analyzer):
        """Test support/resistance level identification"""
        closes = [100.0] * 100
        highs = [101.0] * 100
        lows = [99.0] * 100

        # Add some peaks and valleys
        for i in range(10, 90, 20):
            lows[i] = 95.0  # Support
            highs[i] = 105.0  # Resistance

        support = analyzer._identify_support_levels(closes, lows)
        resistance = analyzer._identify_resistance_levels(closes, highs)

        assert isinstance(support, list)
        assert isinstance(resistance, list)

    def test_detect_market_cycle_complete(self, analyzer, sample_price_data):
        """Test complete market cycle detection"""
        result = analyzer.detect_market_cycle(
            sample_price_data["c"],
            sample_price_data["h"],
            sample_price_data["l"],
            sample_price_data["v"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        assert isinstance(result, MarketCycleDetection)
        assert isinstance(result.current_regime, MarketRegime)
        assert 0 <= result.regime_confidence <= 100
        assert -100 <= result.bull_bear_score <= 100
        assert -100 <= result.accumulation_distribution_score <= 100
        assert result.volatility_regime in ["low", "normal", "high", "extreme"]

    def test_transition_probabilities(self, analyzer):
        """Test regime transition probabilities"""
        probs = analyzer._calculate_transition_probabilities(
            current_regime=MarketRegime.BULL_STRONG,
            bull_bear_score=70,
            acc_dist_score=30,
            trend_strength=70
        )

        assert isinstance(probs, dict)
        assert len(probs) > 0

        # Should sum to ~100
        total = sum(probs.values())
        assert 99 <= total <= 101


class TestComprehensiveAnalysis:
    """Test comprehensive seasonality analysis"""

    @pytest.mark.asyncio
    async def test_analyze_complete_seasonality(self, analyzer, sample_price_data, earnings_dates):
        """Test complete seasonality analysis"""
        result = await analyzer.analyze_complete_seasonality(
            ticker="SPY",
            price_data=sample_price_data,
            dates=sample_price_data["dates"],
            current_date=datetime(2024, 6, 15),
            earnings_dates=earnings_dates
        )

        assert isinstance(result, ComprehensiveSeasonalityReport)
        assert result.ticker == "SPY"
        assert isinstance(result.seasonal_patterns, SeasonalPattern)
        assert isinstance(result.election_cycle, ElectionCycleAnalysis)
        assert isinstance(result.options_expiration, OptionsExpirationAnalysis)
        assert isinstance(result.earnings_season, EarningsSeasonAnalysis)
        assert isinstance(result.market_cycle, MarketCycleDetection)
        assert 0 <= result.composite_score <= 100
        assert isinstance(result.key_insights, list)
        assert isinstance(result.warnings, list)

    def test_composite_score_calculation(self, analyzer, sample_price_data):
        """Test composite score calculation"""
        seasonal = analyzer.analyze_seasonal_patterns(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        election = analyzer.analyze_election_cycle(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        options = analyzer.analyze_options_expiration(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        earnings = analyzer.analyze_earnings_season(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15),
            None
        )

        market_cycle = analyzer.detect_market_cycle(
            sample_price_data["c"],
            sample_price_data["h"],
            sample_price_data["l"],
            sample_price_data["v"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        score = analyzer._calculate_composite_score(
            seasonal, election, options, earnings, market_cycle
        )

        assert 0 <= score <= 100

    def test_insights_and_warnings_generation(self, analyzer, sample_price_data):
        """Test insights and warnings generation"""
        seasonal = analyzer.analyze_seasonal_patterns(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        election = analyzer.analyze_election_cycle(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        options = analyzer.analyze_options_expiration(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        earnings = analyzer.analyze_earnings_season(
            sample_price_data["c"],
            sample_price_data["dates"],
            datetime(2024, 6, 15),
            None
        )

        market_cycle = analyzer.detect_market_cycle(
            sample_price_data["c"],
            sample_price_data["h"],
            sample_price_data["l"],
            sample_price_data["v"],
            sample_price_data["dates"],
            datetime(2024, 6, 15)
        )

        insights, warnings = analyzer._generate_insights_and_warnings(
            seasonal, election, options, earnings, market_cycle
        )

        assert isinstance(insights, list)
        assert isinstance(warnings, list)


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_data(self, analyzer):
        """Test handling of empty data"""
        result = analyzer.analyze_seasonal_patterns([], [], datetime(2024, 6, 15))
        assert len(result.best_months) == 0

    def test_minimal_data(self, analyzer):
        """Test handling of minimal data"""
        dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(30)]
        closes = [100.0] * 30

        result = analyzer.analyze_seasonal_patterns(closes, dates, datetime(2024, 6, 15))
        assert isinstance(result, SeasonalPattern)

    def test_flat_prices(self, analyzer):
        """Test handling of flat price action"""
        dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(252)]
        closes = [100.0] * 252

        result = analyzer.analyze_seasonal_patterns(closes, dates, datetime(2024, 6, 15))

        # Should handle without errors
        assert isinstance(result, SeasonalPattern)
        assert result.current_month_rank > 0

    def test_extreme_volatility(self, analyzer):
        """Test handling of extreme volatility"""
        dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(252)]
        closes = [100 + (i % 2) * 50 for i in range(252)]  # Wild swings

        result = analyzer.analyze_seasonal_patterns(closes, dates, datetime(2024, 6, 15))

        assert isinstance(result, SeasonalPattern)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
