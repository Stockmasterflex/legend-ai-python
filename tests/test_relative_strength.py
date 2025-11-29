"""
Tests for Relative Strength Rating (Minervini SEPA Methodology)

Tests the RS calculation engine that implements Mark Minervini's
weighted quarterly formula and percentile ranking.
"""
import pytest
import numpy as np
from datetime import datetime

from app.services.relative_strength import (
    RelativeStrengthCalculator,
    RSRating,
    get_rs_emoji,
    filter_by_rs_threshold,
)


class TestRelativeStrengthCalculator:
    """Test the RS calculator"""
    
    def test_calculator_initialization(self):
        """Test calculator can be initialized"""
        calc = RelativeStrengthCalculator()
        assert calc is not None
        assert calc.DAYS_PER_QUARTER == 63
        assert calc.DAYS_PER_YEAR == 252
    
    def test_quarterly_performance_calculation(self):
        """Test quarterly performance calculation"""
        calc = RelativeStrengthCalculator()
        
        # Create 252 days of prices with 10% gain each quarter
        prices = np.ones(252) * 100
        
        # Q1 (days -252 to -190): +10% (100 -> 110)
        prices[-252:-189] = np.linspace(100, 110, 63)
        
        # Q2 (days -189 to -127): +10% (110 -> 121)
        prices[-189:-126] = np.linspace(110, 121, 63)
        
        # Q3 (days -126 to -64): +10% (121 -> 133)
        prices[-126:-63] = np.linspace(121, 133, 63)
        
        # Q4 (days -63 to -1): +10% (133 -> 146)
        prices[-63:] = np.linspace(133, 146, 63)
        
        # Calculate quarterly performance
        quarterly = calc._calculate_quarterly_performance(prices)
        
        assert quarterly is not None
        q1, q2, q3, q4 = quarterly
        
        # Each quarter should have ~10% performance
        assert 9.0 < q1 < 11.0, f"Q1 should be ~10%, got {q1}"
        assert 9.0 < q2 < 11.0, f"Q2 should be ~10%, got {q2}"
        assert 9.0 < q3 < 11.0, f"Q3 should be ~10%, got {q3}"
        assert 9.0 < q4 < 11.0, f"Q4 should be ~10%, got {q4}"
    
    def test_weighted_score_calculation(self):
        """Test Minervini's weighted formula: 0.4*Q4 + 0.2*Q3 + 0.2*Q2 + 0.2*Q1"""
        calc = RelativeStrengthCalculator()
        
        # Create simple test: Q1=10%, Q2=10%, Q3=10%, Q4=20%
        prices = np.ones(252) * 100
        prices[-252:-189] = np.linspace(100, 110, 63)  # Q1: +10%
        prices[-189:-126] = np.linspace(110, 121, 63)  # Q2: +10%
        prices[-126:-63] = np.linspace(121, 133, 63)   # Q3: +10%
        prices[-63:] = np.linspace(133, 160, 63)       # Q4: +20%
        
        quarterly = calc._calculate_quarterly_performance(prices)
        q1, q2, q3, q4 = quarterly
        
        # Weighted score
        expected_score = 0.4 * q4 + 0.2 * q3 + 0.2 * q2 + 0.2 * q1
        
        # Should weight recent performance (Q4) higher
        assert expected_score > 12.0, "Weighted score should be > 12% due to Q4 weight"
    
    def test_percentile_ranking(self):
        """Test percentile ranking calculation"""
        calc = RelativeStrengthCalculator()
        
        # Create universe scores
        universe_scores = {
            'A': 10.0,  # Worst
            'B': 20.0,
            'C': 30.0,
            'D': 40.0,
            'E': 50.0,  # Median
            'F': 60.0,
            'G': 70.0,
            'H': 80.0,
            'I': 90.0,  # Best
        }
        
        # Test ranking at various levels
        percentile, rank = calc._calculate_percentile_rank(95.0, universe_scores)
        assert percentile >= 90.0, "Score of 95 should be in top 10%"
        assert rank == 1, "Score of 95 should be rank 1"
        
        percentile, rank = calc._calculate_percentile_rank(50.0, universe_scores)
        assert 30.0 <= percentile <= 60.0, f"Score of 50 should be near median, got {percentile}"
        
        percentile, rank = calc._calculate_percentile_rank(5.0, universe_scores)
        assert percentile <= 10.0, f"Score of 5 should be in bottom 10%, got {percentile}"
    
    def test_rs_rating_calculation(self):
        """Test full RS rating calculation"""
        calc = RelativeStrengthCalculator()
        
        # Create strong performer
        strong_prices = np.ones(252) * 100
        strong_prices[-63:] = np.linspace(100, 150, 63)  # +50% last quarter
        
        # Create weak performers for universe
        universe_prices = {}
        for i in range(10):
            symbol = f'WEAK{i}'
            prices = np.ones(252) * 100
            prices[-63:] = np.linspace(100, 105, 63)  # Only +5% last quarter
            universe_prices[symbol] = prices
        
        # Calculate RS rating
        rs_rating = calc.calculate_rs_rating(
            symbol='STRONG',
            prices=strong_prices,
            universe_prices=universe_prices
        )
        
        assert rs_rating is not None
        assert rs_rating.rs_rating >= 80, "Strong performer should have RS >= 80"
        assert rs_rating.q4_performance > 40.0, "Q4 should be strong"
        assert rs_rating.universe_rank == 1, "Should be rank 1"
    
    def test_insufficient_data(self):
        """Test handling of insufficient data"""
        calc = RelativeStrengthCalculator()
        
        # Only 100 days of data (need 252)
        prices = np.ones(100) * 100
        universe_prices = {'A': np.ones(100) * 100}
        
        rs_rating = calc.calculate_rs_rating(
            symbol='TEST',
            prices=prices,
            universe_prices=universe_prices
        )
        
        assert rs_rating is None, "Should return None for insufficient data"
    
    def test_simple_rs_backward_compatibility(self):
        """Test simple RS calculation for backward compatibility"""
        calc = RelativeStrengthCalculator()
        
        # Stock gains 20% in 60 days
        stock_prices = np.linspace(100, 120, 61)
        
        # SPY gains 10% in 60 days
        spy_prices = np.linspace(100, 110, 61)
        
        rs = calc.calculate_rs_simple('TEST', stock_prices, spy_prices)
        
        assert rs is not None
        assert rs > 5.0, "Stock should outperform SPY by ~10%"


