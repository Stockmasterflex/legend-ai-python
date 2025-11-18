# Professional Trade Journaling System

A comprehensive trade journaling system for professional traders to track, analyze, and improve their trading performance.

## Features

### 1. Trade Entry Forms
- **Pre-trade checklist** - Ensure all criteria are met before entering
- **Pattern identification** - Link trades to specific patterns (VCP, Cup & Handle, etc.)
- **Risk/reward calculation** - Automatic calculation of position sizing and R:R
- **Thesis documentation** - Record your trading thesis before entry
- **Screenshot capture** - Store chart screenshots for later review

### 2. Trade Tracking
- **Entry/exit timestamps** - Precise tracking of trade timing
- **Slippage tracking** - Monitor execution quality
- **Emotional state logging** - Track your psychology during trades
- **Market conditions** - Record market context
- **Follow-through notes** - Document trade progression

### 3. Performance Analytics
- **Win rate by pattern** - See which setups work best for you
- **R-multiple distribution** - Track actual vs planned risk/reward
- **Time in trade analysis** - Understand your holding periods
- **Best/worst trade reviews** - Learn from extremes
- **Mistake categorization** - Identify patterns in errors

### 4. Learning System
- **Tag trades by lesson** - Organize trades by learning opportunities
- **Create playbooks** - Document your repeatable strategies
- **Pattern success rates** - Track performance by setup type
- **Improvement tracking** - Monitor progress over time
- **Review reminders** - Accountability features

### 5. Export & Reporting
- **CSV exports** - Export for spreadsheet analysis
- **Tax reports** - IRS Form 8949 compatible exports
- **Performance letters** - Monthly/quarterly reports
- **Accountability reports** - Track discipline and rule adherence
- **JSON exports** - Full data exports for custom analysis

## API Endpoints

### Pre-Trade Planning

#### Create Trade Plan
```http
POST /api/journal/plan/create
```

Create a pre-trade plan with checklist before execution.

**Request Body:**
```json
{
  "ticker": "AAPL",
  "pattern_identified": "VCP",
  "thesis": "Strong breakout setup with volume dry-up and tight consolidation",
  "planned_entry": 150.00,
  "planned_stop": 145.00,
  "planned_target": 160.00,
  "planned_position_size": 100,
  "checklist_data": {
    "trend_aligned": true,
    "volume_confirmation": true,
    "risk_defined": true
  },
  "screenshot_url": "https://..."
}
```

#### Complete Checklist
```http
POST /api/journal/plan/checklist
```

Complete pre-trade checklist verification.

### Trade Execution

#### Execute Entry
```http
POST /api/journal/execute/entry
```

Execute trade entry and track slippage.

**Request Body:**
```json
{
  "trade_id": "TRD-20241118-abc123",
  "actual_entry_price": 150.50,
  "actual_position_size": 100,
  "emotional_state": "confident",
  "market_condition": "trending_up",
  "market_context": "SPY bullish, sector strength"
}
```

#### Partial Exit
```http
POST /api/journal/execute/partial-exit
```

Record partial position exits.

#### Execute Exit
```http
POST /api/journal/execute/exit
```

Close trade and calculate final metrics.

**Request Body:**
```json
{
  "trade_id": "TRD-20241118-abc123",
  "exit_price": 160.00,
  "exit_reason": "target",
  "emotional_state": "disciplined",
  "fees_paid": 10.00
}
```

### Post-Trade Review

#### Add Trade Notes
```http
POST /api/journal/review/notes
```

Add post-trade review notes.

**Request Body:**
```json
{
  "trade_id": "TRD-20241118-abc123",
  "what_went_well": "Perfect entry timing, followed the plan",
  "what_went_wrong": "Could have held longer for bigger gain",
  "lessons_learned": "Trust the setup and let winners run"
}
```

#### Add Tag
```http
POST /api/journal/review/tag
```

Tag trades for organization.

**Examples:** `perfect_execution`, `revenge_trade`, `emotional`, `lesson`

