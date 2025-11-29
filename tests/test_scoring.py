from app.core.pattern_engine.scoring import PatternScorer


def test_score_pattern_breakdown():
    pattern = {
        "ticker": "AAPL",
        "confidence": 0.82,
        "current_price": 55,
        "pattern_height_pct": 0.14,
        "market_cap": 250_000_000_000,
        "trend_start_pct": 34,
        "hcr": 0.78,
        "metadata": {
            "year_high": 60,
            "year_low": 30,
            "base_depth_pct": 0.12,
            "trend_strength": 0.86,
            "volume_trend": -0.6,
            "throwback_pct": 0.04,
            "breakout_gap_pct": 0.05,
        },
    }

    scorer = PatternScorer()
    components, total = scorer.score_pattern(pattern)

    assert round(total, 2) == components.total_score()
    assert total > 6  # solid setup should clear baseline
    assert components.to_dict()["yearly_range"] > 0.5


def test_score_patterns_orders_results():
    strong_pattern = {
        "ticker": "AAPL",
        "confidence": 0.82,
        "current_price": 55,
        "pattern_height_pct": 0.14,
        "market_cap": 250_000_000_000,
        "trend_start_pct": 34,
        "hcr": 0.78,
        "metadata": {
            "year_high": 60,
            "year_low": 30,
            "base_depth_pct": 0.12,
            "trend_strength": 0.86,
            "volume_trend": -0.6,
            "throwback_pct": 0.04,
            "breakout_gap_pct": 0.05,
        },
    }

    weaker_pattern = {
        "ticker": "XYZ",
        "confidence": 0.4,
        "current_price": 20,
        "pattern_height_pct": 0.3,
        "market_cap": 80_000_000,
        "trend_start_pct": 5,
        "metadata": {
            "year_high": 40,
            "year_low": 10,
            "base_depth_pct": 0.35,
            "trend_strength": 0.3,
            "volume_trend": 0.1,
            "throwback_pct": 0.15,
            "breakout_gap_pct": 0.0,
        },
    }

    scorer = PatternScorer()
    ranked = scorer.score_patterns([weaker_pattern, strong_pattern])

    assert ranked[0]["ticker"] == "AAPL"
    assert ranked[0]["score"] > ranked[1]["score"]
    assert "score_components" in ranked[0]
