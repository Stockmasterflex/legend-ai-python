# Historical Playback & Simulation Features

Comprehensive guide to time-traveling through historical data, paper trading, what-if analysis, and pattern recognition training.

## Table of Contents

1. [Historical Playback](#historical-playback)
2. [Simulation Trading](#simulation-trading)
3. [What-If Analysis](#what-if-analysis)
4. [Pattern Recognition Training](#pattern-recognition-training)

---

## Historical Playback

Time-travel through historical market data with full playback controls.

### Features

- **Replay any historical date range**
- **Variable playback speed** (0.5x to 5x)
- **Pause and analyze** specific moments
- **Seek to specific dates**
- **Step forward/backward** bar by bar
- **Add annotations** to mark key moments
- **Bookmark sessions** for later review
- **Share replays** with unique URLs

### API Endpoints

#### Create Playback Session

```http
POST /api/playback/create
```

**Request Body:**
```json
{
  "user_id": "user123",
  "ticker": "AAPL",
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-06-30T00:00:00Z",
  "interval": "1day"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "playback_id": 1,
    "ticker": "AAPL",
    "start_date": "2024-01-01T00:00:00+00:00",
    "end_date": "2024-06-30T00:00:00+00:00",
    "current_position": "2024-01-01T00:00:00+00:00",
    "status": "paused",
    "interval": "1day",
    "playback_speed": 1.0
  }
}
```

#### Control Playback

**Play/Resume:**
```http
POST /api/playback/{playback_id}/play
```

**Request Body:**
```json
{
  "speed": 2.0
}
```

**Pause:**
```http
POST /api/playback/{playback_id}/pause
```

**Seek to Date:**
```http
POST /api/playback/{playback_id}/seek
```

**Request Body:**
```json
{
  "target_date": "2024-03-15T00:00:00Z"
}
```

**Step Forward/Backward:**
```http
POST /api/playback/{playback_id}/step
```

**Request Body:**
```json
{
  "steps": 5
}
```
Use negative values to step backward.

#### Get Current State

```http
GET /api/playback/{playback_id}/state
```

**Response:**
```json
{
  "success": true,
  "data": {
    "playback_id": 1,
    "ticker": "AAPL",
    "status": "playing",
    "current_position": "2024-03-15T00:00:00+00:00",
    "playback_speed": 1.0,
    "current_bar": {
      "timestamp": "2024-03-15T00:00:00",
      "open": 175.50,
      "high": 177.25,
      "low": 175.00,
      "close": 176.80,
      "volume": 85432100
    },
    "visible_data": {
      "timestamps": ["2024-01-01", "2024-01-02", ...],
      "open": [170.25, 171.00, ...],
      "high": [172.50, 172.75, ...],
      "low": [169.80, 170.50, ...],
      "close": [171.50, 171.25, ...],
      "volume": [90123456, 88765432, ...]
    },
    "progress": {
      "current_bar": 73,
      "total_bars": 126,
      "percentage": 57.94
    }
  }
}
```

#### Add Annotations

```http
POST /api/playback/{playback_id}/annotate
```

**Request Body:**
```json
{
  "annotation_type": "entry",
  "title": "Perfect VCP Entry",
  "content": "Volume dried up nicely, tight consolidation near highs",
  "price_level": 176.80,
  "metadata": {
    "pattern": "VCP",
    "stage": 3
  }
}
```

**Annotation Types:**
- `note` - General observation
- `entry` - Entry point marker
- `exit` - Exit point marker
- `pattern` - Pattern identification
- `support` - Support level
- `resistance` - Resistance level

#### Bookmark & Share

**Create Bookmark:**
```http
POST /api/playback/{playback_id}/bookmark?user_id=user123
```

**Request Body:**
```json
{
  "name": "AAPL VCP Breakout March 2024",
  "description": "Perfect example of volume contraction",
  "tags": ["VCP", "breakout", "teaching"]
}
```

**Share Replay:**
```http
POST /api/playback/{playback_id}/share?user_id=user123
```

**Request Body:**
```json
{
  "title": "AAPL VCP Study",
  "description": "Educational replay showing classic VCP formation",
  "is_public": true,
  "expiration_days": 30
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "share_id": 5,
    "share_token": "abc123def456...",
    "share_url": "/replay/shared/abc123def456...",
    "title": "AAPL VCP Study",
    "is_public": true,
    "expiration_date": "2024-04-15T00:00:00+00:00"
  }
}
```

---

## Simulation Trading

Risk-free paper trading environment to practice strategies and test setups.

### Features

- **Multiple simulation accounts**
- **Full P&L tracking**
- **Long and short positions**
- **Stop loss and target management**
- **Comprehensive statistics**
- **Equity curve visualization**
- **Performance analytics**

### API Endpoints

#### Create Simulation Account

```http
POST /api/simulation/accounts/create
```

**Request Body:**
```json
{
  "user_id": "user123",
  "name": "VCP Strategy Testing",
  "initial_balance": 100000.0
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "account_id": 1,
    "user_id": "user123",
    "name": "VCP Strategy Testing",
    "initial_balance": 100000.0,
    "current_balance": 100000.0,
    "cash_balance": 100000.0,
    "total_pnl": 0.0,
    "total_trades": 0,
    "status": "active"
  }
}
```

#### Enter Trade

```http
POST /api/simulation/accounts/{account_id}/trades/enter
```

**Request Body:**
```json
{
  "ticker": "TSLA",
  "entry_price": 245.50,
  "position_size": 100,
  "trade_type": "long",
  "stop_loss": 238.00,
  "target_price": 265.00,
  "notes": "VCP breakout, volume contraction complete"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "trade_id": 1,
    "ticker": "TSLA",
    "entry_price": 245.50,
    "position_size": 100,
    "stop_loss": 238.00,
    "target_price": 265.00,
    "status": "open",
    "cost": 24550.0
  }
}
```

#### Exit Trade

```http
POST /api/simulation/trades/{trade_id}/exit
```

**Request Body:**
```json
{
  "exit_price": 262.00,
  "exit_reason": "target"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "trade_id": 1,
    "ticker": "TSLA",
    "entry_price": 245.50,
    "exit_price": 262.00,
    "position_size": 100,
    "pnl": 1650.0,
    "pnl_pct": 6.72,
    "r_multiple": 2.2,
    "status": "closed"
  }
}
```

#### Get Statistics

```http
GET /api/simulation/accounts/{account_id}/statistics
```

**Response:**
```json
{
  "success": true,
  "data": {
    "account_id": 1,
    "total_trades": 25,
    "winning_trades": 16,
    "losing_trades": 9,
    "win_rate": 64.0,
    "total_pnl": 12450.50,
    "total_pnl_pct": 12.45,
    "avg_win": 1250.75,
    "avg_loss": -625.30,
    "largest_win": 3200.00,
    "largest_loss": -1150.00,
    "profit_factor": 2.15,
    "avg_r_multiple": 1.85,
    "expectancy": 498.02,
    "max_win_streak": 7,
    "max_loss_streak": 3,
    "max_drawdown": -8.5
  }
}
```

#### Get Equity Curve

```http
GET /api/simulation/accounts/{account_id}/equity-curve
```

**Response:**
```json
{
  "success": true,
  "data": {
    "account_id": 1,
    "equity_curve": [
      {"date": "2024-01-01T00:00:00", "equity": 100000, "trade_number": 0},
      {"date": "2024-01-15T00:00:00", "equity": 101650, "trade_number": 1, "pnl": 1650, "ticker": "TSLA"},
      ...
    ],
    "drawdown_curve": [
      {"date": "2024-01-01T00:00:00", "drawdown": 0},
      {"date": "2024-01-15T00:00:00", "drawdown": 0},
      ...
    ],
    "final_equity": 112450.50,
    "peak_equity": 115230.00
  }
}
```

---

## What-If Analysis

Explore alternative scenarios to learn from past trades.

### Features

- **Entry timing analysis** - "What if I entered earlier/later?"
- **Exit timing analysis** - "What if I held longer?"
- **Position sizing** - "What if I traded more/fewer shares?"
- **Stop loss analysis** - "What if I used a different stop?"
- **Save scenarios** for future reference
- **Compare outcomes** side-by-side

### API Endpoints

#### Analyze Entry Timing

```http
POST /api/whatif/entry-timing
```

**Request Body:**
```json
{
  "user_id": "user123",
  "ticker": "NVDA",
  "base_entry_date": "2024-03-15T00:00:00Z",
  "base_entry_price": 875.50,
  "alternative_entry_date": "2024-03-10T00:00:00Z",
  "exit_date": "2024-04-15T00:00:00Z",
  "position_size": 100,
  "scenario_name": "NVDA Early Entry Test"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "scenario_id": 1,
    "ticker": "NVDA",
    "base_scenario": {
      "entry_date": "2024-03-15T00:00:00",
      "entry_price": 875.50,
      "pnl": 5250.00,
      "pnl_pct": 6.0
    },
    "alternative_scenario": {
      "entry_date": "2024-03-10T00:00:00",
      "entry_price": 848.20,
      "pnl": 8030.00,
      "pnl_pct": 9.47
    },
    "comparison": {
      "pnl_difference": 2780.00,
      "pnl_difference_pct": 52.95,
      "better_scenario": "alternative",
      "improvement": 2780.00
    }
  }
}
```

#### Analyze Exit Timing

```http
POST /api/whatif/exit-timing
```

**Request Body:**
```json
{
  "user_id": "user123",
  "ticker": "META",
  "entry_date": "2024-02-01T00:00:00Z",
  "entry_price": 395.00,
  "base_exit_date": "2024-02-15T00:00:00Z",
  "alternative_exit_date": "2024-03-01T00:00:00Z",
  "position_size": 50
}
```

#### Analyze Position Size

```http
POST /api/whatif/position-size
```

**Request Body:**
```json
{
  "user_id": "user123",
  "ticker": "GOOGL",
  "entry_date": "2024-01-10T00:00:00Z",
  "entry_price": 142.50,
  "exit_date": "2024-02-10T00:00:00Z",
  "exit_price": 151.00,
  "base_position_size": 100,
  "alternative_position_size": 200
}
```

#### Analyze Stop Loss

```http
POST /api/whatif/stop-loss
```

**Request Body:**
```json
{
  "user_id": "user123",
  "ticker": "AAPL",
  "entry_date": "2024-03-01T00:00:00Z",
  "entry_price": 175.00,
  "exit_date": "2024-03-30T00:00:00Z",
  "base_stop_loss": 170.00,
  "alternative_stop_loss": 172.50,
  "position_size": 200
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "scenario_id": 4,
    "ticker": "AAPL",
    "base_scenario": {
      "stop_loss": 170.00,
      "stop_hit": false,
      "exit_price": 182.50,
      "pnl": 1500.00,
      "risk_amount": 1000.00
    },
    "alternative_scenario": {
      "stop_loss": 172.50,
      "stop_hit": true,
      "exit_price": 172.50,
      "pnl": -500.00,
      "risk_amount": 500.00
    },
    "comparison": {
      "pnl_difference": -2000.00,
      "risk_difference": -500.00,
      "better_scenario": "base",
      "recommendation": "Tighter stop (alternative) would have stopped out for a loss"
    }
  }
}
```

---

## Pattern Recognition Training

Educational quiz system to improve pattern identification skills.

### Features

- **Interactive quizzes** with real chart data
- **Multiple difficulty levels** (easy, medium, hard)
- **9 pattern types** to master
- **Time-based scoring** with speed bonuses
- **Performance tracking** and statistics
- **Leaderboards** for competition
- **Personalized recommendations**

### Available Patterns

1. VCP (Volatility Contraction Pattern)
2. Cup & Handle
3. Triangle (Ascending/Descending/Symmetrical)
4. Channel (Up/Down)
5. Wedge (Rising/Falling)
6. Head & Shoulders
7. Double Top
8. Double Bottom
9. SMA50 Pullback

### API Endpoints

#### Generate Quiz

```http
POST /api/training/quiz/generate
```

**Request Body:**
```json
{
  "ticker": "TSLA",
  "difficulty": "medium",
  "pattern_type": "VCP"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "quiz_id": 1,
    "ticker": "TSLA",
    "difficulty": "medium",
    "question": "What chart pattern is forming in TSLA?",
    "options": ["VCP", "Cup & Handle", "Triangle", "Channel", "Wedge"],
    "chart_data": {
      "timestamps": ["2024-01-01", "2024-01-02", ...],
      "open": [245.50, 247.00, ...],
      "high": [248.75, 249.50, ...],
      "low": [244.00, 246.25, ...],
      "close": [247.25, 248.50, ...],
      "volume": [85432100, 78965432, ...]
    },
    "bars_shown": 100
  }
}
```

#### Submit Answer

```http
POST /api/training/quiz/{quiz_id}/submit
```

**Request Body:**
```json
{
  "user_id": "user123",
  "answer": "VCP",
  "time_taken_seconds": 15
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "attempt_id": 1,
    "quiz_id": 1,
    "is_correct": true,
    "correct_answer": "VCP",
    "user_answer": "VCP",
    "score": 115.0,
    "time_taken_seconds": 15,
    "explanation": "Volatility Contraction Pattern (VCP) shows a series of contractions with declining volatility...",
    "feedback": "Excellent! You correctly identified the pattern."
  }
}
```

**Scoring System:**
- Base: 100 points for correct answer
- Time bonus:
  - < 10 seconds: +20 points
  - < 20 seconds: +15 points
  - < 30 seconds: +10 points
  - < 60 seconds: +5 points

#### Get User Statistics

```http
GET /api/training/stats/{user_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "user123",
    "total_attempts": 45,
    "correct_attempts": 32,
    "accuracy": 71.11,
    "average_score": 98.5,
    "average_time_seconds": 22.3,
    "pattern_stats": {
      "VCP": {"total": 8, "correct": 7, "accuracy": 87.5},
      "Cup & Handle": {"total": 6, "correct": 4, "accuracy": 66.67},
      ...
    },
    "difficulty_stats": {
      "easy": {"total": 15, "correct": 14},
      "medium": {"total": 20, "correct": 13},
      "hard": {"total": 10, "correct": 5}
    },
    "recent_accuracy": 80.0,
    "current_streak": 5,
    "best_streak": 9,
    "strengths": ["VCP", "Triangle", "SMA50 Pullback"],
    "weaknesses": ["Head & Shoulders", "Double Top"]
  }
}
```

#### Get Leaderboard

```http
GET /api/training/leaderboard?limit=10
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "user_id": "pro_trader",
      "average_score": 112.5,
      "total_attempts": 150,
      "accuracy": 92.0
    },
    {
      "user_id": "user123",
      "average_score": 98.5,
      "total_attempts": 45,
      "accuracy": 71.11
    },
    ...
  ]
}
```

#### Get Recommendations

```http
GET /api/training/recommendations/{user_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "recommendations": [
      "Practice identifying Head & Shoulders patterns",
      "Practice identifying Double Top patterns",
      "Try moving up to medium difficulty",
      "Focus on improving speed for higher scores"
    ]
  }
}
```

---

## Use Cases & Examples

### Educational Trading Journal

1. Create playback of a significant trade
2. Add annotations explaining decision points
3. Bookmark for future reference
4. Share with study group

### Strategy Testing

1. Create simulation account
2. Practice entering trades using historical playback
3. Track performance statistics
4. Use what-if analysis to refine entries/exits

### Pattern Recognition Mastery

1. Take daily pattern quizzes
2. Focus on weak areas from statistics
3. Compete on leaderboard
4. Achieve consistent 80%+ accuracy

### Trade Review & Learning

1. Replay past trades
2. Use what-if analysis to test alternatives
3. Document learnings with annotations
4. Build library of bookmarked examples

---

## Best Practices

### Historical Playback

- Start with paused playback to study initial conditions
- Use annotations liberally to document observations
- Step through critical periods bar-by-bar
- Bookmark exceptional examples for teaching

### Simulation Trading

- Treat simulation seriously like real money
- Follow your actual trading plan
- Review statistics weekly
- Use equity curve to identify performance trends

### What-If Analysis

- Run scenarios on both wins and losses
- Compare multiple alternatives per trade
- Document insights in scenario names
- Build a library of learning moments

### Pattern Training

- Start with easy difficulty to build confidence
- Take quizzes when fresh and focused
- Review explanations for wrong answers
- Practice weakest patterns more frequently

---

## Technical Details

### Database Schema

All features use PostgreSQL with the following tables:

- `historical_playbacks` - Playback sessions
- `playback_annotations` - User annotations
- `simulation_accounts` - Paper trading accounts
- `simulation_trades` - Simulated trades
- `what_if_scenarios` - Analysis scenarios
- `pattern_quizzes` - Quiz questions
- `quiz_attempts` - User attempts
- `replay_bookmarks` - Saved sessions
- `shared_replays` - Shareable links

### Data Sources

- Historical data from TwelveData, Finnhub, Yahoo Finance
- Cached in Redis for performance
- On-demand fetching for playback ranges

### Performance Considerations

- Playback data cached in memory during active sessions
- Maximum 5000 bars per playback session
- Share tokens expire based on user settings
- Quiz chart data stored in database for consistency

---

## Support & Troubleshooting

### Common Issues

**Playback not loading:**
- Check date range is valid
- Ensure ticker symbol is correct
- Verify market data availability

**Simulation trade rejected:**
- Check account has sufficient cash
- Verify ticker exists
- Ensure prices are reasonable

**Quiz generation fails:**
- Random ticker selection may occasionally fail
- Try specifying a specific ticker
- Check if pattern type is valid

### Rate Limits

- Playback creation: 10 per minute
- Trade entry: 20 per minute
- Quiz generation: 30 per minute
- General API: 60 requests per minute

---

## Future Enhancements

- [ ] Multi-timeframe playback
- [ ] Strategy backtesting framework
- [ ] Social features (follow traders, share portfolios)
- [ ] Advanced pattern training (drawing tools)
- [ ] Mobile app support
- [ ] Real-time paper trading
- [ ] Tournament mode for quizzes
- [ ] AI-powered trade suggestions

---

For more information, visit `/docs` for interactive API documentation.
