# Legend AI CLI

Professional command-line interface for the Legend AI Trading Pattern Scanner API.

## Installation

```bash
pip install legend-cli
```

Or install from source:

```bash
cd cli
pip install -e .
```

## Usage

### Detect Patterns

```bash
# Basic pattern detection
legend-cli detect AAPL

# With custom interval
legend-cli detect NVDA --interval 1week

# Weekly timeframe
legend-cli detect TSLA --interval 1week
```

### Scan Universe

```bash
# Scan S&P 500
legend-cli scan

# Scan with custom parameters
legend-cli scan --universe SP500 --min-score 8.0 --max-results 10

# Scan NASDAQ 100
legend-cli scan --universe NASDAQ100 --min-score 7.5
```

### Chat with AI

```bash
# General question
legend-cli chat "What are the best tech stocks right now?"

# Stock-specific question
legend-cli chat "Should I buy now?" --symbol AAPL

# Pattern explanation
legend-cli chat "What is a VCP pattern?"
```

### Watchlist Management

```bash
# List watchlist
legend-cli watchlist list

# Add to watchlist
legend-cli watchlist add NVDA --reason "VCP forming"

# Add with entry/stop
legend-cli watchlist add AAPL --reason "Cup and Handle"
```

### Health Check

```bash
# Check API health
legend-cli health
```

### Custom API URL

```bash
# Use local API
legend-cli detect AAPL --url http://localhost:8000

# Use custom endpoint
legend-cli scan --url https://my-api.com
```

## Examples

### Example Output: Pattern Detection

```
╭─ Pattern for AAPL ─────────────────────────╮
│ VCP (Volatility Contraction Pattern)      │
│                                            │
│ Score: 8.5/10                             │
│ Entry: $175.50                            │
│ Stop: $170.25                             │
│ Target: $185.00                           │
│ Risk/Reward: 2.5R                         │
│ RS Rating: 85                             │
│                                            │
│ Cached: False | Processing Time: 1.23s    │
╰────────────────────────────────────────────╯
Chart: https://example.com/chart.png
```

### Example Output: Universe Scan

```
                  Top Setups from SP500
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━┓
┃ Ticker ┃ Pattern                ┃ Score ┃   Entry ┃  Target ┃  R:R ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━┩
│ NVDA   │ VCP                    │   9.2 │ $450.00 │ $475.00 │ 3.2R │
│ AAPL   │ Cup and Handle         │   8.8 │ $175.50 │ $185.00 │ 2.5R │
│ MSFT   │ Ascending Triangle     │   8.5 │ $385.00 │ $395.00 │ 2.8R │
│ TSLA   │ Flat Base              │   8.2 │ $245.00 │ $260.00 │ 2.1R │
└────────┴────────────────────────┴───────┴─────────┴─────────┴──────┘

Found 42 patterns from 500 stocks
```

## Features

- 🎯 **Pattern Detection**: Detect patterns with beautiful CLI output
- 🔍 **Universe Scanning**: Scan markets with table visualization
- 🤖 **AI Chat**: Interactive AI assistant
- 📊 **Watchlist**: Manage your watchlist from terminal
- 🎨 **Rich Output**: Beautiful terminal UI with colors and tables
- ⚡ **Fast**: Optimized for speed with caching support

## Requirements

- Python 3.8+
- httpx
- rich

## License

MIT
