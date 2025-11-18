"""
Tests for Trade Journal System
"""
import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, TradeJournal, TradeStatus, EmotionalState, MarketCondition, Ticker
from app.services.trade_journal import TradeJournalService


# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def db_session():
    """Create a test database session"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_trade_plan(db_session):
    """Test creating a trade plan"""
    service = TradeJournalService(db_session)

    trade = await service.create_trade_plan(
        ticker="AAPL",
        pattern_identified="VCP",
        thesis="Strong breakout setup with volume dry-up",
        planned_entry=150.00,
        planned_stop=145.00,
        planned_target=160.00,
        planned_position_size=100,
        checklist_data={"trend_aligned": True, "volume_confirmation": True}
    )

    assert trade is not None
    assert trade.trade_id.startswith("TRD-")
    assert trade.status == TradeStatus.PLANNED
    assert trade.planned_risk_reward == 2.0  # (160-150) / (150-145)
    assert trade.planned_risk_amount == 500.0  # 5 * 100


@pytest.mark.asyncio
async def test_execute_entry_with_slippage(db_session):
    """Test executing trade entry and tracking slippage"""
    service = TradeJournalService(db_session)

    # Create plan first
    trade = await service.create_trade_plan(
        ticker="AAPL",
        pattern_identified="VCP",
        thesis="Test trade",
        planned_entry=150.00,
        planned_stop=145.00,
        planned_target=160.00,
        planned_position_size=100
    )

    # Execute entry with slippage
    executed_trade = await service.execute_entry(
        trade_id=trade.trade_id,
        actual_entry_price=150.50,  # 50 cent slippage
        actual_position_size=100,
        emotional_state=EmotionalState.CONFIDENT,
        market_condition=MarketCondition.TRENDING_UP
    )

    assert executed_trade.status == TradeStatus.OPEN
    assert executed_trade.entry_slippage == 0.50
    assert executed_trade.slippage_cost == 50.0  # 0.50 * 100 shares
    assert executed_trade.emotional_state_entry == EmotionalState.CONFIDENT


@pytest.mark.asyncio
async def test_execute_exit_and_calculate_pnl(db_session):
    """Test executing trade exit and calculating P&L"""
    service = TradeJournalService(db_session)

    # Create and execute trade
    trade = await service.create_trade_plan(
        ticker="AAPL",
        pattern_identified="VCP",
        thesis="Test trade",
        planned_entry=150.00,
        planned_stop=145.00,
        planned_target=160.00,
        planned_position_size=100
    )

    await service.execute_entry(
        trade_id=trade.trade_id,
        actual_entry_price=150.00,
        actual_position_size=100
    )

    # Exit at target
    closed_trade = await service.execute_exit(
        trade_id=trade.trade_id,
        exit_price=160.00,
        exit_reason="target",
        fees_paid=10.00
    )

    assert closed_trade.status == TradeStatus.CLOSED
    assert closed_trade.gross_pnl == 1000.0  # (160-150) * 100
    assert closed_trade.net_pnl == 990.0  # 1000 - 10 fees
    assert closed_trade.r_multiple == pytest.approx(1.98, 0.01)  # 990 / 500


@pytest.mark.asyncio
async def test_add_trade_notes(db_session):
    """Test adding post-trade review notes"""
    service = TradeJournalService(db_session)

    trade = await service.create_trade_plan(
        ticker="AAPL",
        pattern_identified="VCP",
        thesis="Test trade",
        planned_entry=150.00,
        planned_stop=145.00,
        planned_target=160.00,
        planned_position_size=100
    )

    updated_trade = await service.add_trade_notes(
        trade_id=trade.trade_id,
        what_went_well="Perfect entry timing",
        what_went_wrong="Took profits too early",
        lessons_learned="Trust the setup and let winners run"
    )

    assert updated_trade.what_went_well == "Perfect entry timing"
    assert updated_trade.lessons_learned is not None


@pytest.mark.asyncio
async def test_add_trade_tag(db_session):
    """Test adding tags to trades"""
    service = TradeJournalService(db_session)

    trade = await service.create_trade_plan(
        ticker="AAPL",
        pattern_identified="VCP",
        thesis="Test trade",
        planned_entry=150.00,
        planned_stop=145.00,
        planned_target=160.00,
        planned_position_size=100
    )

    tag = await service.add_trade_tag(trade_id=trade.trade_id, tag="perfect_execution")

    assert tag.tag == "perfect_execution"
    assert tag.trade_journal_id == trade.id


@pytest.mark.asyncio
async def test_add_mistake(db_session):
    """Test categorizing mistakes"""
    service = TradeJournalService(db_session)

    trade = await service.create_trade_plan(
        ticker="AAPL",
        pattern_identified="VCP",
        thesis="Test trade",
        planned_entry=150.00,
        planned_stop=145.00,
        planned_target=160.00,
        planned_position_size=100
    )

    mistake = await service.add_mistake(
        trade_id=trade.trade_id,
        category="exit",
        mistake_type="cut_winner_short",
        description="Exited due to fear instead of following plan",
        impact="moderate"
    )

    assert mistake.category == "exit"
    assert mistake.impact == "moderate"


@pytest.mark.asyncio
async def test_create_playbook(db_session):
    """Test creating a trading playbook"""
    service = TradeJournalService(db_session)

    playbook = await service.create_playbook(
        name="VCP Breakout Strategy",
        description="Classic VCP pattern with 3-4 contractions",
        pattern_type="VCP",
        entry_criteria=["Volume dry-up", "Tight consolidation", "Above 21 EMA"],
        exit_criteria=["Hit target", "Stop loss", "Pattern breaks"],
        risk_management={"max_risk_per_trade": 1.0, "position_sizing": "1% rule"}
    )

    assert playbook.name == "VCP Breakout Strategy"
    assert playbook.pattern_type == "VCP"
    assert len(playbook.entry_criteria) == 3


@pytest.mark.asyncio
async def test_add_lesson(db_session):
    """Test adding a trading lesson"""
    service = TradeJournalService(db_session)

    lesson = await service.add_lesson(
        title="Don't chase breakouts",
        lesson="Wait for pullback after initial breakout for better entry",
        pattern_type="VCP",
        importance="high"
    )

    assert lesson.title == "Don't chase breakouts"
    assert lesson.importance == "high"


@pytest.mark.asyncio
async def test_get_performance_analytics(db_session):
    """Test performance analytics calculation"""
    service = TradeJournalService(db_session)

    # Create multiple trades
    for i in range(5):
        trade = await service.create_trade_plan(
            ticker=f"STOCK{i}",
            pattern_identified="VCP",
            thesis=f"Test trade {i}",
            planned_entry=100.00,
            planned_stop=95.00,
            planned_target=110.00,
            planned_position_size=100
        )

        await service.execute_entry(
            trade_id=trade.trade_id,
            actual_entry_price=100.00,
            actual_position_size=100
        )

        # Make some winners and some losers
        exit_price = 110.00 if i % 2 == 0 else 95.00

        await service.execute_exit(
            trade_id=trade.trade_id,
            exit_price=exit_price,
            exit_reason="target" if i % 2 == 0 else "stop"
        )

    # Get analytics
    analytics = await service.get_performance_analytics()

    assert analytics['total_trades'] == 5
    assert analytics['winning_trades'] == 3
    assert analytics['losing_trades'] == 2
    assert analytics['win_rate'] == 60.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
