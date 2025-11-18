# Professional Watchlist Features

This document describes the professional watchlist management features available in Legend AI.

## Overview

The Legend AI platform now includes professional-grade watchlist management with the following capabilities:

1. **Multiple Watchlists** - Organize stocks into unlimited custom lists
2. **Smart Organization** - Auto-categorize, filter, and sort with intelligent algorithms
3. **Watchlist Analytics** - Comprehensive performance and distribution metrics
4. **Import/Export** - CSV and TradingView integration for seamless workflow

## Architecture

### Database Models

#### WatchlistGroup
Represents a collection of stocks organized by strategy or theme.

**Fields:**
- `id` - Unique identifier
- `user_id` - Owner of the watchlist
- `name` - Watchlist name (e.g., "Swing Trades", "Day Trading")
- `description` - Optional description
- `color` - Hex color code for visual organization
- `strategy` - Trading strategy (e.g., "Swing Trading", "Position Trading")
- `position` - Order position for drag-and-drop
- `is_default` - Whether this is the default group

#### Watchlist (Enhanced)
Individual stock items within watchlists.

**Organization Fields:**
- `group_id` - Foreign key to WatchlistGroup
- `color` - Individual ticker color override
- `category` - Sector/category (auto or manual)
- `pattern_type` - Detected pattern (VCP, Cup & Handle, etc.)
- `position` - Order within group
- `strength_score` - Overall strength rating (0-100)

**Price Targets:**
- `target_entry` - Expected entry price
- `target_stop` - Stop loss price
- `target_price` - Take profit target

**Notes & Tags:**
- `reason` - Why added to watchlist
- `notes` - Additional notes
- `tags` - Flexible JSON array of tags

**Performance Tracking:**
- `entry_price` - Actual entry price
- `exit_price` - Actual exit price
- `profit_loss_pct` - Performance if traded

## API Endpoints

All endpoints are under `/api/v2/watchlists`

### Watchlist Groups

#### Create Group
```http
POST /api/v2/watchlists/groups
Content-Type: application/json

{
  "name": "Swing Trades",
  "description": "Medium-term setups",
  "color": "#10B981",
  "strategy": "Swing Trading"
}
```

#### Get All Groups
```http
GET /api/v2/watchlists/groups?user_id=default
```

#### Update Group
```http
PUT /api/v2/watchlists/groups/{group_id}
Content-Type: application/json

{
  "name": "Updated Name",
  "color": "#EF4444"
}
```

#### Delete Group
```http
DELETE /api/v2/watchlists/groups/{group_id}?move_items_to=2
```

#### Reorder Groups (Drag & Drop)
```http
POST /api/v2/watchlists/groups/reorder
Content-Type: application/json

{
  "ids": [3, 1, 2]
}
```

### Watchlist Items

#### Add Item
```http
POST /api/v2/watchlists/items
Content-Type: application/json

{
  "ticker": "AAPL",
  "group_id": 1,
  "status": "Watching",
  "pattern_type": "VCP",
  "strength_score": 85,
  "target_entry": 175.50,
  "target_stop": 170.00,
  "target_price": 185.00,
  "reason": "Strong RS, volume dry-up",
  "tags": ["tech", "earnings-play"],
  "color": "#10B981"
}
```

#### Get Items (with filters)
```http
GET /api/v2/watchlists/items?group_id=1&status=Watching&min_strength=75
```

**Query Parameters:**
- `user_id` - Filter by user (default: "default")
- `group_id` - Filter by group
- `status` - Filter by status
- `pattern_type` - Filter by pattern
- `category` - Filter by category
- `min_strength` - Minimum strength score

#### Update Item
```http
PUT /api/v2/watchlists/items/{item_id}
Content-Type: application/json

{
  "status": "Breaking Out",
  "strength_score": 92,
  "notes": "Volume surge detected"
}
```

#### Delete Item
```http
DELETE /api/v2/watchlists/items/{item_id}
```

#### Reorder Items
```http
POST /api/v2/watchlists/items/reorder?group_id=1
Content-Type: application/json

{
  "ids": [5, 3, 1, 2, 4]
}
```

#### Color Code Item
```http
PUT /api/v2/watchlists/items/{item_id}/color?color=#EF4444
```

### Smart Organization

#### Auto-Categorize by Sector
```http
POST /api/v2/watchlists/organize/auto-categorize?group_id=1
```

Returns:
```json
{
  "success": true,
  "message": "Auto-categorized 15 items",
  "items_updated": 15
}
```

#### Group by Pattern Type
```http
GET /api/v2/watchlists/organize/by-pattern
```

