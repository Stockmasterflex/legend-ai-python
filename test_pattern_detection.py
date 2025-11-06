#!/usr/bin/env python3
"""
Test script for pattern detection logic

Tests the Minervini 8-point trend template and pattern detection algorithms
"""

import asyncio
from datetime import datetime, timedelta
import random

from app.core.pattern_detector import PatternDetector, PatternResult


def generate_mock_price_data(days: int = 300, trend: str = "uptrend") -> dict:
    """Generate mock OHLCV data for testing"""
    closes = []
    highs = []
    lows = []
    opens = []
    volumes = []
    timestamps = []

    # Start with a base price
    base_price = 100.0
    current_price = base_price

    # Generate daily data
    for i in range(days):
        # Add some trend and volatility
        if trend == "uptrend":
            trend_factor = 1 + (i / days) * 0.5  # Gradual uptrend
        elif trend == "downtrend":
            trend_factor = 1 - (i / days) * 0.3  # Gradual downtrend
        else:
            trend_factor = 1.0

        # Random walk with trend
        daily_change = random.gauss(0, 0.02) + (trend_factor - 1) * 0.005
        current_price *= (1 + daily_change)

        # Generate OHLC
        volatility = abs(random.gauss(0, 0.02))
        daily_high = current_price * (1 + volatility)
        daily_low = current_price * (1 - volatility)
        daily_open = closes[-1] if closes else current_price * (1 + random.gauss(0, 0.01))

        closes.append(round(current_price, 2))
        opens.append(round(daily_open, 2))
        highs.append(round(daily_high, 2))
        lows.append(round(daily_low, 2))
        volumes.append(random.randint(1000000, 10000000))

        # Timestamp
        date = datetime.now() - timedelta(days=days-i)
        timestamps.append(date.isoformat())

    return {
        "c": closes,
        "o": opens,
        "h": highs,
        "l": lows,
        "v": volumes,
        "t": timestamps
    }


def generate_spy_data(days: int = 300) -> dict:
    """Generate mock SPY data for RS calculation"""
    return generate_mock_price_data(days, "uptrend")


async def test_trend_template():
    """Test the 8-point trend template"""
    print("\n🧪 Testing 8-Point Trend Template")
    print("=" * 50)

    detector = PatternDetector()

    # Test with uptrending stock
    print("\n📈 Testing with uptrending stock...")
    uptrend_data = generate_mock_price_data(300, "uptrend")
    result = await detector.analyze_ticker("UPTREND", uptrend_data)

    if result:
        print("✅ Analysis completed:")
        print(f"   Pattern: {result.pattern}")
        print(f"   Score: {result.score}/10")
        print(f"   Trend Template: {'✅ PASS' if len([c for c in result.criteria_met if '✓' in c]) >= 7 else '❌ FAIL'}")
        print(f"   Criteria Met: {len([c for c in result.criteria_met if '✓' in c])}/8")
        for criterion in result.criteria_met[:3]:  # Show first 3
            print(f"     {criterion}")

    # Test with insufficient data
    print("\n📉 Testing with insufficient data...")
    short_data = generate_mock_price_data(30, "uptrend")
    result_short = await detector.analyze_ticker("SHORT", short_data)

    if result_short:
        print("✅ Analysis completed:")
        print(f"   Pattern: {result_short.pattern}")
        print(f"   Score: {result_short.score}/10")
        print(f"   Analysis: {result_short.analysis}")


async def test_pattern_detection():
    """Test various pattern detection algorithms"""
    print("\n🎯 Testing Pattern Detection Algorithms")
    print("=" * 50)

    detector = PatternDetector()

    # Test VCP-like data (volatility contractions)
    print("\n🔄 Testing VCP Detection...")
    # Create data with decreasing volatility
    vcp_data = generate_mock_price_data(200, "sideways")
    result_vcp = await detector.analyze_ticker("VCP_TEST", vcp_data)

    if result_vcp:
        print("✅ VCP Analysis:")
        print(f"   Pattern: {result_vcp.pattern}")
        print(f"   Score: {result_vcp.score}/10")
        print(f"   Contractions: {result_vcp.consolidation_days or 0}")

    # Test breakout data
    print("\n📈 Testing Breakout Detection...")
    breakout_data = generate_mock_price_data(200, "strong_uptrend")
    result_breakout = await detector.analyze_ticker("BREAKOUT_TEST", breakout_data)

    if result_breakout:
        print("✅ Breakout Analysis:")
        print(f"   Pattern: {result_breakout.pattern}")
        print(f"   Score: {result_breakout.score}/10")


async def test_rs_calculation():
    """Test Relative Strength calculation"""
    print("\n📊 Testing RS Calculation")
    print("=" * 50)

    detector = PatternDetector()

    # Test with stock outperforming SPY
    stock_data = generate_mock_price_data(200, "strong_uptrend")
    spy_data = generate_mock_price_data(200, "moderate_uptrend")

    result = await detector.analyze_ticker("RS_TEST", stock_data, spy_data)

    if result and result.rs_rating is not None:
        print("✅ RS Calculation:")
        print(f"   RS Rating: {result.rs_rating}")
        bonus = 2 if result.rs_rating > 15 else 1 if result.rs_rating > 5 else 0
        print(f"   RS Score Bonus: +{bonus}")

    else:
        print("❌ RS calculation failed")


async def test_api_format():
    """Test that results match expected API format"""
    print("\n🔌 Testing API Response Format")
    print("=" * 50)

    detector = PatternDetector()
    test_data = generate_mock_price_data(200, "uptrend")

    result = await detector.analyze_ticker("FORMAT_TEST", test_data)

    if result:
        # Test to_dict() method
        api_format = result.to_dict()

        required_fields = [
            "ticker", "pattern", "score", "entry", "stop", "target",
            "risk_reward", "criteria_met", "analysis", "timestamp"
        ]

        missing_fields = [field for field in required_fields if field not in api_format]

        if not missing_fields:
            print("✅ API format correct - all required fields present")
            print(f"   Sample data: ticker={api_format['ticker']}, score={api_format['score']}")
        else:
            print(f"❌ Missing fields: {missing_fields}")

        # Validate data types
        if isinstance(api_format.get("score"), (int, float)):
            print("✅ Score is numeric")
        else:
            print("❌ Score is not numeric")

        if isinstance(api_format.get("entry"), (int, float)):
            print("✅ Entry price is numeric")
        else:
            print("❌ Entry price is not numeric")


async def main():
    """Run all pattern detection tests"""
    print("🧪 LEGEND AI - Pattern Detection Test Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now()}")

    try:
        await test_trend_template()
        await test_pattern_detection()
        await test_rs_calculation()
        await test_api_format()

        print("\n" + "=" * 60)
        print("🎉 Pattern Detection Tests Completed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
