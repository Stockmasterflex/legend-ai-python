# Broker Connections & Live Trading

This document explains how to set up and use broker connections for live trading with Legend AI.

## Overview

Legend AI supports connections to multiple brokers for live trading:

- **Alpaca** - Commission-free trading with developer-friendly API
- **TD Ameritrade** - Comprehensive broker with thinkorswim platform
- **Interactive Brokers** - Professional-grade broker with global access
- **TradeStation** - Advanced trading platform for active traders

## Features

### 1. Broker Connections
- Multi-broker support with unified interface
- Paper/simulation trading mode for testing
- Automatic credential management
- Connection pooling and lifecycle management

### 2. Live Trading
- **Quick Entry Orders** - One-click trading with automatic position sizing
- **Market Orders** - Instant execution at current market price
- **Limit Orders** - Execute at specified price or better
- **Stop Orders** - Trigger orders when price reaches stop level
- **Stop-Limit Orders** - Combine stop and limit prices
- **Trailing Stops** - Dynamic stop that follows price movements
- **Bracket Orders** - Entry + Take Profit + Stop Loss in one order

### 3. Position Sync
- Auto-import positions from broker
- Real-time position tracking
- Real-time P&L calculations
- Portfolio summary and analytics
- Risk metrics for each position

### 4. Execution Analytics
- Fill quality tracking
- Slippage analysis (basis points)
- Execution duration monitoring
- Price improvement detection
- Best execution reporting
- Order routing statistics

## Setup

### 1. Environment Variables

Add your broker credentials to `.env`:

```bash
# Default broker and mode
DEFAULT_BROKER=alpaca
BROKER_PAPER_TRADING=true  # Set to false for live trading

# Alpaca
ALPACA_API_KEY=your_api_key_here
ALPACA_API_SECRET=your_api_secret_here

# TD Ameritrade
TD_AMERITRADE_API_KEY=your_consumer_key_here
TD_AMERITRADE_REFRESH_TOKEN=your_refresh_token_here
TD_AMERITRADE_ACCOUNT_ID=your_account_id_here

# Interactive Brokers
IB_GATEWAY_URL=https://localhost:5000/v1/api  # Optional
IB_ACCOUNT_ID=your_account_id_here  # Optional

# TradeStation
TRADESTATION_API_KEY=your_api_key_here
TRADESTATION_API_SECRET=your_api_secret_here
TRADESTATION_REFRESH_TOKEN=your_refresh_token_here
TRADESTATION_ACCOUNT_ID=your_account_id_here  # Optional
```

### 2. Obtaining API Credentials

#### Alpaca
1. Sign up at https://alpaca.markets/
2. Go to Paper Trading account
3. Generate API keys from dashboard
4. Copy API Key ID and Secret Key

#### TD Ameritrade
1. Create developer account at https://developer.tdameritrade.com/
2. Register an app to get Consumer Key (API Key)
3. Complete OAuth flow to get refresh token
4. Find your account ID in thinkorswim

#### Interactive Brokers
1. Install IB Gateway or TWS
2. Enable API connections in settings
3. Run Client Portal Gateway locally
4. Gateway URL defaults to https://localhost:5000

#### TradeStation
1. Create account at https://www.tradestation.com/
2. Apply for API access
3. Create app to get API Key and Secret
4. Complete OAuth flow for refresh token

## API Endpoints

### Connection Management

#### Connect to Broker
```http
POST /api/broker/connect
Content-Type: application/json

{
  "broker_type": "alpaca",
  "paper_trading": true
}
```

#### Disconnect
```http
POST /api/broker/disconnect/alpaca
```

#### Get Account Info
```http
GET /api/broker/account/alpaca
```

Response:
```json
{
  "account_id": "XXXXX",
  "broker": "alpaca",
  "cash": 100000.00,
  "buying_power": 200000.00,
  "portfolio_value": 105000.00,
  "equity": 105000.00,
  "unrealized_pl": 5000.00,
  "realized_pl_today": 1000.00,
  "pattern_day_trader": false
}
```

### Position Management

#### Get All Positions
```http
GET /api/broker/positions/alpaca
```

#### Get Position for Symbol
```http
GET /api/broker/positions/alpaca/AAPL
```

#### Get Portfolio Summary
```http
GET /api/broker/portfolio/alpaca
```

