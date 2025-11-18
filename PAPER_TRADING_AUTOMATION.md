# Paper Trading Automation System

A comprehensive paper trading automation system for the Legend AI platform with full risk management, performance tracking, and broker integration stubs.

## Features

### 1. Signal Generation (`signal_generator.py`)
- Auto-detect entry signals from pattern scans
- Calculate optimal position sizing using 2% risk rule
- Set intelligent stop-loss and target prices
- Generate validated trading signals
- Signal strength classification (Weak, Moderate, Strong, Very Strong)

**Key Classes:**
- `TradingSignal` - Complete signal with entry/stop/target and position size
- `SignalGenerator` - Generates signals from pattern detection
- `create_manual_signal()` - Create signals manually for testing

### 2. Order Management (`order_manager.py`)
- Bracket orders (entry + stop loss + take profit)
- Trailing stops with percentage or dollar-based trailing
- Scale in/out logic for partial profits
- Time-based exits
- Order state management (pending, submitted, filled, cancelled)

**Key Classes:**
- `Order` - Individual order with full lifecycle tracking
- `BracketOrder` - Entry order linked to stop and target orders
- `TrailingStop` - Dynamic stop-loss that follows price
- `OrderManager` - Centralized order management

### 3. Risk Management (`portfolio_risk_manager.py`)
- Max loss per trade (default 2%)
- Max portfolio heat (default 6% - maximum total risk)
- Sector exposure limits (default 25% per sector)
- Correlation checks between positions
- Position-level and portfolio-level risk tracking

**Key Classes:**
- `PositionRisk` - Risk metrics for individual positions
- `PortfolioRisk` - Portfolio-wide risk assessment
- `PortfolioRiskManager` - Complete risk management system

### 4. Performance Tracking (`performance_tracker.py`)
- Track all paper trades with complete details
- Calculate comprehensive metrics (win rate, profit factor, expectancy, R-multiples)
- Generate performance reports
- Learn from mistakes with mistake tracking
- Export trades to JSON

**Key Classes:**
- `TradeRecord` - Detailed trade with P&L and learning notes
- `PerformanceMetrics` - Win rate, profit factor, expectancy, etc.
- `PerformanceReport` - Complete performance report with recommendations
- `PerformanceTracker` - Track and analyze all trades

### 5. Broker Integration (`broker_integration.py`)
- Paper broker for simulation
- Alpaca API integration stub
- Interactive Brokers integration stub
- Manual review queue for real trades
- Emergency kill switch

**Key Classes:**
- `BrokerInterface` - Abstract base for all brokers
- `PaperBroker` - Simulated execution
- `AlpacaBroker` - Alpaca API stub (requires implementation)
- `InteractiveBrokersBroker` - IB API stub (requires implementation)
- `KillSwitch` - Emergency stop for all trading
- `BrokerManager` - Manage multiple brokers with safety

### 6. Trading Automation (`trading_automation.py`)
- Main orchestrator integrating all components
- Automated signal processing and execution
- Portfolio monitoring and updates
- Risk-aware position management
- Daily loss limits with automatic kill switch

**Key Classes:**
- `AutomationConfig` - Configuration for automation
- `TradingAutomation` - Main automation orchestrator

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Trading Automation                        │
│  (Orchestrates all components)                              │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Signal     │   │    Order     │   │  Portfolio   │
│  Generator   │───│   Manager    │───│     Risk     │
└──────────────┘   └──────────────┘   └──────────────┘
        │                  │                  │
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Performance  │   │   Broker     │   │     Risk     │
│   Tracker    │   │ Integration  │   │  Calculator  │
└──────────────┘   └──────────────┘   └──────────────┘
```

## Usage

### Quick Start

```python
from app.services.trading_automation import TradingAutomation, AutomationConfig, AutomationMode
from app.services.signal_generator import create_manual_signal

# Configure automation
config = AutomationConfig(
    account_size=100000,
    risk_per_trade_pct=2.0,
    max_portfolio_heat_pct=6.0,
    automation_mode=AutomationMode.SEMI_AUTO
)

# Create automation system
automation = TradingAutomation(config)

