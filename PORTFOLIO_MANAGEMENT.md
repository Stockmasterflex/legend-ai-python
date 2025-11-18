# Portfolio Management System

Comprehensive portfolio management with position tracking, performance analytics, risk management, and trade journaling.

## Features Overview

### 1. Position Tracking
- **Add/Remove Positions**: Manage portfolio positions with automatic cost basis calculation
- **Real-time P&L**: Live profit/loss tracking with current market prices
- **Cost Basis Tracking**: Average cost basis with support for adding to positions
- **Allocation Pie Chart**: Visual portfolio allocation breakdown

### 2. Performance Analytics
- **Daily/Weekly/Monthly Returns**: Calculate returns across different time periods
- **Benchmark Comparison**: Compare performance against SPY or custom benchmarks
- **Best/Worst Performers**: Identify top and bottom performing positions
- **Risk-Adjusted Returns**: Sharpe ratio, Sortino ratio, max drawdown

### 3. Risk Management
- **Position Sizing Calculator**: 2% rule with optional Kelly Criterion
- **Portfolio Heat**: Total risk exposure tracking
- **Correlation Matrix**: Analyze position correlations for diversification
- **Diversification Score**: 0-100 score with letter grade (A+ to F)

### 4. Trade Journal
- **Entry/Exit Notes**: Document why you entered and exited trades
- **Screenshots**: Attach chart screenshots to trades
- **Lessons Learned**: Post-trade reflection and analysis
- **Performance Tags**: Categorize trades (win, loss, breakout, etc.)

---

## API Endpoints

### Portfolio Management (`/api/portfolio`)

#### Create Portfolio
```http
POST /api/portfolio/create
Content-Type: application/json

{
  "user_id": "default",
  "name": "My Portfolio",
  "initial_capital": 100000
}
```

#### Add Position
```http
POST /api/portfolio/position/add
Content-Type: application/json

{
  "portfolio_id": 1,
  "symbol": "AAPL",
  "quantity": 100,
  "entry_price": 175.50,
  "stop_loss": 170.00,
  "target_price": 185.00,
  "notes": "Strong VCP pattern, RS > 90"
}
```

#### Remove Position
```http
POST /api/portfolio/position/remove
Content-Type: application/json

{
  "position_id": 1,
  "quantity": 50,  // Optional: partial exit
  "exit_price": 182.50  // Optional: uses current price if not provided
}
```

#### Get Portfolio Metrics
```http
GET /api/portfolio/{portfolio_id}/metrics
```

Returns:
- Total portfolio value
- Cash balance
- Total P&L and return %
- Number of positions
- Position allocations with percentages

#### Get Allocation Data
```http
GET /api/portfolio/{portfolio_id}/allocation
```

Returns pie chart data:
```json
{
  "labels": ["AAPL", "MSFT", "GOOGL", "Cash"],
  "values": [25000, 18000, 15000, 42000],
  "percentages": [25.0, 18.0, 15.0, 42.0]
}
```

---

### Performance Analytics (`/api/performance`)

#### Calculate Returns
```http
GET /api/performance/{portfolio_id}/returns?period=daily
```

Periods: `daily`, `weekly`, `monthly`

Returns:
- Current value
- Total return ($)
- Total return (%)
- Annualized return (%)

#### Benchmark Comparison
```http
GET /api/performance/{portfolio_id}/benchmark?benchmark=SPY&period_days=30
```

Returns:
- Portfolio return %
- Benchmark return %
- Alpha (excess return)
- Relative performance (outperforming/underperforming)

#### Get Best/Worst Performers
```http
GET /api/performance/{portfolio_id}/performers
```

Returns:
- Top 5 best performing positions
- Top 5 worst performing positions
- Each with symbol, P&L, P&L %, position size

#### Risk-Adjusted Returns
```http
GET /api/performance/{portfolio_id}/risk-adjusted
```

Returns:
- Sharpe ratio
- Sortino ratio
- Max drawdown (%)
- Mean return and volatility

#### Performance Summary
```http
GET /api/performance/{portfolio_id}/summary
```

Comprehensive report with:
- Returns metrics
- Benchmark comparison
- Best/worst performers
- Risk-adjusted metrics
- Trade statistics (win rate, profit factor, etc.)

---

### Risk Analytics (`/api/risk-analytics`)

#### Position Size Calculator
```http
POST /api/risk-analytics/position-size
Content-Type: application/json

{
  "portfolio_id": 1,
  "symbol": "TSLA",
  "entry_price": 250.00,
  "stop_loss": 242.00,
  "risk_percent": 2.0,
  "use_kelly": true,
  "win_rate": 0.65,
  "avg_win_loss_ratio": 2.5
}
```