#### Add Mistake
```http
POST /api/journal/review/mistake
```

Categorize trading mistakes.

**Categories:** `entry`, `exit`, `sizing`, `emotional`, `planning`

### Learning System

#### Create Playbook
```http
POST /api/journal/playbook/create
```

Document repeatable trading strategies.

**Request Body:**
```json
{
  "name": "VCP Breakout Strategy",
  "description": "Classic VCP pattern with 3-4 contractions",
  "pattern_type": "VCP",
  "entry_criteria": [
    "Volume dry-up visible",
    "Tight consolidation (< 10% range)",
    "Above 21 EMA",
    "RS rating > 80"
  ],
  "exit_criteria": [
    "Hit target (2R minimum)",
    "Stop loss triggered",
    "Pattern breaks down"
  ],
  "risk_management": {
    "max_risk_per_trade": 1.0,
    "position_sizing": "1% rule",
    "max_position_size": 10000
  }
}
```

#### Add Lesson
```http
POST /api/journal/lesson/add
```

Record trading lessons learned.

### Analytics

#### Get Trades
```http
GET /api/journal/trades?status=closed&pattern=VCP&limit=50
```

Query trades with filters.

**Query Parameters:**
- `user_id` - User identifier (default: "default")
- `status` - planned, open, closed, cancelled
- `pattern` - Pattern type filter
- `tags` - Comma-separated tags
- `start_date` - ISO format date
- `end_date` - ISO format date
- `limit` - Max results (default: 50)

#### Performance Analytics
```http
GET /api/journal/analytics/performance
```

Get comprehensive performance metrics.

**Response:**
```json
{
  "success": true,
  "analytics": {
    "total_trades": 50,
    "winning_trades": 32,
    "losing_trades": 18,
    "win_rate": 64.0,
    "total_pnl": 15000.00,
    "average_win": 800.00,
    "average_loss": -350.00,
    "average_r_multiple": 1.85,
    "best_trade": {
      "trade_id": "TRD-20241101-xyz",
      "pnl": 3500.00,
      "r_multiple": 4.2
    },
    "worst_trade": {
      "trade_id": "TRD-20241015-abc",
      "pnl": -980.00,
      "r_multiple": -1.96
    },
    "avg_holding_time_hours": 48.5
  }
}
```

#### Pattern Performance
```http
GET /api/journal/analytics/patterns
```

Performance breakdown by pattern type.

#### Mistake Analysis
```http
GET /api/journal/analytics/mistakes
```

Analyze common trading mistakes.

### Export & Reporting

#### CSV Export
```http
GET /api/journal/export/csv?start_date=2024-01-01
```

Export trades to CSV format.

#### Tax Report
```http
GET /api/journal/export/tax-report?year=2024
```

IRS Form 8949 compatible tax report.

#### Performance Letter
```http
GET /api/journal/reports/performance-letter?period=monthly
```

Professional trading report.

**Periods:** `daily`, `weekly`, `monthly`, `quarterly`, `yearly`

#### Accountability Report
```http
GET /api/journal/reports/accountability
```

Track discipline, planning, and rule adherence.

## Workflow Example

### Complete Trade Flow

1. **Plan the Trade**
   ```bash
   POST /api/journal/plan/create
   # Creates trade plan with thesis and risk/reward
   ```

2. **Complete Checklist**
   ```bash
   POST /api/journal/plan/checklist
   # Verify all entry criteria met
   ```

3. **Execute Entry**
   ```bash
   POST /api/journal/execute/entry
   # Record actual entry with slippage tracking
   ```

4. **Manage Position** (optional)
   ```bash
   POST /api/journal/execute/partial-exit
   # Scale out of position
   ```

5. **Execute Exit**
   ```bash
   POST /api/journal/execute/exit
   # Close trade, calculate P&L and metrics
   ```

6. **Review Trade**
   ```bash
   POST /api/journal/review/notes
   POST /api/journal/review/tag
   POST /api/journal/review/mistake
   # Document learnings and mistakes
   ```