# Create a signal
signal = create_manual_signal(
    ticker="AAPL",
    entry_price=150.00,
    stop_loss=145.00,
    target_price=160.00,
    account_size=100000
)

# Process the signal
bracket = automation.process_signal(signal)

# Execute the trade
automation.execute_signal(signal.signal_id)

# Update positions with current prices
automation.update_positions({"AAPL": 152.00})

# Close position
automation.close_position("AAPL", exit_price=155.00, reason="target_reached")

# Get portfolio status
status = automation.get_portfolio_status()
print(f"Portfolio Heat: {status['portfolio_heat']:.2f}%")
print(f"Win Rate: {status['performance']['win_rate']:.2f}%")

# Generate performance report
report = automation.generate_report(days=30)
```

### Example Workflows

See `examples/paper_trading_example.py` for complete examples:

```bash
python examples/paper_trading_example.py
```

## Configuration

### Automation Config

```python
config = AutomationConfig(
    # Account
    account_size=100000.0,

    # Risk parameters
    risk_per_trade_pct=2.0,           # 2% risk per trade
    max_portfolio_heat_pct=6.0,       # 6% max total risk
    max_sector_exposure_pct=25.0,     # 25% max per sector

    # Signal filters
    min_signal_strength=SignalStrength.MODERATE,
    min_risk_reward_ratio=2.0,
    min_pattern_score=60.0,

    # Order management
    use_bracket_orders=True,
    use_trailing_stops=True,
    trailing_stop_percent=5.0,
    scale_out_enabled=False,

    # Time-based rules
    max_days_in_trade=30,
    max_open_positions=5,

    # Execution
    automation_mode=AutomationMode.SEMI_AUTO,
    execution_mode=ExecutionMode.PAPER_ONLY,

    # Safety
    daily_loss_limit=2.0,  # % of account
    kill_switch_enabled=True
)
```

## Automation Modes

### 1. MANUAL
- Manual signal generation
- Manual execution
- Full control over every decision

### 2. SEMI_AUTO (Recommended)
- Automatic signal generation from patterns
- Manual review and execution
- Best balance of automation and safety

### 3. FULL_AUTO (Paper trading only)
- Fully automated signal generation and execution
- Use only for paper trading
- Requires additional safety checks for real trading

## Risk Management Rules

### Per-Trade Risk
- Default: 2% of account per trade
- Prevents any single trade from causing significant damage
- Automatically calculated position size

### Portfolio Heat
- Default: 6% maximum total risk across all positions
- Prevents over-exposure across the portfolio
- Limits new positions when heat is high

### Sector Exposure
- Default: 25% maximum per sector
- Ensures diversification
- Prevents sector-specific crashes

### Daily Loss Limit
- Default: 2% of account per day
- Automatically engages kill switch if exceeded
- Prevents emotional revenge trading

## Performance Metrics

The system tracks comprehensive performance metrics:

- **Win Rate**: Percentage of winning trades
- **Profit Factor**: Gross profit / Gross loss
- **Expectancy**: Average $ per trade
- **R-Multiple**: Profit/Loss in terms of initial risk
- **Average Win/Loss**: Mean profit and loss amounts
- **Streaks**: Current and longest win/loss streaks
- **By Category**: Performance breakdown by signal type and sector

## Safety Features

### Kill Switch
Emergency stop that halts all trading:

```python
# Engage kill switch
automation.broker_manager.engage_kill_switch(
    reason="Market crash detected",
    engaged_by="system"
)

# Check status
status = automation.broker_manager.kill_switch.status
print(f"Engaged: {status['engaged']}")
```

### Manual Review Queue
For real trading, all orders go through manual review:

```python
# Set execution mode to manual review
config.execution_mode = ExecutionMode.MANUAL_REVIEW

# Orders are queued for approval
pending = broker_manager.get_pending_requests()

# Approve or reject
broker_manager.approve_request(request_id, approved_by="user")
broker_manager.reject_request(request_id, reason="High volatility")
```

### Emergency Close All
Close all positions immediately:

```python
closed_count = automation.emergency_close_all(reason="market_crash")
print(f"Closed {closed_count} positions")
```

## Testing

Run the test suite:

```bash
# All tests
pytest tests/test_paper_trading_automation.py -v