Response:
```json
{
  "total_equity": 105000.00,
  "cash": 100000.00,
  "buying_power": 200000.00,
  "portfolio_value": 105000.00,
  "total_unrealized_pl": 5000.00,
  "total_unrealized_pl_percent": 5.0,
  "total_positions": 3,
  "long_positions": 3,
  "short_positions": 0,
  "top_gainers": [
    {
      "symbol": "AAPL",
      "unrealized_pl": 3000.00,
      "unrealized_pl_percent": 6.0
    }
  ],
  "top_losers": []
}
```

#### Close Position
```http
POST /api/broker/positions/close/alpaca/AAPL
```

### Order Placement

#### Place Simple Order
```http
POST /api/broker/orders/place
Content-Type: application/json

{
  "broker_type": "alpaca",
  "symbol": "AAPL",
  "side": "buy",
  "order_type": "limit",
  "quantity": 100,
  "price": 175.50,
  "time_in_force": "day"
}
```

#### Quick Entry (One-Click Trading)
```http
POST /api/broker/orders/quick-entry
Content-Type: application/json

{
  "broker_type": "alpaca",
  "symbol": "AAPL",
  "side": "buy",
  "account_size": 100000.00,
  "risk_percent": 1.0,
  "stop_loss_price": 174.00,
  "target_price": 180.00,
  "order_type": "market"
}
```

This automatically:
- Calculates position size based on 1% risk
- Places entry order
- Sets up risk/reward tracking
- Returns position sizing details

#### Bracket Order
```http
POST /api/broker/orders/bracket
Content-Type: application/json

{
  "broker_type": "alpaca",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 100,
  "entry_price": 175.50,
  "take_profit_price": 180.00,
  "stop_loss_price": 174.00
}
```

#### Cancel Order
```http
DELETE /api/broker/orders/alpaca/{order_id}
```

#### Get Orders
```http
GET /api/broker/orders/alpaca?status=new&limit=50
```

### Market Data

#### Get Current Price
```http
GET /api/broker/price/alpaca/AAPL
```

### Execution Analytics

#### Get Execution Analytics
```http
GET /api/broker/analytics/execution?symbol=AAPL&days=30
```

Response:
```json
{
  "total_orders": 25,
  "filled_orders": 23,
  "avg_fill_rate": 98.5,
  "total_volume": 2500,
  "avg_slippage_bps": 3.2,
  "median_slippage_bps": 2.5,
  "total_slippage_cost": 125.50,
  "avg_execution_duration_ms": 250,
  "avg_execution_quality": 92.5,
  "orders_with_price_improvement": 5,
  "price_improvement_amount": 75.00
}
```

#### Get Slippage Analysis
```http
GET /api/broker/analytics/slippage?symbol=AAPL
```

### Supported Brokers List
```http
GET /api/broker/brokers/supported
```

## Python SDK Usage

### Basic Connection

```python
from app.brokers.factory import BrokerFactory
from app.brokers.base import BrokerType

# Create and connect to broker
broker = BrokerFactory.create(
    broker_type=BrokerType.ALPACA,
    credentials={
        "api_key": "YOUR_API_KEY",
        "api_secret": "YOUR_API_SECRET"
    },
    paper_trading=True
)

async with broker:
    # Get account
    account = await broker.get_account()
    print(f"Cash: ${account.cash:,.2f}")
    print(f"Buying Power: ${account.buying_power:,.2f}")

    # Get positions
    positions = await broker.get_positions()
    for pos in positions:
        print(f"{pos.symbol}: {pos.quantity} shares @ ${pos.avg_entry_price}")
        print(f"  P&L: ${pos.unrealized_pl:,.2f} ({pos.unrealized_pl_percent:.2f}%)")
```

### Live Trading Service

```python
from app.services.live_trading import LiveTradingService, QuickEntryRequest
from app.brokers.base import OrderSide, OrderType

# Create trading service
trading_service = LiveTradingService(broker)

# Quick entry with auto position sizing
result = await trading_service.quick_entry(
    QuickEntryRequest(
        symbol="AAPL",
        side=OrderSide.BUY,
        account_size=100000.00,
        risk_percent=1.0,  # Risk 1% of account
        stop_loss_price=174.00,
        target_price=180.00,
        order_type=OrderType.MARKET
    )
)

print(f"Order placed: {result['order'].order_id}")
print(f"Position size: {result['position_sizing'].position_size} shares")
print(f"Risk amount: ${result['risk_amount']:,.2f}")
```

### Position Sync Service