## Database Schema

### TradeJournal
Main trade journal entry with comprehensive tracking.

**Key Fields:**
- Pre-trade: thesis, planned entry/stop/target, checklist
- Execution: actual prices, slippage, timestamps
- Performance: P&L, R-multiple, holding period
- Psychology: emotional states, market conditions
- Review: notes, lessons, follow-through

### Supporting Tables
- **TradeTag** - Trade organization tags
- **TradeMistake** - Categorized mistakes
- **Playbook** - Trading strategies
- **TradeLesson** - Knowledge base
- **TradeReview** - Periodic performance reviews

## Enumerations

### TradeStatus
- `PLANNED` - Trade plan created, not executed
- `OPEN` - Position entered
- `CLOSED` - Position exited
- `CANCELLED` - Plan cancelled before entry

### EmotionalState
- `CONFIDENT` - High conviction
- `FEARFUL` - Fear-based decision
- `GREEDY` - Greed-influenced
- `NEUTRAL` - Emotionally neutral
- `ANXIOUS` - Nervous/anxious
- `DISCIPLINED` - Following plan strictly
- `IMPULSIVE` - Impulse decision

### MarketCondition
- `TRENDING_UP` - Bullish market
- `TRENDING_DOWN` - Bearish market
- `CONSOLIDATING` - Range-bound
- `VOLATILE` - High volatility
- `QUIET` - Low volatility

## Best Practices

### 1. Always Plan Before Trading
Create a trade plan BEFORE entering. This forces you to think through:
- Why are you taking this trade?
- What's your edge?
- What's your risk/reward?
- What are your exit criteria?

### 2. Complete the Checklist
Use the pre-trade checklist to ensure all criteria are met:
- Is the trend aligned?
- Do you have volume confirmation?
- Is risk properly defined?
- Have you sized the position correctly?

### 3. Track Everything
Record all trade details:
- Exact entry/exit prices
- Slippage and fees
- Your emotional state
- Market conditions

### 4. Review Every Trade
After closing a trade, review:
- What went well?
- What went wrong?
- What did you learn?
- Tag appropriately
- Categorize any mistakes

### 5. Use Playbooks
Create playbooks for your best setups:
- Document exact entry criteria
- Define exit rules
- Specify risk management
- Track success rate over time

### 6. Regular Analysis
- Review performance weekly/monthly
- Analyze pattern success rates
- Identify mistake patterns
- Track improvement areas

### 7. Export for Taxes
At year-end, export tax reports for easy filing:
```bash
GET /api/journal/export/tax-report?year=2024
```

## Testing

Run the test suite:
```bash
pytest tests/test_trade_journal.py -v
```

## Database Migration

Apply migrations:
```bash
alembic upgrade head
```

Create new migration:
```bash
alembic revision --autogenerate -m "description"
```

## Integration with Existing Features

The trade journal integrates seamlessly with:
- **Pattern Scanner** - Link trades to detected patterns
- **Watchlist** - Track trades from watchlist alerts
- **Risk Calculator** - Use calculated position sizes
- **AI Assistant** - Get trade reviews from AI
- **Charts** - Store chart screenshots with trades

## Performance Metrics Explained

### Win Rate
Percentage of profitable trades: `Wins / Total Trades * 100`

### R-Multiple
Actual profit/loss divided by initial risk: `Net P&L / Planned Risk`
- 1R = Risked $500, made $500
- 2R = Risked $500, made $1000
- -1R = Risked $500, lost $500

### Expectancy
Average expected profit per trade:
`(Win Rate × Avg Win) + ((1 - Win Rate) × Avg Loss)`

### MAE (Maximum Adverse Excursion)
Largest unrealized loss during the trade.

### MFE (Maximum Favorable Excursion)
Largest unrealized profit during the trade.

## Support

For issues or questions:
- API Documentation: `/docs`
- Health Check: `/api/journal/health`
- Error Logs: Check application logs

## License

Part of the Legend AI Trading Platform
