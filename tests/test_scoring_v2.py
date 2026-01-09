
import pytest
from app.core.pattern_engine.scoring import PatternScorer

def test_pattern_scorer_basics():
    scorer = PatternScorer()
    
    # Mock pattern
    pattern = {
        "pattern": "VCP",
        "confidence": 0.9,
        "entry": 105.0,
        "metadata": {
            "trend_tier": "TIER_1", # +10 (Trend Quality)
            "regime": {"trend": "BULL"}, 
            "volume_trend_slope": -0.5, # +10 (Volume Characteristic)
            "trend_start_pct": 0.5,
        }
    }
    
    components, score = scorer.score_pattern(pattern)
    
    print(f"Components: {components.to_dict()}")
    print(f"Total Score: {score}")

    # Checks
    # Trend Quality: TIER_1 (10) + Confidence 0.9*5 (4.5) = 14.5
    # Structure: VCP = 15.0
    # Volume: slope < 0 = 10.0
    # Maturity: Default 5.0
    # Proximity: Default 5.0
    # RS: Default 5.0
    # MA Stack: Default 5.0
    # Risks: 0.0
    
    expected_score = 14.5 + 15.0 + 10.0 + 5.0 + 5.0 + 5.0 + 5.0
    # = 59.5
    
    assert components.trend_quality == 14.5
    assert components.structure_tightness == 15.0
    assert components.volume_characteristics == 10.0
    assert score == expected_score

def test_pattern_scorer_penalties():
    scorer = PatternScorer()
    
    pattern = {
        "pattern": "Flag",
        "metadata": {
            "trend_tier": "TIER_3", # 0 pts from tier
            "regime": {"trend": "BEAR"}, # -10 risk
        }
    }
    
    components, score = scorer.score_pattern(pattern)
    
    assert components.risk_regime == -10.0
    assert components.trend_quality <= 5.0 # Only confidence points if any
    
if __name__ == "__main__":
    test_pattern_scorer_basics()
    test_pattern_scorer_penalties()
    print("All scoring tests passed!")
