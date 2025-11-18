# Legend AI CLI

Professional trading pattern scanner and analysis command-line interface.

## Features

### 1. Core Commands

- **Analyze** - Analyze stocks and detect patterns
- **Scan** - Scan universes for trading opportunities
- **Watchlist** - Manage your stock watchlist
- **Chart** - Generate and view charts
- **Alerts** - Manage price and pattern alerts

### 2. Interactive TUI Mode

- Real-time market data dashboard
- Keyboard navigation
- Auto-refreshing data
- Beautiful terminal UI

### 3. Automation Features

- JSON/CSV/YAML output formats
- Batch processing
- Pipe-friendly output
- Scheduled scans (via cron)

### 4. Configuration Management

- Config file support (~/.legend/config.yaml)
- Environment variable overrides
- API key management
- User preferences

## Installation

### PyPI (Python Package)

```bash
pip install legend-ai

# With TUI support
pip install legend-ai[tui]

# With all features
pip install legend-ai[all]
```

### Homebrew (macOS/Linux)

```bash
# Add tap (first time only)
brew tap Stockmasterflex/legend-ai

# Install
brew install legend-ai

# Upgrade
brew upgrade legend-ai
```

### npm (Node.js wrapper)

```bash
# Global install
npm install -g legend-ai-cli

# Or use npx
npx legend-ai-cli --help
```

### Docker

```bash
# Pull image
docker pull legendai/cli:latest

# Run CLI
docker run -it --rm legendai/cli legend --help

# Run TUI
docker run -it --rm legendai/cli legend tui

# With config persistence
docker run -it --rm -v ~/.legend:/root/.legend legendai/cli legend analyze AAPL
```

## Quick Start

### 1. Initialize Configuration

```bash
legend config init
```

This creates `~/.legend/config.yaml` with default settings.

### 2. Configure API URL

```bash
# Point to local API
legend config set api_url http://localhost:8000

# Or point to remote API
legend config set api_url https://api.legend-ai.com
```

### 3. Verify Connection

```bash
legend health
```

### 4. Analyze a Stock

```bash
legend analyze AAPL
```

## Usage Examples

### Analysis

```bash
# Analyze a ticker
legend analyze AAPL

# Analyze with specific interval
legend analyze AAPL --interval weekly

# Pattern detection
legend analyze AAPL --pattern

# Batch analysis
legend analyze AAPL,MSFT,GOOGL --concurrent 5

# JSON output
legend analyze AAPL --output json

# Analyze and pipe to jq
legend analyze AAPL -o json | jq '.indicators'
```

### Scanning

```bash
# Quick scan
legend scan quick

# Full universe scan
legend scan universe --universe SP500

# Scan specific sector
legend scan sector Technology

# Scan with filters
legend scan universe \
  --sector tech \
  --min-price 50 \
  --max-price 500 \
  --min-volume 1000000

# Scan for specific patterns
legend scan universe --patterns VCP,CupAndHandle

# Output to CSV
legend scan universe -o csv > results.csv
```

### Watchlist Management

```bash
# Add ticker
legend watchlist add TSLA

# Add with notes and alert
legend watchlist add NVDA \
  --notes "Breakout setup" \
  --alert-price 500

# List watchlist
legend watchlist list

# List with status filter
legend watchlist list --status active

# Update status
legend watchlist update TSLA triggered

# Remove ticker
legend watchlist remove AAPL

# Clear watchlist
legend watchlist clear --force
```

### Charts

```bash
# Generate chart
legend chart show AAPL

# Weekly chart
legend chart show AAPL --interval weekly

# Don't open browser
legend chart show AAPL --no-open

# Batch charts
legend chart batch AAPL,MSFT,GOOGL
```

### Alerts

```bash
# List alerts
legend alerts list

# Create price alert
legend alerts create AAPL \
  --type price \
  --price 180 \
  --condition above

# Create pattern alert
legend alerts create NVDA \
  --type pattern \
  --condition VCP

# Delete alert
legend alerts delete 123
```

### Interactive TUI Mode

```bash
# Launch TUI
legend tui

# TUI with custom refresh
legend tui --refresh 10

# TUI with specific universe
legend tui --universe NASDAQ100
```

**Keyboard Shortcuts:**
- `r` - Refresh data
- `s` - Scan universe
- `a` - Analyze selected ticker
- `w` - Refresh watchlist
- `q` - Quit
- `?` - Help

### Configuration

```bash
# Show current config
legend config show

# Set configuration value
legend config set output_format json
legend config set color false
legend config set verbose true

# Reset to defaults
legend config reset

# Show config file path
legend config path
```

### Utilities

