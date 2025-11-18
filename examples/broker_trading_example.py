"""
Broker Trading Example

This script demonstrates how to use the broker integrations for live trading.

IMPORTANT: This uses paper trading by default. Set paper_trading=False for live trading.
"""

import asyncio
import os
from dotenv import load_dotenv

from app.brokers.factory import BrokerFactory
from app.brokers.base import BrokerType, OrderType, OrderSide, TimeInForce
from app.services.live_trading import LiveTradingService, QuickEntryRequest, BracketOrderRequest
from app.services.position_sync import PositionSyncService
from app.services.execution_analytics import ExecutionAnalyticsService

# Load environment variables
load_dotenv()


async def main():
    """Main example function"""

    # ============================================================================
    # 1. CONNECT TO BROKER
    # ============================================================================
    print("\n" + "="*70)
    print("1. CONNECTING TO BROKER")
    print("="*70)

    # Choose broker (change as needed)
    broker_type = BrokerType.ALPACA

    # Get credentials from environment
    if broker_type == BrokerType.ALPACA:
        credentials = {
            "api_key": os.getenv("ALPACA_API_KEY", ""),
            "api_secret": os.getenv("ALPACA_API_SECRET", ""),
        }
    elif broker_type == BrokerType.TD_AMERITRADE:
        credentials = {
            "api_key": os.getenv("TD_AMERITRADE_API_KEY", ""),
            "refresh_token": os.getenv("TD_AMERITRADE_REFRESH_TOKEN", ""),
            "account_id": os.getenv("TD_AMERITRADE_ACCOUNT_ID", ""),
        }
    else:
        print(f"Add credentials for {broker_type.value}")
        return

    # Create broker instance
    broker = BrokerFactory.create(
        broker_type=broker_type,
        credentials=credentials,
        paper_trading=True,  # IMPORTANT: Set to False for live trading
    )

    # Connect to broker (use async context manager)
    async with broker:
        print(f"✅ Connected to {broker_type.value} (paper trading)")

        # ============================================================================
        # 2. GET ACCOUNT INFORMATION
        # ============================================================================
        print("\n" + "="*70)
        print("2. ACCOUNT INFORMATION")
        print("="*70)

        account = await broker.get_account()
        print(f"Account ID: {account.account_id}")
        print(f"Cash: ${account.cash:,.2f}")
        print(f"Buying Power: ${account.buying_power:,.2f}")
        print(f"Portfolio Value: ${account.portfolio_value:,.2f}")
        print(f"Equity: ${account.equity:,.2f}")
        print(f"Unrealized P&L: ${account.unrealized_pl:,.2f}")
        print(f"Pattern Day Trader: {account.pattern_day_trader}")

        # ============================================================================
        # 3. GET CURRENT POSITIONS
        # ============================================================================
        print("\n" + "="*70)
        print("3. CURRENT POSITIONS")
        print("="*70)

        positions = await broker.get_positions()
        if positions:
            for pos in positions:
                print(f"\n{pos.symbol}:")
                print(f"  Quantity: {pos.quantity} shares")
                print(f"  Avg Entry: ${pos.avg_entry_price:.2f}")
                print(f"  Current: ${pos.current_price:.2f}")
                print(f"  Market Value: ${pos.market_value:,.2f}")
                print(f"  P&L: ${pos.unrealized_pl:,.2f} ({pos.unrealized_pl_percent:.2f}%)")
        else:
            print("No open positions")

        # ============================================================================
        # 4. PORTFOLIO SUMMARY WITH ANALYTICS
        # ============================================================================
        print("\n" + "="*70)
        print("4. PORTFOLIO SUMMARY")
        print("="*70)

        sync_service = PositionSyncService(broker)
        summary = await sync_service.get_portfolio_summary()

        print(f"Total Equity: ${summary.total_equity:,.2f}")
        print(f"Total Unrealized P&L: ${summary.total_unrealized_pl:,.2f} ({summary.total_unrealized_pl_percent:.2f}%)")
        print(f"Total Positions: {summary.total_positions}")
        print(f"  Long: {summary.long_positions}")
        print(f"  Short: {summary.short_positions}")

        if summary.top_gainers:
            print("\nTop Gainers:")
            for gainer in summary.top_gainers:
                print(f"  {gainer['symbol']}: ${gainer['unrealized_pl']:,.2f} ({gainer['unrealized_pl_percent']:.2f}%)")

        if summary.top_losers:
            print("\nTop Losers:")
            for loser in summary.top_losers:
                print(f"  {loser['symbol']}: ${loser['unrealized_pl']:,.2f} ({loser['unrealized_pl_percent']:.2f}%)")

        # ============================================================================
        # 5. PLACE QUICK ENTRY ORDER (with auto position sizing)
        # ============================================================================
        print("\n" + "="*70)
        print("5. QUICK ENTRY ORDER (Example - Not Executed)")
        print("="*70)

        # Example: Buy AAPL with 1% risk
        # UNCOMMENT TO ACTUALLY PLACE ORDER
        """
        trading_service = LiveTradingService(broker)

        # Get current price
        current_price = await broker.get_current_price("AAPL")
        print(f"Current AAPL price: ${current_price:.2f}")

        # Calculate entry with 1% ATR below current price (example)
        stop_loss = current_price * 0.98  # 2% stop
        target = current_price * 1.06  # 6% target (3:1 R/R)

        result = await trading_service.quick_entry(
            QuickEntryRequest(
                symbol="AAPL",
                side=OrderSide.BUY,
                account_size=account.cash,
                risk_percent=1.0,  # Risk 1% of account
                entry_price=None,  # Market order
                stop_loss_price=stop_loss,
                target_price=target,
                order_type=OrderType.MARKET
            )
        )

        print(f"Order placed: {result['order'].order_id}")
        print(f"Position size: {result['position_sizing'].position_size} shares")
        print(f"Risk amount: ${result['risk_amount']:,.2f}")
        print(f"Potential reward: ${result['potential_reward']:,.2f}")
        print(f"Risk/Reward: {result['position_sizing'].risk_reward_ratio:.2f}:1")
        """

        print("Quick entry example shown above (commented out for safety)")
        print("Uncomment to actually place orders")

        # ============================================================================
        # 6. PLACE BRACKET ORDER (Entry + TP + SL)
        # ============================================================================
        print("\n" + "="*70)
        print("6. BRACKET ORDER (Example - Not Executed)")
        print("="*70)

        # Example bracket order
        # UNCOMMENT TO ACTUALLY PLACE ORDER
        """
        current_price = await broker.get_current_price("AAPL")

        bracket_orders = await trading_service.place_bracket_order(
            BracketOrderRequest(
                symbol="AAPL",
                side=OrderSide.BUY,
                quantity=10,
                entry_price=current_price,  # Or None for market
                take_profit_price=current_price * 1.06,
                stop_loss_price=current_price * 0.98,
            )
        )

        print(f"Bracket order placed with {len(bracket_orders)} legs")
        for order in bracket_orders:
            print(f"  {order.order_type.value} order: {order.order_id}")
        """

        print("Bracket order example shown above (commented out for safety)")

        # ============================================================================
        # 7. GET CURRENT ORDERS
        # ============================================================================
        print("\n" + "="*70)
        print("7. CURRENT ORDERS")
        print("="*70)

        orders = await broker.get_orders(limit=10)
        if orders:
            for order in orders:
                print(f"\nOrder {order.order_id}:")
                print(f"  Symbol: {order.symbol}")
                print(f"  Side: {order.side.value}")
                print(f"  Type: {order.order_type.value}")
                print(f"  Quantity: {order.quantity}")
                print(f"  Status: {order.status.value}")
                if order.price:
                    print(f"  Price: ${order.price:.2f}")
                if order.filled_qty > 0:
                    print(f"  Filled: {order.filled_qty}/{order.quantity}")
                    print(f"  Avg Fill Price: ${order.avg_fill_price:.2f}")
        else:
            print("No open orders")

        # ============================================================================
        # 8. EXECUTION ANALYTICS
        # ============================================================================
        print("\n" + "="*70)
        print("8. EXECUTION ANALYTICS")
        print("="*70)

        analytics = ExecutionAnalyticsService()

        # Note: In a real scenario, executions would be recorded automatically
        # This is just showing the structure

        stats = analytics.get_aggregate_stats()
        if stats.total_orders > 0:
            print(f"Total Orders: {stats.total_orders}")
            print(f"Fill Rate: {stats.avg_fill_rate:.1f}%")
            print(f"Total Volume: {stats.total_volume:,.0f} shares")
            if stats.avg_slippage_bps:
                print(f"Avg Slippage: {stats.avg_slippage_bps:.2f} bps")
            if stats.avg_execution_duration_ms:
                print(f"Avg Execution Time: {stats.avg_execution_duration_ms:.0f}ms")
            print(f"Execution Quality: {stats.avg_execution_quality:.1f}/100")
        else:
            print("No execution history yet")

        # ============================================================================
        # 9. RISK METRICS FOR POSITION
        # ============================================================================
        print("\n" + "="*70)
        print("9. RISK METRICS (Example)")
        print("="*70)

        # Example: Calculate risk for a position
        if positions:
            pos = positions[0]
            # Assume we have a stop loss 2% below entry
            stop_loss = pos.avg_entry_price * 0.98

            metrics = await sync_service.calculate_risk_metrics(
                symbol=pos.symbol,
                entry_price=pos.avg_entry_price,
                stop_loss=stop_loss,
                account_size=account.equity
            )

            print(f"Position: {metrics['symbol']}")
            print(f"Entry: ${metrics['entry_price']:.2f}")
            print(f"Current: ${metrics['current_price']:.2f}")
            print(f"Stop Loss: ${metrics['stop_loss']:.2f}")
            print(f"Risk per Share: ${metrics['risk_per_share']:.2f}")
            print(f"Total Risk: ${metrics['risk_amount']:,.2f} ({metrics['risk_percent']:.2f}%)")
            print(f"Current P&L: ${metrics['unrealized_pl']:,.2f}")
            print(f"R-Multiple: {metrics['r_multiple']:.2f}R")

        # ============================================================================
        # 10. CLOSE POSITION (Example)
        # ============================================================================
        print("\n" + "="*70)
        print("10. CLOSE POSITION (Example - Not Executed)")
        print("="*70)

        # Example: Close a position
        # UNCOMMENT TO ACTUALLY CLOSE
        """
        if positions:
            pos = positions[0]
            close_order = await trading_service.close_position(
                symbol=pos.symbol,
                quantity=None,  # None = close entire position
                order_type=OrderType.MARKET
            )
            print(f"Position close order placed: {close_order.order_id}")
        """

        print("Position close example shown above (commented out for safety)")

        print("\n" + "="*70)
        print("EXAMPLE COMPLETE")
        print("="*70)
        print("\nTo actually trade:")
        print("1. Set paper_trading=False in broker creation")
        print("2. Uncomment the order placement code")
        print("3. Review and understand each order before placing")
        print("4. Start with small positions to test")
        print("\n⚠️  IMPORTANT: Trading involves risk. Only trade with money you can afford to lose.")


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