class TestRSRating:
    """Test RSRating dataclass"""
    
    def test_rsrating_creation(self):
        """Test creating RSRating object"""
        rating = RSRating(
            rs_rating=85,
            raw_score=35.5,
            q1_performance=10.0,
            q2_performance=12.0,
            q3_performance=15.0,
            q4_performance=25.0,
            one_year_performance=62.0,
            percentile=85.5,
            universe_rank=15,
            universe_size=100,
            timestamp=datetime.utcnow()
        )
        
        assert rating.rs_rating == 85
        assert rating.raw_score == 35.5
        assert rating.universe_rank == 15
    
    def test_rsrating_to_dict(self):
        """Test converting RSRating to dictionary"""
        rating = RSRating(
            rs_rating=90,
            raw_score=40.0,
            q1_performance=10.0,
            q2_performance=10.0,
            q3_performance=15.0,
            q4_performance=30.0,
            one_year_performance=65.0,
            percentile=90.5,
            universe_rank=10,
            universe_size=100,
            timestamp=datetime.utcnow()
        )
        
        data = rating.to_dict()
        
        assert data['rs_rating'] == 90
        assert data['raw_score'] == 40.0
        assert 'timestamp' in data
    
    def test_rsrating_emoji(self):
        """Test emoji indicators for RS ratings"""
        # Test top 10% (90+)
        rating_90 = RSRating(
            rs_rating=95, raw_score=50.0, q1_performance=10.0,
            q2_performance=10.0, q3_performance=15.0, q4_performance=30.0,
            one_year_performance=65.0, percentile=95.0,
            universe_rank=5, universe_size=100, timestamp=datetime.utcnow()
        )
        assert rating_90.emoji == "🔥"
        
        # Test strong (70-89)
        rating_75 = RSRating(
            rs_rating=75, raw_score=25.0, q1_performance=5.0,
            q2_performance=5.0, q3_performance=10.0, q4_performance=15.0,
            one_year_performance=35.0, percentile=75.0,
            universe_rank=25, universe_size=100, timestamp=datetime.utcnow()
        )
        assert rating_75.emoji == "🟢"
        
        # Test above average (50-69)
        rating_55 = RSRating(
            rs_rating=55, raw_score=10.0, q1_performance=2.0,
            q2_performance=2.0, q3_performance=3.0, q4_performance=5.0,
            one_year_performance=12.0, percentile=55.0,
            universe_rank=45, universe_size=100, timestamp=datetime.utcnow()
        )
        assert rating_55.emoji == "🟡"
        
        # Test below average (<50)
        rating_30 = RSRating(
            rs_rating=30, raw_score=-5.0, q1_performance=-2.0,
            q2_performance=-1.0, q3_performance=0.0, q4_performance=-2.0,
            one_year_performance=-5.0, percentile=30.0,
            universe_rank=70, universe_size=100, timestamp=datetime.utcnow()
        )
        assert rating_30.emoji == "⚪"