```bash
# Health check
legend health

# Quick analysis (shorthand)
legend quick AAPL

# Run diagnostics
legend doctor

# Show version
legend --version

# Show help
legend --help
legend analyze --help
```

## Automation Examples

### 1. Daily Scan Script

```bash
#!/bin/bash
# daily_scan.sh

RESULTS_DIR="$HOME/legend-results"
DATE=$(date +%Y-%m-%d)

mkdir -p "$RESULTS_DIR"

# Run scan and save results
legend scan universe \
  --universe SP500 \
  --patterns VCP,CupAndHandle \
  --output json > "$RESULTS_DIR/scan_$DATE.json"

echo "Scan complete: $RESULTS_DIR/scan_$DATE.json"
```

### 2. Watchlist Monitor (Cron)

```bash
# Add to crontab: crontab -e
# Run every hour during market hours (9 AM - 4 PM ET)
0 9-16 * * 1-5 legend scan universe --output csv >> ~/watchlist_updates.csv
```

### 3. Batch Analysis Pipeline

```bash
# Scan for setups, then analyze top matches
legend scan universe -o json | \
  jq -r '.matches[:10] | .[].ticker' | \
  xargs -I {} legend analyze {} --output json | \
  jq -s '.'
```

### 4. JSON Processing

```bash
# Get tickers with RSI < 30
legend scan universe -o json | \
  jq '.matches[] | select(.indicators.rsi < 30) | .ticker'

# Export to CSV for Excel
legend analyze AAPL,MSFT,GOOGL -o csv > analysis.csv
```

## Environment Variables

Override config with environment variables:

```bash
export LEGEND_API_URL=http://localhost:8000
export LEGEND_API_KEY=your_api_key
export LEGEND_OUTPUT_FORMAT=json

legend analyze AAPL
```

## Configuration File

Location: `~/.legend/config.yaml`

```yaml
# API Configuration
api_url: http://localhost:8000
api_key: null
timeout: 30

# Output Configuration
output_format: table  # table, json, csv, yaml
color: true
verbose: false

# TUI Configuration
tui_refresh_interval: 5
tui_theme: dark

# Cache Configuration
cache_enabled: true
cache_ttl: 300

# Watchlist Configuration
default_watchlist: default
```

## Output Formats

### Table (Default)

Rich formatted tables with colors and styling.

### JSON

```bash
legend analyze AAPL -o json
```

```json
{
  "ticker": "AAPL",
  "current_price": 175.50,
  "change_percent": 1.25,
  "indicators": {
    "sma_50": 170.25,
    "sma_200": 165.80,
    "rsi": 58.5
  },
  "patterns": [
    {
      "name": "VCP",
      "confidence": 0.85
    }
  ]
}
```

### CSV

```bash
legend scan universe -o csv
```

```csv
ticker,pattern_type,confidence,price,rs_rating
AAPL,VCP,0.85,175.50,95
MSFT,CupAndHandle,0.75,380.20,92
```

### YAML

```bash
legend analyze AAPL -o yaml
```

```yaml
ticker: AAPL
current_price: 175.50
change_percent: 1.25
indicators:
  sma_50: 170.25
  sma_200: 165.80
  rsi: 58.5
```

## API Requirements

The CLI requires a running Legend AI API server.

### Start API Locally

```bash
# From project root
uvicorn app.main:app --reload

# API runs at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Connect to Remote API

```bash
legend config set api_url https://api.legend-ai.com
```

## Troubleshooting

### Run Diagnostics

```bash
legend doctor
```

This checks:
- Python version
- Configuration
- API connectivity
- Dependencies

### Common Issues

**"Cannot reach API"**
```bash
# Check if API is running
curl http://localhost:8000/health

# Start API server
uvicorn app.main:app --reload
```

**"Configuration error"**
```bash
# Reset configuration
legend config reset

# Reinitialize
legend config init
```

**"TUI dependencies missing"**
```bash
pip install legend-ai[tui]
```

## Development

### Install from Source

```bash
git clone https://github.com/Stockmasterflex/legend-ai-python.git
cd legend-ai-python
pip install -e ".[all]"
```

### Run Tests

```bash
pytest tests/
pytest tests/test_cli.py -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file

## Support

- GitHub Issues: https://github.com/Stockmasterflex/legend-ai-python/issues
- Documentation: https://github.com/Stockmasterflex/legend-ai-python
- Email: contact@legend-ai.com

## Changelog

### v1.0.0 (2024)

- Initial release
- Core commands (analyze, scan, watchlist, chart, alerts)
- Interactive TUI mode
- Multiple output formats
- Configuration management
- PyPI, Homebrew, npm, Docker distribution
