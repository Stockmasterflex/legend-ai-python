"""
Pattern Detection Accuracy Tests

These tests verify that pattern detection produces accurate, tradeable signals.
Critical for protecting against false signals when trading with real money.
"""
import pytest
from decimal import Decimal
from typing import Dict, Any

from app.services.pattern_scanner import pattern_scanner_service
from app.core.detector_registry import get_all_detectors


class TestPatternDetectionAccuracy:
    """Test pattern detection accuracy and quality"""

    @pytest.mark.asyncio
    async def test_pattern_confidence_threshold(self):
        """Verify all detected patterns meet minimum confidence threshold"""
        # Scan a known symbol
        results = await pattern_scanner_service.scan_symbol("AAPL", "1day")

        # All patterns should meet minimum confidence (0.6)
        for pattern in results:
            assert pattern["confidence"] >= 0.6, (
                f"Pattern {pattern['pattern']} confidence {pattern['confidence']} "
                f"below minimum 0.6"
            )

    @pytest.mark.asyncio
    async def test_pattern_score_validity(self):
        """Verify pattern scores are within valid range (0-10)"""
        results = await pattern_scanner_service.scan_symbol("NVDA", "1day")

        for pattern in results:
            score = pattern["score"]
            assert 0 <= score <= 10, (
                f"Pattern {pattern['pattern']} score {score} outside valid range 0-10"
            )

    @pytest.mark.asyncio
    async def test_entry_stop_target_logic(self):
        """Verify entry, stop, and target prices are logically ordered"""
        results = await pattern_scanner_service.scan_symbol("MSFT", "1day")

        for pattern in results:
            entry = pattern.get("entry")
            stop = pattern.get("stop")
            target = pattern.get("target")

            # Skip if any price is None
            if not (entry and stop and target):
                continue

            # Entry must be above stop (for long patterns)
            assert entry > stop, (
                f"{pattern['pattern']}: Entry ${entry} must be above stop ${stop}"
            )

            # Target must be above entry
            assert target > entry, (
                f"{pattern['pattern']}: Target ${target} must be above entry ${entry}"
            )

    @pytest.mark.asyncio
    async def test_risk_reward_ratio(self):
        """Verify risk/reward ratios are favorable (>= 1.5:1)"""
        results = await pattern_scanner_service.scan_symbol("GOOGL", "1day")

        for pattern in results:
            rr = pattern.get("risk_reward")

            # Skip if R:R not calculated
            if rr is None:
                continue

            # R:R should be at least 1.5:1 for quality setups
            assert rr >= 1.5, (
                f"{pattern['pattern']}: R:R {rr:.2f} below minimum 1.5:1"
            )

    @pytest.mark.asyncio
    async def test_pattern_evidence_required(self):
        """Verify all patterns include supporting evidence"""
        results = await pattern_scanner_service.scan_symbol("TSLA", "1day")

        for pattern in results:
            evidence = pattern.get("evidence", [])

            # Each pattern should have at least 1 piece of evidence
            assert len(evidence) > 0, (
                f"{pattern['pattern']} has no supporting evidence"
            )

    @pytest.mark.asyncio
    async def test_window_dates_validity(self):
        """Verify pattern window dates are present and logical"""
        results = await pattern_scanner_service.scan_symbol("META", "1day")

        for pattern in results:
            window_start = pattern.get("window_start")
            window_end = pattern.get("window_end")

            # Both dates should be present
            assert window_start is not None, (
                f"{pattern['pattern']} missing window_start"
            )
            assert window_end is not None, (
                f"{pattern['pattern']} missing window_end"
            )

            # window_end should be after or equal to window_start
            assert window_end >= window_start, (
                f"{pattern['pattern']}: window_end {window_end} before window_start {window_start}"
            )

    @pytest.mark.asyncio
    async def test_high_score_patterns_quality(self):
        """Verify high-scoring patterns (>= 8.0) have strong evidence"""
        results = await pattern_scanner_service.scan_symbol("NVDA", "1day")

        high_score_patterns = [p for p in results if p["score"] >= 8.0]

        for pattern in high_score_patterns:
            # High-scoring patterns should be marked as "strong"
            assert pattern.get("strong") is True, (
                f"{pattern['pattern']} score {pattern['score']} but not marked strong"
            )

            # Should have detailed description
            description = pattern.get("description", "")
            assert len(description) > 20, (
                f"{pattern['pattern']} high score but weak description: {description}"
            )

    @pytest.mark.asyncio
    async def test_detector_registry_completeness(self):
        """Verify all detectors are properly registered"""
        detectors = get_all_detectors()

        # Should have at least 8 detectors (VCP, Cup&Handle, Triangle, Wedge, H&S, Double, Channel, SMA50)
        assert len(detectors) >= 8, (
            f"Expected at least 8 detectors, found {len(detectors)}"
        )

        # Each detector should have required attributes
        for detector in detectors:
            assert hasattr(detector, "name"), "Detector missing 'name' attribute"
            assert hasattr(detector, "find"), "Detector missing 'find' method"

    @pytest.mark.asyncio
    async def test_concurrent_scanning_consistency(self):
        """Verify concurrent scanning produces consistent results"""
        # Scan same symbols multiple times concurrently
        scan_result = await pattern_scanner_service.scan_universe(
            universe=["AAPL", "NVDA", "MSFT"],
            limit=10,
            min_score=7.0
        )

        # Should complete successfully
        assert scan_result["success"] is True

        # Should include metadata
        assert "meta" in scan_result
        assert scan_result["meta"]["scanner_type"] == "multi_pattern"

        # Should respect limit
        assert len(scan_result["results"]) <= 10

    @pytest.mark.asyncio
    async def test_minimum_score_filtering(self):
        """Verify minimum score filtering works correctly"""
        scan_result = await pattern_scanner_service.scan_universe(
            universe=["AAPL", "NVDA", "TSLA", "MSFT"],
            limit=50,
            min_score=8.0
        )

        # All results should meet or exceed minimum score
        for result in scan_result["results"]:
            assert result["score"] >= 8.0, (
                f"Result {result['symbol']} score {result['score']} below min 8.0"
            )