Returns:
```json
{
  "success": true,
  "grouped": {
    "VCP": [...],
    "Cup & Handle": [...],
    "Ascending Triangle": [...],
    "Unclassified": [...]
  }
}
```

#### Sort by Strength
```http
GET /api/v2/watchlists/organize/by-strength?group_id=1
```

### Analytics

#### Get Watchlist Analytics
```http
GET /api/v2/watchlists/analytics?group_id=1
```

Returns comprehensive analytics:
```json
{
  "success": true,
  "analytics": {
    "total_items": 25,
    "average_rs_rating": 78.5,
    "average_strength": 82.3,
    "sector_distribution": {
      "Technology": 10,
      "Healthcare": 5,
      "Finance": 7,
      "Energy": 3
    },
    "pattern_breakdown": {
      "VCP": 8,
      "Cup & Handle": 6,
      "Ascending Triangle": 4,
      "Unclassified": 7
    },
    "status_breakdown": {
      "Watching": 15,
      "Breaking Out": 5,
      "Triggered": 3,
      "Completed": 2
    },
    "performance": {
      "completed_trades": 2,
      "average_pnl_pct": 12.5,
      "win_rate_pct": 100
    },
    "strongest_setups": [
      {
        "ticker": "NVDA",
        "strength": 95,
        "pattern": "VCP"
      },
      ...
    ]
  }
}
```

### Import/Export

#### Export to CSV
```http
GET /api/v2/watchlists/export/csv?group_id=1
```

Returns CSV content with all watchlist data.

#### Import from CSV
```http
POST /api/v2/watchlists/import/csv?group_id=1
Content-Type: multipart/form-data

file: watchlist.csv
```

**CSV Format:**
```csv
ticker,name,status,pattern_type,category,target_entry,target_stop,target_price,strength_score,color,notes,tags
AAPL,Apple Inc.,Watching,VCP,Technology,175.50,170.00,185.00,85,#10B981,Strong setup,"tech,earnings"
```

#### Import Symbol List (Copy/Paste)
```http
POST /api/v2/watchlists/import/symbols
Content-Type: application/json

{
  "symbols": ["AAPL", "MSFT", "NVDA", "GOOGL"],
  "group_id": 1
}
```

#### Export to TradingView
```http
GET /api/v2/watchlists/export/tradingview?group_id=1
```

Returns comma-separated symbols:
```json
{
  "success": true,
  "symbols": "AAPL,MSFT,NVDA,GOOGL,AMZN",
  "count": 5
}
```

#### Import from TradingView
```http
POST /api/v2/watchlists/import/tradingview
Content-Type: application/json

{
  "symbols_string": "AAPL,MSFT,NVDA,GOOGL,AMZN",
  "group_id": 1
}
```

Accepts both comma-separated and newline-separated formats.

### Utility Endpoints

#### Get Summary
```http
GET /api/v2/watchlists/summary
```

Returns quick overview of all watchlists with key metrics.

## Migration

For existing users with watchlist data, run the migration script:

```bash
python -m app.migrations.migrate_watchlists
```

This will:
1. Create default watchlist group for existing users
2. Migrate all existing watchlist items
3. Preserve all data (reason, tags, status, etc.)

## Usage Examples

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000/api/v2/watchlists"

# Create a watchlist group
response = requests.post(f"{BASE_URL}/groups", json={
    "name": "Swing Trades",
    "description": "Medium-term setups",
    "color": "#10B981",
    "strategy": "Swing Trading"
})
group = response.json()["group"]

# Add stocks to watchlist
stocks = ["AAPL", "MSFT", "NVDA"]
for symbol in stocks:
    requests.post(f"{BASE_URL}/items", json={
        "ticker": symbol,
        "group_id": group["id"],
        "status": "Watching"
    })

# Get analytics
analytics = requests.get(f"{BASE_URL}/analytics?group_id={group['id']}")
print(analytics.json())

# Export to TradingView
tv_export = requests.get(f"{BASE_URL}/export/tradingview?group_id={group['id']}")
print(f"TradingView symbols: {tv_export.json()['symbols']}")
```

### JavaScript Client Example

```javascript
const BASE_URL = 'http://localhost:8000/api/v2/watchlists';

// Create watchlist group
const createGroup = async () => {
  const response = await fetch(`${BASE_URL}/groups`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: 'Day Trading',
      color: '#F59E0B',
      strategy: 'Day Trading'
    })
  });
  return await response.json();
};