Returns:
- Recommended shares (2% rule)
- Position value
- Dollar risk
- Kelly Criterion sizing (if enabled)
- Conservative/aggressive alternatives

#### Portfolio Heat
```http
GET /api/risk-analytics/{portfolio_id}/portfolio-heat
```

Returns:
- Total heat % (sum of all position risks)
- Risk level: LOW/MODERATE/HIGH/CRITICAL
- Recommendations
- Individual position risks
- Max recommended heat (10%)

#### Correlation Matrix
```http
GET /api/risk-analytics/{portfolio_id}/correlation-matrix?period_days=60
```

Returns:
- NxN correlation matrix
- List of symbols
- Highly correlated pairs (>0.7)
- Average correlation

#### Diversification Score
```http
GET /api/risk-analytics/{portfolio_id}/diversification-score
```

Returns:
- Score (0-100)
- Letter grade (A+ to F)
- Factor breakdown:
  - Number of positions (0-25 points)
  - Sector diversity (0-25 points)
  - Position concentration (0-25 points)
  - Correlation (0-25 points)
- Recommendations for improvement

#### Risk Summary
```http
GET /api/risk-analytics/{portfolio_id}/risk-summary
```

Comprehensive risk report with:
- Portfolio heat
- Diversification score
- Average correlation
- Risk recommendations

---

### Trade Journal (`/api/journal`)

#### Log Trade Entry
```http
POST /api/journal/entry
Content-Type: application/json

{
  "portfolio_id": 1,
  "symbol": "NVDA",
  "quantity": 50,
  "entry_price": 485.00,
  "entry_reason": "Breaking out of 3-week VCP pattern with volume",
  "setup_type": "VCP",
  "screenshot_url": "https://example.com/chart.png",
  "emotions": "Confident, patient",
  "tags": ["vcp", "breakout", "tech"],
  "position_id": 5
}
```

#### Log Trade Exit
```http
POST /api/journal/exit
Content-Type: application/json

{
  "portfolio_id": 1,
  "symbol": "NVDA",
  "quantity": 50,
  "exit_price": 510.00,
  "entry_price": 485.00,
  "exit_reason": "Hit profit target, showed weakness",
  "lessons_learned": "Good patience waiting for setup. Should have taken partial profit at resistance.",
  "mistakes_made": "Didn't take partial profit at obvious resistance level",
  "what_went_well": "Entry timing was excellent, respected stop loss plan",
  "screenshot_url": "https://example.com/exit-chart.png",
  "emotions": "Satisfied but slightly greedy",
  "trade_grade": "B+",
  "tags": ["win", "vcp"],
  "position_id": 5
}
```

Auto-calculates:
- Profit/loss ($)
- Profit/loss (%)
- Auto-tags as "win" or "loss"

#### Update Journal Entry
```http
PUT /api/journal/{journal_id}
Content-Type: application/json

{
  "lessons_learned": "Updated lessons after review",
  "trade_grade": "A-"
}
```

#### Get Journal Entries
```http
GET /api/journal/{portfolio_id}/entries?trade_type=exit&symbol=AAPL&tags=win&limit=50
```

Filters:
- `trade_type`: entry/exit
- `symbol`: filter by ticker
- `tags`: comma-separated tags
- `limit`: max entries (1-200)

#### Get Journal Statistics
```http
GET /api/journal/{portfolio_id}/statistics
```

Returns:
- Total trades
- Win/loss counts
- Win rate %
- Net P&L
- Average win/loss
- Setup type performance
- Tag distribution
- Grade distribution
- Recent lessons learned

#### Get Trade Review
```http
GET /api/journal/entry/{journal_id}
```

Returns complete trade details with related entries (multiple entries/exits for same position)

#### Get Lessons Learned
```http
GET /api/journal/{portfolio_id}/lessons?limit=20
```

Returns recent lessons from closed trades

---

## Database Models

### Portfolio
- `id`: Primary key
- `user_id`: User identifier
- `name`: Portfolio name
- `initial_capital`: Starting capital
- `cash_balance`: Current cash
- `total_value`: Cached portfolio value
- `created_at`, `updated_at`: Timestamps

### Position
- `id`: Primary key
- `portfolio_id`: Foreign key to portfolio
- `ticker_id`: Foreign key to ticker
- `quantity`: Number of shares
- `avg_cost_basis`: Average entry price
- `current_price`: Latest market price
- `total_cost`: Total invested
- `current_value`: Current market value
- `unrealized_pnl`: Unrealized profit/loss
- `unrealized_pnl_pct`: P&L percentage
- `stop_loss`: Stop loss price
- `target_price`: Target price
- `position_size_pct`: % of portfolio
- `status`: open/closed/partial
- `opened_at`, `closed_at`: Timestamps
- `notes`: Position notes