# Specific test
pytest tests/test_paper_trading_automation.py::TestSignalGenerator -v

# With coverage
pytest tests/test_paper_trading_automation.py --cov=app.services
```

## Broker Integration

### Paper Trading (Implemented)
Fully functional paper trading with simulated execution.

### Alpaca (Stub)
To implement real Alpaca trading:

1. Install: `pip install alpaca-trade-api`
2. Add credentials to config
3. Implement API calls in `AlpacaBroker` class
4. Remove stub warnings

### Interactive Brokers (Stub)
To implement real IB trading:

1. Install: `pip install ib_insync`
2. Run TWS or IB Gateway
3. Implement API calls in `InteractiveBrokersBroker` class
4. Remove stub warnings

## Integration with Legend AI

The automation system integrates with existing Legend AI components:

- **Pattern Detection** → Signal Generation
- **Risk Calculator** → Position Sizing
- **Trade Manager** → Performance Tracking
- **Market Data** → Price Updates

### Generate Signals from Pattern Scans

```python
from app.models import PatternScan
from app.services.signal_generator import SignalGenerator
from app.services.risk_calculator import RiskCalculator

# Get pattern scan from database
pattern_scan = db.query(PatternScan).filter(...).first()

# Generate signal
risk_calc = RiskCalculator()
signal_gen = SignalGenerator(risk_calc)

signal = signal_gen.generate_signal_from_pattern(
    pattern_scan=pattern_scan,
    account_size=100000,
    risk_per_trade_pct=2.0
)

# Process with automation
if signal:
    automation.process_signal(signal)
```

## File Structure

```
app/services/
├── signal_generator.py           # Signal generation
├── order_manager.py              # Order management
├── portfolio_risk_manager.py     # Portfolio risk
├── performance_tracker.py        # Performance tracking
├── broker_integration.py         # Broker APIs
├── trading_automation.py         # Main orchestrator
├── risk_calculator.py           # Position sizing (existing)
└── trades.py                     # Trade management (existing)

examples/
└── paper_trading_example.py      # Example usage

tests/
└── test_paper_trading_automation.py  # Test suite
```

## Best Practices

1. **Start with Paper Trading**: Test thoroughly before real money
2. **Use Semi-Auto Mode**: Manual review prevents costly mistakes
3. **Monitor Portfolio Heat**: Don't exceed 6% total risk
4. **Review Performance Reports**: Learn from wins and losses
5. **Track Mistakes**: Use mistake tracking to improve
6. **Respect the Kill Switch**: Don't override safety features
7. **Diversify Sectors**: Don't concentrate in one sector
8. **Use Trailing Stops**: Protect profits as they grow
9. **Set Time Limits**: Exit stale positions after 30 days
10. **Check Daily Limits**: Stop trading after hitting daily loss limit

## Performance Tracking & Learning

### Track Mistakes

```python
from app.services.performance_tracker import MistakeCategory

# Record a mistake
tracker.add_mistake(
    trade_id="TRADE_001",
    mistake_category=MistakeCategory.PREMATURE_EXIT,
    description="Sold at first resistance instead of target"
)

# Record a lesson
tracker.add_lesson(
    trade_id="TRADE_001",
    lesson="Wait for target or stop, don't exit early on noise"
)
```

### Generate Reports

```python
# Get detailed report
report = automation.generate_report(days=30)

# Review recommendations
for recommendation in report['recommendations']:
    print(f"📊 {recommendation}")

# Review common mistakes
for mistake, count in report['common_mistakes'].items():
    print(f"⚠ {mistake}: {count} times")
```

## Future Enhancements

- [ ] Machine learning for signal quality scoring
- [ ] Advanced correlation analysis
- [ ] Multi-timeframe analysis
- [ ] Options strategies integration
- [ ] Real-time market data integration
- [ ] Advanced scaling strategies
- [ ] Portfolio optimization
- [ ] Tax-loss harvesting
- [ ] Backtesting framework
- [ ] Strategy parameters optimization

## Support

For issues or questions:
- Check `examples/paper_trading_example.py` for usage examples
- Review tests in `tests/test_paper_trading_automation.py`
- See inline documentation in each module

## License

Part of the Legend AI project.