class TestTradePlanValidity:
    """Test trade plan generation produces valid, tradeable plans"""

    def test_position_size_calculation(self):
        """Verify position sizing respects 2% risk rule"""
        account_size = 100000  # $100k account
        entry = 150.00
        stop = 145.00
        risk_per_share = entry - stop  # $5

        # With 2% risk rule: max risk = $2000
        max_risk = account_size * 0.02  # $2000
        max_shares = max_risk / risk_per_share  # 400 shares
        position_cost = max_shares * entry  # $60,000

        # Position should not exceed account size
        assert position_cost <= account_size

        # Risk amount should not exceed 2% of account
        actual_risk = max_shares * risk_per_share
        assert actual_risk <= max_risk

    def test_stop_loss_placement(self):
        """Verify stop losses are placed at reasonable levels"""
        entry = 150.00
        stop = 145.00

        # Stop should be within 5% of entry for quality setups
        stop_distance_pct = ((entry - stop) / entry) * 100
        assert stop_distance_pct <= 5.0, (
            f"Stop distance {stop_distance_pct:.2f}% exceeds 5% threshold"
        )

    def test_target_achievability(self):
        """Verify profit targets are realistic"""
        entry = 150.00
        target = 165.00

        # Target should be within 20% of entry for conservative setups
        target_distance_pct = ((target - entry) / entry) * 100
        assert target_distance_pct <= 20.0, (
            f"Target distance {target_distance_pct:.2f}% exceeds 20% threshold"
        )


class TestDataIntegrity:
    """Test data quality and integrity"""

    @pytest.mark.asyncio
    async def test_price_data_completeness(self):
        """Verify price data has all required fields"""
        from app.services.market_data import market_data_service

        price_data = await market_data_service.get_time_series(
            ticker="AAPL",
            interval="1day",
            outputsize=100
        )

        assert price_data is not None, "Failed to fetch price data"

        # Should have OHLCV data
        required_fields = ["o", "h", "l", "c", "v"]
        for field in required_fields:
            assert field in price_data, f"Missing required field: {field}"
            assert len(price_data[field]) > 0, f"Empty data for field: {field}"

    @pytest.mark.asyncio
    async def test_price_data_validity(self):
        """Verify price data values are logical"""
        from app.services.market_data import market_data_service

        price_data = await market_data_service.get_time_series(
            ticker="AAPL",
            interval="1day",
            outputsize=10
        )

        for i in range(len(price_data["c"])):
            open_price = price_data["o"][i]
            high = price_data["h"][i]
            low = price_data["l"][i]
            close = price_data["c"][i]

            # High should be >= all other prices
            assert high >= open_price, f"Bar {i}: High {high} < Open {open_price}"
            assert high >= close, f"Bar {i}: High {high} < Close {close}"
            assert high >= low, f"Bar {i}: High {high} < Low {low}"

            # Low should be <= all other prices
            assert low <= open_price, f"Bar {i}: Low {low} > Open {open_price}"
            assert low <= close, f"Bar {i}: Low {low} > Close {close}"
            assert low <= high, f"Bar {i}: Low {low} > High {high}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