class TestRSHelperFunctions:
    """Test RS helper functions"""
    
    def test_get_rs_emoji(self):
        """Test get_rs_emoji function"""
        assert get_rs_emoji(95) == "🔥"
        assert get_rs_emoji(85) == "🟢"
        assert get_rs_emoji(60) == "🟡"
        assert get_rs_emoji(40) == "⚪"
    
    def test_filter_by_rs_threshold(self):
        """Test filtering patterns by RS threshold"""
        patterns = [
            {'ticker': 'A', 'rs_rating': 95},
            {'ticker': 'B', 'rs_rating': 80},
            {'ticker': 'C', 'rs_rating': 65},
            {'ticker': 'D', 'rs_rating': None},  # No RS data
            {'ticker': 'E', 'rs_rating': 50},
        ]
        
        # Filter with RS >= 70
        filtered = filter_by_rs_threshold(patterns, min_rs=70)
        
        assert len(filtered) == 2
        assert filtered[0]['ticker'] == 'A'
        assert filtered[1]['ticker'] == 'B'
    
    def test_filter_by_custom_threshold(self):
        """Test filtering with custom threshold"""
        patterns = [
            {'ticker': 'A', 'rs_rating': 95},
            {'ticker': 'B', 'rs_rating': 92},
            {'ticker': 'C', 'rs_rating': 85},
        ]
        
        # Filter with RS >= 90 (only top 10%)
        filtered = filter_by_rs_threshold(patterns, min_rs=90)
        
        assert len(filtered) == 2
        assert all(p['rs_rating'] >= 90 for p in filtered)


class TestRSIntegration:
    """Integration tests for RS system"""
    
    def test_full_universe_ranking(self):
        """Test ranking a full universe of stocks"""
        calc = RelativeStrengthCalculator()
        
        # Create universe of 20 stocks with varying performance
        universe_prices = {}
        
        for i in range(20):
            symbol = f'STOCK{i:02d}'
            prices = np.ones(252) * 100
            
            # Each stock has different Q4 performance (0% to 40%)
            q4_gain = i * 2  # 0%, 2%, 4%, ... 38%
            end_price = 100 * (1 + q4_gain / 100)
            prices[-63:] = np.linspace(100, end_price, 63)
            
            universe_prices[symbol] = prices
        
        # Test the strongest stock (STOCK19 with 38% Q4 gain)
        strong_prices = universe_prices['STOCK19']
        rs_rating = calc.calculate_rs_rating(
            symbol='STOCK19',
            prices=strong_prices,
            universe_prices={k: v for k, v in universe_prices.items() if k != 'STOCK19'}
        )
        
        assert rs_rating is not None
        assert rs_rating.rs_rating >= 95, "Strongest stock should have RS >= 95"
        assert rs_rating.universe_rank == 1, "Should be rank 1"
        
        # Test median stock (STOCK10 with 20% Q4 gain)
        median_prices = universe_prices['STOCK10']
        rs_rating_median = calc.calculate_rs_rating(
            symbol='STOCK10',
            prices=median_prices,
            universe_prices={k: v for k, v in universe_prices.items() if k != 'STOCK10'}
        )
        
        assert rs_rating_median is not None
        assert 40.0 < rs_rating_median.percentile < 60.0, "Median stock should be near 50th percentile"


class TestMinerviniFormula:
    """Test Minervini's specific formula requirements"""
    
    def test_recent_performance_weighted_higher(self):
        """Test that Q4 (most recent) has 40% weight, others have 20%"""
        calc = RelativeStrengthCalculator()
        
        # Stock A: Consistent 10% each quarter
        prices_consistent = np.ones(252) * 100
        prices_consistent[-252:-189] = np.linspace(100, 110, 63)
        prices_consistent[-189:-126] = np.linspace(110, 121, 63)
        prices_consistent[-126:-63] = np.linspace(121, 133, 63)
        prices_consistent[-63:] = np.linspace(133, 146, 63)
        
        # Stock B: Weak early, strong recent (Q1-Q3: 5%, Q4: 30%)
        prices_recent_strong = np.ones(252) * 100
        prices_recent_strong[-252:-189] = np.linspace(100, 105, 63)  # Q1: +5%
        prices_recent_strong[-189:-126] = np.linspace(105, 110, 63)  # Q2: +5%
        prices_recent_strong[-126:-63] = np.linspace(110, 116, 63)   # Q3: +5%
        prices_recent_strong[-63:] = np.linspace(116, 151, 63)       # Q4: +30%
        
        q_consistent = calc._calculate_quarterly_performance(prices_consistent)
        q_recent = calc._calculate_quarterly_performance(prices_recent_strong)
        
        # Calculate weighted scores
        score_consistent = 0.4 * q_consistent[3] + 0.2 * q_consistent[2] + 0.2 * q_consistent[1] + 0.2 * q_consistent[0]
        score_recent = 0.4 * q_recent[3] + 0.2 * q_recent[2] + 0.2 * q_recent[1] + 0.2 * q_recent[0]
        
        # Stock B should have higher score due to strong Q4 (40% weight)
        assert score_recent > score_consistent, "Recent strong performance should score higher due to Q4 weighting"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