### TradeJournal
- `id`: Primary key
- `portfolio_id`: Foreign key to portfolio
- `position_id`: Foreign key to position (optional)
- `ticker_id`: Foreign key to ticker
- `trade_type`: entry/exit/add/trim
- `quantity`: Number of shares
- `price`: Trade price
- `entry_reason`: Why entered
- `exit_reason`: Why exited
- `setup_type`: Pattern/setup used
- `screenshot_url`: Chart screenshot
- `lessons_learned`: Post-trade reflection
- `emotions`: Emotional state
- `tags`: Comma-separated tags
- `r_multiple`: Risk multiple achieved
- `profit_loss`: Realized P&L
- `profit_loss_pct`: P&L percentage
- `trade_grade`: A+ to F
- `mistakes_made`: What went wrong
- `what_went_well`: What went right
- `traded_at`, `created_at`, `updated_at`: Timestamps

---

## Usage Examples

### Complete Workflow

1. **Create Portfolio**
```bash
curl -X POST http://localhost:8000/api/portfolio/create \
  -H "Content-Type: application/json" \
  -d '{"name":"Tech Growth","initial_capital":50000}'
```

2. **Add Position**
```bash
curl -X POST http://localhost:8000/api/portfolio/position/add \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_id":1,
    "symbol":"AAPL",
    "quantity":100,
    "entry_price":175.50,
    "stop_loss":170.00,
    "notes":"Strong momentum"
  }'
```

3. **Log Entry in Journal**
```bash
curl -X POST http://localhost:8000/api/journal/entry \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_id":1,
    "symbol":"AAPL",
    "quantity":100,
    "entry_price":175.50,
    "entry_reason":"Breaking out above 50MA with increasing volume",
    "setup_type":"Cup & Handle"
  }'
```

4. **Check Portfolio Metrics**
```bash
curl http://localhost:8000/api/portfolio/1/metrics
```

5. **Calculate Position Size**
```bash
curl -X POST http://localhost:8000/api/risk-analytics/position-size \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_id":1,
    "symbol":"MSFT",
    "entry_price":380.00,
    "stop_loss":370.00,
    "risk_percent":2.0
  }'
```

6. **Check Diversification**
```bash
curl http://localhost:8000/api/risk-analytics/1/diversification-score
```

7. **Close Position & Log Exit**
```bash
# Close position
curl -X POST http://localhost:8000/api/portfolio/position/remove \
  -H "Content-Type: application/json" \
  -d '{"position_id":1,"exit_price":185.00}'

# Log exit in journal
curl -X POST http://localhost:8000/api/journal/exit \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_id":1,
    "symbol":"AAPL",
    "quantity":100,
    "exit_price":185.00,
    "entry_price":175.50,
    "exit_reason":"Hit profit target",
    "lessons_learned":"Great setup, followed plan perfectly",
    "trade_grade":"A"
  }'
```

8. **Get Performance Summary**
```bash
curl http://localhost:8000/api/performance/1/summary
```

---

## Migration

Run database migration to create new tables:

```bash
alembic upgrade head
```

Or manually run:
```bash
python -c "from app.services.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

---

## Visualization

The system includes utilities for generating:
- **Pie Charts**: Portfolio allocation
- **Correlation Heatmaps**: Position correlations
- **Performance Charts**: Portfolio vs benchmark
- **Bar Charts**: Best/worst performers
- **Gauge Charts**: Diversification score

Access via `/api/portfolio/{id}/allocation` and other endpoints.

---

## Features Summary

✅ Position Tracking with Real-time P&L
✅ Cost Basis Tracking
✅ Allocation Pie Charts
✅ Daily/Weekly/Monthly Returns
✅ Benchmark Comparison (SPY)
✅ Best/Worst Performers
✅ Risk-Adjusted Returns (Sharpe, Sortino)
✅ Position Sizing Calculator (2% rule + Kelly)
✅ Portfolio Heat Tracking
✅ Correlation Matrix
✅ Diversification Score
✅ Trade Journal with Entry/Exit Notes
✅ Screenshot Support
✅ Lessons Learned Tracking
✅ Performance Tags

---

## Next Steps

1. Access interactive API docs at `/docs`
2. Create your first portfolio
3. Add positions and track P&L
4. Use position sizing calculator for new trades
5. Monitor portfolio heat and diversification
6. Keep detailed trade journal for continuous improvement

For questions or issues, check `/docs` for complete API documentation.
