"""
Tests for Smart Money Tracking Services
"""

import pytest
from datetime import datetime, timedelta
from app.services.smart_money import (
    get_dark_pool_service,
    get_institutional_service,
    get_block_trade_service,
    get_analytics_service
)
from app.services.smart_money.models import (
    DarkPoolPrint,
    InstitutionalHolder,
    InsiderTransaction,
    BlockTrade,
    OwnershipChange,
    Sentiment,
    TradeType
)


@pytest.fixture
def dark_pool_service():
    """Get dark pool service instance"""
    return get_dark_pool_service()


@pytest.fixture
def institutional_service():
    """Get institutional service instance"""
    return get_institutional_service()


@pytest.fixture
def block_trade_service():
    """Get block trade service instance"""
    return get_block_trade_service()


@pytest.fixture
def analytics_service():
    """Get analytics service instance"""
    return get_analytics_service()


# ============================================================================
# Dark Pool Service Tests
# ============================================================================

@pytest.mark.asyncio
async def test_dark_pool_add_print(dark_pool_service):
    """Test adding a dark pool print"""
    print_data = DarkPoolPrint(
        symbol="AAPL",
        timestamp=datetime.now(),
        price=178.50,
        size=100000,
        value=17850000.0,
        exchange="DARK_POOL",
        premium_discount=0.5,
        market_price=178.00,
        is_premium=True,
        sentiment=Sentiment.BULLISH
    )

    await dark_pool_service.add_print(print_data)

    # Verify print was added
    prints = await dark_pool_service.get_realtime_prints("AAPL", limit=10)
    assert len(prints) > 0
    assert prints[0].symbol == "AAPL"


@pytest.mark.asyncio
async def test_dark_pool_daily_summary(dark_pool_service):
    """Test getting daily dark pool summary"""
    # Add some test data
    for i in range(5):
        print_data = DarkPoolPrint(
            symbol="AAPL",
            timestamp=datetime.now() - timedelta(hours=i),
            price=178.50 + i,
            size=100000 * (i + 1),
            value=17850000.0 * (i + 1),
            exchange="DARK_POOL",
            premium_discount=0.5 * i,
            market_price=178.00,
            is_premium=i % 2 == 0,
            sentiment=Sentiment.BULLISH if i % 2 == 0 else Sentiment.BEARISH
        )
        await dark_pool_service.add_print(print_data)

    summary = await dark_pool_service.get_daily_summary("AAPL")

    assert summary["symbol"] == "AAPL"
    assert summary["total_prints"] >= 5
    assert summary["total_volume"] > 0
    assert summary["total_value"] > 0


@pytest.mark.asyncio
async def test_dark_pool_unusual_activity(dark_pool_service):
    """Test detecting unusual dark pool activity"""
    # Generate sample data
    await dark_pool_service.generate_sample_data("TSLA", days=7)

    unusual = await dark_pool_service.detect_unusual_activity("TSLA")

    assert "symbol" in unusual
    assert "is_unusual" in unusual
    assert "volume_ratio" in unusual


# ============================================================================
# Institutional Service Tests
# ============================================================================

@pytest.mark.asyncio
async def test_institutional_add_holder(institutional_service):
    """Test adding institutional holder"""
    holder = InstitutionalHolder(
        name="Vanguard Group Inc",
        shares=1250000000,
        value=222500000000.0,
        percentage=8.5,
        change=5000000,
        change_percentage=0.4,
        filing_date=datetime.now(),
        is_new_position=False,
        is_sold_out=False
    )

    await institutional_service.add_holder(holder)

    holders = await institutional_service.get_top_holders(holder.shares, limit=10)
    assert len(holders) > 0


@pytest.mark.asyncio
async def test_institutional_flow(institutional_service):
    """Test getting institutional flow"""
    # Generate sample data
    await institutional_service.generate_sample_data("AAPL")

    flow = await institutional_service.get_institutional_flow("AAPL")

    assert "symbol" in flow
    assert "flow_direction" in flow
    assert "institutional_ownership" in flow


@pytest.mark.asyncio
async def test_insider_sentiment(institutional_service):
    """Test analyzing insider sentiment"""
    # Generate sample data
    await institutional_service.generate_sample_data("AAPL")

    sentiment = await institutional_service.analyze_insider_sentiment("AAPL", days=90)

    assert "symbol" in sentiment
    assert "sentiment" in sentiment
    assert sentiment["sentiment"] in ["bullish", "bearish", "neutral"]
    assert "activity_score" in sentiment


# ============================================================================
# Block Trade Service Tests
# ============================================================================

@pytest.mark.asyncio
async def test_block_trade_add(block_trade_service):
    """Test adding a block trade"""
    trade = BlockTrade(
        symbol="AAPL",
        timestamp=datetime.now(),
        trade_type=TradeType.SWEEP,
        price=178.50,
        size=250000,
        value=44625000.0,
        is_options=False,
        sentiment=Sentiment.BULLISH,
        volume_ratio=3.5
    )

    await block_trade_service.add_trade(trade)

    trades = await block_trade_service.get_recent_blocks("AAPL", hours=24)
    assert len(trades) > 0