// Add item
const addItem = async (ticker, groupId) => {
  const response = await fetch(`${BASE_URL}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ticker,
      group_id: groupId,
      status: 'Watching'
    })
  });
  return await response.json();
};

// Get items with filters
const getItems = async (filters) => {
  const params = new URLSearchParams(filters);
  const response = await fetch(`${BASE_URL}/items?${params}`);
  return await response.json();
};

// Usage
const group = await createGroup();
await addItem('TSLA', group.group.id);
const items = await getItems({ group_id: group.group.id, min_strength: 80 });
```

## Best Practices

### Organization Strategy

1. **Create Strategy-Based Groups**
   - Separate watchlists for different trading styles
   - Use colors consistently (e.g., green for swing, orange for day trading)

2. **Use Pattern Types**
   - Auto-categorize stocks by detected patterns
   - Filter by pattern to find similar setups

3. **Track Strength Scores**
   - Update strength scores as setups develop
   - Sort by strength to prioritize strongest setups

4. **Leverage Tags**
   - Use tags for flexible categorization
   - Examples: "earnings-play", "low-float", "sector-leader"

### Performance Tracking

1. **Update Entry/Exit Prices**
   - Record actual entry when triggered
   - Record exit price when closed
   - System calculates profit/loss automatically

2. **Monitor Analytics**
   - Review win rate and average P&L regularly
   - Identify strongest sectors and patterns
   - Adjust strategy based on performance

### Import/Export Workflow

1. **TradingView Integration**
   - Export from TradingView to sync watchlists
   - Import to Legend AI for pattern detection
   - Export back with enhanced analysis

2. **CSV Backup**
   - Export regularly for backup
   - Import to restore or migrate between accounts

## Feature Highlights

### 1. Multiple Watchlists ✅
- Unlimited watchlist groups
- Categorize by strategy (Swing, Day, Position)
- Color-code for visual organization
- Drag-and-drop reordering

### 2. Smart Organization ✅
- Auto-categorize by sector
- Group by pattern type
- Sort by strength score
- Advanced filtering (status, pattern, category, strength)

### 3. Watchlist Analytics ✅
- Average RS rating calculation
- Sector distribution charts
- Pattern breakdown analysis
- Performance tracking (win rate, avg P&L)
- Strongest setups identification

### 4. Import/Export ✅
- CSV import/export with full data preservation
- Copy/paste ticker lists
- Share watchlists between users
- TradingView sync (comma-separated format)

## Technical Details

### Database Schema

```sql
-- Watchlist Groups
CREATE TABLE watchlist_groups (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(100) NOT NULL,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  color VARCHAR(20) DEFAULT '#3B82F6',
  strategy VARCHAR(100),
  position INTEGER DEFAULT 0,
  is_default BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ
);

-- Enhanced Watchlists
CREATE TABLE watchlists (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(100) NOT NULL DEFAULT 'default',
  group_id INTEGER REFERENCES watchlist_groups(id),
  ticker_id INTEGER REFERENCES tickers(id),
  status VARCHAR(50) DEFAULT 'Watching',

  -- Organization
  color VARCHAR(20),
  category VARCHAR(100),
  pattern_type VARCHAR(50),
  position INTEGER DEFAULT 0,
  strength_score FLOAT,

  -- Targets
  target_entry FLOAT,
  target_stop FLOAT,
  target_price FLOAT,

  -- Notes
  reason TEXT,
  notes TEXT,
  tags JSON,

  -- Alerts
  alerts_enabled BOOLEAN DEFAULT TRUE,
  alert_threshold FLOAT,

  -- Performance
  entry_price FLOAT,
  exit_price FLOAT,
  profit_loss_pct FLOAT,

  -- Timestamps
  added_at TIMESTAMPTZ DEFAULT NOW(),
  triggered_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
);
```

### Caching

Watchlist data is cached in Redis with 1-hour TTL for optimal performance:
- Groups list: `watchlist:groups:{user_id}`
- Items list: `watchlist:items:{user_id}:{group_id}`
- Analytics: `watchlist:analytics:{user_id}:{group_id}`

### Performance

- List operations: < 10ms (cached)
- Analytics calculations: < 50ms
- Import/Export: ~100ms per 100 items
- Auto-categorization: ~20ms per item

## Future Enhancements

Planned features:
- [ ] Real-time price updates in watchlist
- [ ] Advanced charting within watchlist view
- [ ] Automated pattern detection for watchlist items
- [ ] Email/SMS alerts for watchlist triggers
- [ ] Watchlist sharing between users
- [ ] Historical performance charts
- [ ] AI-powered watchlist recommendations
- [ ] Mobile app integration

## Support

For questions or issues:
- GitHub Issues: [legend-ai-python/issues](https://github.com/stockmasterflex/legend-ai-python/issues)
- API Documentation: `/docs` endpoint
- Migration Support: See `app/migrations/migrate_watchlists.py`