```python
from app.services.position_sync import PositionSyncService

# Create position sync service
sync_service = PositionSyncService(broker)

# Get portfolio summary
summary = await sync_service.get_portfolio_summary()
print(f"Total P&L: ${summary.total_unrealized_pl:,.2f}")
print(f"Total Positions: {summary.total_positions}")

# Sync positions
positions = await sync_service.sync_positions()

# Get risk metrics for a position
metrics = await sync_service.calculate_risk_metrics(
    symbol="AAPL",
    entry_price=175.50,
    stop_loss=174.00,
    account_size=100000.00
)
print(f"Risk: ${metrics['risk_amount']:,.2f} ({metrics['risk_percent']:.2f}%)")
print(f"R-multiple: {metrics['r_multiple']:.2f}R")
```

### Execution Analytics

```python
from app.services.execution_analytics import ExecutionAnalyticsService

analytics = ExecutionAnalyticsService()

# Record execution (happens automatically via API)
# But you can also do it manually
metrics = analytics.record_execution(order, market_price_at_order)

# Get aggregate stats
stats = analytics.get_aggregate_stats(symbol="AAPL")
print(f"Avg slippage: {stats.avg_slippage_bps:.2f} bps")
print(f"Execution quality: {stats.avg_execution_quality:.1f}/100")

# Get slippage analysis
slippage = analytics.get_slippage_analysis()
print(f"Median slippage: {slippage['median_slippage_bps']:.2f} bps")
```

## Order Types Explained

### Market Order
- Executes immediately at current market price
- Guaranteed fill but not guaranteed price
- Use for: Entering/exiting quickly

### Limit Order
- Executes only at specified price or better
- May not fill if price never reached
- Use for: Entering at specific price

### Stop Order
- Triggers market order when price hits stop level
- Use for: Stop losses, breakout entries

### Stop-Limit Order
- Triggers limit order when price hits stop level
- More control but may not fill
- Use for: Precise exits with control

### Trailing Stop
- Stop that moves with the price
- Locks in profits while letting winners run
- Use for: Protecting profits dynamically

### Bracket Order
- Entry order with automatic profit target and stop loss
- All-in-one trade setup
- Use for: Complete trade management

## Risk Management Best Practices

1. **Always Use Stops** - Every position should have a stop loss
2. **Position Sizing** - Use the 1-2% risk rule
3. **R-Multiples** - Track P&L in terms of initial risk
4. **Diversification** - Don't overconcentrate in one symbol
5. **Paper Trading First** - Test strategies before going live
6. **Monitor Slippage** - Track execution quality
7. **Review Analytics** - Learn from execution data

## Troubleshooting

### Connection Issues

**Alpaca**:
- Verify API keys are correct
- Check if using paper or live keys correctly
- Ensure IP is not blocked

**TD Ameritrade**:
- Refresh token expires - need to re-authenticate
- Check if app is approved by TD
- Verify callback URL in app settings

**Interactive Brokers**:
- Ensure Gateway is running
- Check API settings in Gateway
- Verify SSL certificate acceptance

**TradeStation**:
- Refresh token expires - need to re-authenticate
- Check if using simulation vs live credentials
- Verify account has API access approved

### Order Rejections

Common reasons:
- Insufficient buying power
- Invalid symbol
- Market closed
- Order size too small/large
- Price collar violations
- Pattern day trader restrictions

Check order status and rejection reason in response.

## Security Notes

1. **Never commit credentials** - Use environment variables
2. **Use paper trading for testing** - Don't risk real money while testing
3. **Rotate API keys regularly** - Security best practice
4. **Monitor account activity** - Watch for unauthorized access
5. **Use IP whitelisting** - If broker supports it
6. **Keep tokens secure** - Treat like passwords

## Support

For broker-specific issues:
- Alpaca: https://alpaca.markets/support
- TD Ameritrade: https://developer.tdameritrade.com/community
- Interactive Brokers: https://www.interactivebrokers.com/support
- TradeStation: https://www.tradestation.com/support

For Legend AI issues:
- GitHub Issues: https://github.com/yourrepo/issues
- Documentation: /docs

## Legal Disclaimer

⚠️ **Trading involves substantial risk of loss.** This software is provided for informational and educational purposes only. It is not financial advice. Always:

- Understand the risks before trading
- Start with paper trading
- Never risk more than you can afford to lose
- Consider consulting a financial advisor
- Ensure compliance with local regulations

The developers are not responsible for any financial losses incurred through the use of this software.