@pytest.mark.asyncio
async def test_volume_spike_detection(block_trade_service):
    """Test volume spike detection"""
    spike = await block_trade_service.detect_volume_spikes(
        symbol="AAPL",
        current_volume=50000000,
        threshold=2.0
    )

    assert "symbol" in spike
    assert "is_spike" in spike
    assert "volume_ratio" in spike


@pytest.mark.asyncio
async def test_options_positioning(block_trade_service):
    """Test options positioning analysis"""
    # Generate sample data
    await block_trade_service.generate_sample_data("AAPL", days=7)

    positioning = await block_trade_service.analyze_options_positioning("AAPL", days=7)

    assert "symbol" in positioning
    assert "call_put_ratio" in positioning
    assert "sentiment" in positioning


@pytest.mark.asyncio
async def test_smart_money_divergence(block_trade_service):
    """Test smart money divergence detection"""
    # Generate sample data
    await block_trade_service.generate_sample_data("AAPL", days=5)

    divergence = await block_trade_service.detect_smart_money_divergence(
        symbol="AAPL",
        price_change=-5.0,
        days=5
    )

    assert "symbol" in divergence
    assert "has_divergence" in divergence


# ============================================================================
# Analytics Service Tests
# ============================================================================

@pytest.mark.asyncio
async def test_smart_money_flow(analytics_service, dark_pool_service, institutional_service):
    """Test getting smart money flow"""
    # Generate sample data
    await dark_pool_service.generate_sample_data("AAPL", days=7)
    await institutional_service.generate_sample_data("AAPL")

    flow = await analytics_service.get_smart_money_flow(
        symbol="AAPL",
        total_volume=50000000
    )

    assert flow.symbol == "AAPL"
    assert flow.dark_pool_ratio >= 0
    assert flow.accumulation_distribution in ["accumulation", "distribution", "neutral"]


@pytest.mark.asyncio
async def test_smart_money_indicators(analytics_service, dark_pool_service, block_trade_service):
    """Test getting smart money indicators"""
    # Generate sample data
    await dark_pool_service.generate_sample_data("AAPL", days=7)
    await block_trade_service.generate_sample_data("AAPL", days=7)

    indicators = await analytics_service.get_smart_money_indicators(
        symbol="AAPL",
        price_change=2.5
    )

    assert indicators.symbol == "AAPL"
    assert 0 <= indicators.smart_money_index <= 100
    assert indicators.dark_pool_sentiment in [Sentiment.BULLISH, Sentiment.BEARISH, Sentiment.NEUTRAL]


@pytest.mark.asyncio
async def test_dashboard_data(analytics_service, dark_pool_service, institutional_service, block_trade_service):
    """Test getting complete dashboard data"""
    # Generate sample data
    symbol = "AAPL"
    await dark_pool_service.generate_sample_data(symbol, days=7)
    await institutional_service.generate_sample_data(symbol)
    await block_trade_service.generate_sample_data(symbol, days=7)

    dashboard = await analytics_service.get_dashboard_data(
        symbol=symbol,
        price_change=1.5,
        total_volume=50000000
    )

    assert "symbol" in dashboard
    assert "smart_money_flow" in dashboard
    assert "indicators" in dashboard
    assert "dark_pool" in dashboard
    assert "institutional" in dashboard
    assert "block_trades" in dashboard


# ============================================================================
# Integration Tests
# ============================================================================

@pytest.mark.asyncio
async def test_full_workflow():
    """Test complete workflow from data generation to analytics"""
    symbol = "NVDA"

    # Get services
    dp_service = get_dark_pool_service()
    inst_service = get_institutional_service()
    block_service = get_block_trade_service()
    analytics = get_analytics_service()

    # Generate data
    await dp_service.generate_sample_data(symbol, days=7)
    await inst_service.generate_sample_data(symbol)
    await block_service.generate_sample_data(symbol, days=7)

    # Get analytics
    dashboard = await analytics.get_dashboard_data(
        symbol=symbol,
        price_change=3.2,
        total_volume=75000000
    )

    # Verify all components
    assert dashboard["symbol"] == symbol
    assert len(dashboard["dark_pool"]["recent_prints"]) > 0
    assert len(dashboard["institutional"]["top_holders"]) > 0
    assert len(dashboard["block_trades"]["recent_blocks"]) > 0

    # Verify flow data
    flow = dashboard["smart_money_flow"]
    assert flow["dark_pool_volume"] > 0
    assert flow["smart_money_confidence"] >= 0
    assert flow["smart_money_confidence"] <= 100

    # Verify indicators
    indicators = dashboard["indicators"]
    assert indicators["smart_money_index"] >= 0
    assert indicators["smart_money_index"] <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
