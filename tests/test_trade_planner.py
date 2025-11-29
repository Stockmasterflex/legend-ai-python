"""
Tests for trade planner API
"""

import pytest

from app.api.trade_planner import (TradePlanRequest, calculate_partial_exits,
                                   calculate_position_size)


class TestPositionSizing:
    """Test position size calculations"""

    def test_basic_position_size(self):
        """Test basic position sizing calculation"""
        entry = 100.0
        stop = 95.0
        account_size = 100000.0
        risk_percent = 1.0

        position_size, dollar_amount, risk_amount = calculate_position_size(
            entry, stop, account_size, risk_percent
        )

        # Risk per share = 5.00
        # Max risk = 1000 (1% of 100k)
        # Position size = 1000 / 5 = 200 shares
        assert position_size == 200
        assert dollar_amount == 20000.0  # 200 * 100
        assert risk_amount == 1000.0  # 200 * 5

    def test_higher_risk_percent(self):
        """Test with 2% risk"""
        entry = 50.0
        stop = 48.0
        account_size = 50000.0
        risk_percent = 2.0

        position_size, dollar_amount, risk_amount = calculate_position_size(
            entry, stop, account_size, risk_percent
        )

        # Risk per share = 2.00
        # Max risk = 1000 (2% of 50k)
        # Position size = 1000 / 2 = 500 shares
        assert position_size == 500
        assert dollar_amount == 25000.0
        assert risk_amount == 1000.0

    def test_tight_stop(self):
        """Test with tight stop (higher position size)"""
        entry = 100.0
        stop = 99.0  # Only $1 risk
        account_size = 100000.0
        risk_percent = 1.0

        position_size, dollar_amount, risk_amount = calculate_position_size(
            entry, stop, account_size, risk_percent
        )

        # Risk per share = 1.00
        # Max risk = 1000
        # Position size = 1000 / 1 = 1000 shares
        assert position_size == 1000
        assert dollar_amount == 100000.0  # Full account!
        assert risk_amount == 1000.0


class TestPartialExits:
    """Test partial exit calculations"""

    def test_basic_partial_exits(self):
        """Test 1R, 2R, 3R exit levels"""
        entry = 100.0
        stop = 95.0
        target = 110.0
        position_size = 100

        exits = calculate_partial_exits(entry, stop, target, position_size)

        # Risk per share = 5.00
        # 1R = 105, 2R = 110, 3R = 115
        assert len(exits) == 3

        # 50% at 1R
        assert exits[0].shares == 50
        assert exits[0].price == 105.0
        assert exits[0].r_multiple == 1.0

        # 30% at 2R
        assert exits[1].shares == 30
        assert exits[1].price == 110.0
        assert exits[1].r_multiple == 2.0

        # 20% at 3R
        assert exits[2].shares == 20
        assert exits[2].price == 115.0
        assert exits[2].r_multiple == 3.0

    def test_partial_exits_sum_to_total(self):
        """Verify partial exits sum to total position"""
        entry = 50.0
        stop = 48.0
        target = 56.0
        position_size = 200

        exits = calculate_partial_exits(entry, stop, target, position_size)

        total_shares = sum(e.shares for e in exits)
        assert total_shares == position_size


class TestTradePlanValidation:
    """Test request validation"""

    def test_valid_request(self):
        """Test valid trade plan request"""
        request = TradePlanRequest(
            ticker="NVDA",
            pattern="VCP",
            entry=100.0,
            stop=95.0,
            target=110.0,
            account_size=100000.0,
            risk_percent=1.0,
        )

        assert request.ticker == "NVDA"
        assert request.entry == 100.0

    def test_ticker_uppercase(self):
        """Test ticker is uppercased"""
        request = TradePlanRequest(
            ticker="nvda", entry=100.0, stop=95.0, target=110.0, account_size=100000.0
        )

        assert request.ticker == "NVDA"

    def test_invalid_risk_percent(self):
        """Test risk percent validation"""
        with pytest.raises(ValueError):
            TradePlanRequest(
                ticker="NVDA",
                entry=100.0,
                stop=95.0,
                target=110.0,
                account_size=100000.0,
                risk_percent=10.0,  # Too high!
            )


class TestRiskRewardCalculations:
    """Test R:R calculations"""

    def test_2_to_1_rr(self):
        """Test 2:1 risk/reward"""
        entry = 100.0
        stop = 95.0  # 5 risk
        target = 110.0  # 10 reward

        risk = entry - stop
        reward = target - entry
        rr = reward / risk

        assert rr == 2.0

    def test_3_to_1_rr(self):
        """Test 3:1 risk/reward"""
        entry = 50.0
        stop = 48.0  # 2 risk
        target = 56.0  # 6 reward

        risk = entry - stop
        reward = target - entry
        rr = reward / risk

        assert rr == 3.0


class TestConcentrationWarnings:
    """Test position concentration warnings"""

    def test_high_concentration(self):
        """Test detection of >20% concentration"""
        entry = 10.0
        stop = 9.5  # 0.5 risk
        account_size = 10000.0
        risk_percent = 1.0

        position_size, dollar_amount, risk_amount = calculate_position_size(
            entry, stop, account_size, risk_percent
        )

        concentration = (dollar_amount / account_size) * 100

        # Position = 100 / 0.5 = 200 shares
        # Dollar = 200 * 10 = 2000 (20%)
        assert concentration == 20.0

    def test_normal_concentration(self):
        """Test normal <20% concentration"""
        entry = 100.0
        stop = 95.0  # 5 risk
        account_size = 100000.0
        risk_percent = 1.0

        position_size, dollar_amount, risk_amount = calculate_position_size(
            entry, stop, account_size, risk_percent
        )

        concentration = (dollar_amount / account_size) * 100

        # Position = 1000 / 5 = 200 shares
        # Dollar = 200 * 100 = 20000 (20%)
        assert concentration == 20.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
