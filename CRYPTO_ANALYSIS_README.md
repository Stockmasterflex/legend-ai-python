# Crypto Trading Analysis

Comprehensive cryptocurrency analysis features for Legend AI trading platform.

## Features

### 1. Crypto Data Sources

Multi-source data integration with automatic fallback:

- **Binance API** - Real-time pricing, futures data, funding rates, open interest
- **Coinbase API** - Spot prices and exchange rates
- **CoinGecko** - Market data, rankings, DeFi metrics for 10,000+ coins

**Endpoints:**
```bash
GET /crypto/price/{symbol}?quote_currency=USDT
GET /crypto/ticker/{symbol}
GET /crypto/market/overview
```

### 2. Crypto-Specific Patterns

Advanced pattern detection for crypto markets:

#### Whale Movements
- Detects large transactions (>$1M USD equivalent)
- Unusual volume spikes (>3 standard deviations)
- Sentiment analysis (accumulation vs distribution)

#### Exchange Flow Analysis
- Track inflow/outflow patterns
- Net flow calculations
- Bullish/bearish signals based on flow direction

#### Funding Rates
- Monitor perpetual futures funding rates
- Detect extreme funding (potential reversals)
- Annualized rate calculations with risk assessment

#### Open Interest
- Track futures open interest changes
- Identify liquidation cascade risks
- Trend classification (strong uptrend, downtrend, covering, liquidation)

**Endpoints:**
```bash
GET /crypto/patterns/{symbol}?lookback_hours=24
GET /crypto/whale/{symbol}
GET /crypto/funding/{symbol}
```

### 3. DeFi Analytics

Comprehensive DeFi analysis and optimization:

#### Liquidity Pool Analysis
- TVL (Total Value Locked) tracking
- Volume/TVL ratios
- APY/APR calculations
- Impermanent loss risk assessment

#### Yield Farming Optimizer
- Find top yield opportunities
- Risk-adjusted return calculations
- Filter by TVL, APY, IL risk, and chain
- Auto-compounding analysis

#### Gas Price Optimization
- Real-time Ethereum gas prices
- Optimal timing recommendations
- Transaction cost estimation
- Multi-chain support

#### Smart Contract Analysis
- Contract verification status
- Risk scoring
- Audit report integration (placeholder for production)

**Endpoints:**
```bash
GET /crypto/defi/yields?min_tvl=1000000&min_apy=5&max_il_risk=moderate
GET /crypto/defi/gas?chain=ethereum
GET /crypto/defi/analytics
```

### 4. Cross-Asset Correlation

Understand how crypto moves relative to traditional markets:

#### BTC vs SPY Correlation
- Track Bitcoin correlation with S&P 500
- 7-day, 30-day, and 90-day correlations
- Trend analysis (increasing/decreasing)
- Market regime classification (risk-on/risk-off/decoupled)

#### Bitcoin Dominance
- Track BTC market cap dominance
- Identify altcoin season vs BTC-led markets
- Flight to quality signals

#### Risk-On/Risk-Off Indicators
- Detect market sentiment shifts
- Multi-indicator scoring
- Trading recommendations

#### Flight to Safety Detection
- Monitor safe haven flows
- Gold, bonds, and dollar strength tracking
- Severity and duration estimates

**Endpoints:**
```bash
GET /crypto/correlation
GET /crypto/correlation/btc-spy?lookback_days=90
GET /crypto/dominance
GET /crypto/market/regime
```

### 5. Crypto Alerts

Comprehensive alert system for crypto traders:

#### Price Alerts
- Threshold-based alerts (above/below)
- Configurable per symbol
- 1-hour cooldown to avoid spam

#### Whale Alerts
- Large transaction notifications
- Volume spike detection
- Sentiment analysis

#### Exchange Flow Alerts
- Significant inflow/outflow alerts (>$10M)
- Bullish/bearish signals

#### Network Congestion
- High gas fee warnings
- Optimal transaction timing

#### Funding Rate Extremes
- Alert on extreme funding rates
- Reversal risk notifications

#### Open Interest Spikes
- High liquidation risk warnings
- Volatility expectations

#### Bitcoin Dominance Shifts
- Market regime change alerts
- Alt season vs BTC dominance

**Endpoints:**
```bash
POST /crypto/alerts/monitor
{
  "price_watchlist": [
    {
      "symbol": "BTCUSDT",
      "alert_above": 50000,
      "alert_below": 40000
    }
  ],
  "symbols": ["BTCUSDT", "ETHUSDT"]
}
```

## Installation

### Requirements

All dependencies are included in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Configuration

No API keys required for public data endpoints!

Optional configuration in `.env`:

```env
# Optional: For enhanced features
BINANCE_API_KEY=your_key
BINANCE_SECRET_KEY=your_secret
```

## Usage Examples

### Get Real-Time Bitcoin Price

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get("http://localhost:8000/crypto/price/BTC")
    data = response.json()
    print(f"BTC Price: ${data['price']:,.2f}")
```

### Analyze Crypto Patterns

```python
response = await client.get("http://localhost:8000/crypto/patterns/BTCUSDT?lookback_hours=24")
analysis = response.json()

print(f"Overall Signal: {analysis['overall_signal']}")
print(f"Confidence: {analysis['confidence']:.0%}")
print(f"Risk Level: {analysis['risk_level']}")

for rec in analysis['recommendations']:
    print(f"  - {rec}")
```

### Find Top DeFi Yields

```python
response = await client.get(
    "http://localhost:8000/crypto/defi/yields"
    "?min_tvl=1000000"
    "&min_apy=10"
    "&max_il_risk=moderate"
)
yields = response.json()

for pool in yields['yields'][:5]:
    print(f"{pool['protocol']} - {pool['pool']}")
    print(f"  APY: {pool['apy']:.2f}% (Adjusted: {pool['apy_adjusted']:.2f}%)")
    print(f"  TVL: ${pool['tvl']:,.0f}")
    print(f"  IL Risk: {pool['il_risk']}")
```

### Check Market Correlation

```python
response = await client.get("http://localhost:8000/crypto/correlation")
correlation = response.json()

print(f"Overall Assessment: {correlation['overall_assessment']}")
print("\nTrading Implications:")
for implication in correlation['trading_implications']:
    print(f"  - {implication}")

btc_spy = correlation['btc_spy_correlation']
print(f"\nBTC-SPY Correlation: {btc_spy['correlation']:.2f}")
print(f"Regime: {btc_spy['regime']}")
print(f"Interpretation: {btc_spy['interpretation']}")
```

### Monitor Crypto Alerts

```python
response = await client.post(
    "http://localhost:8000/crypto/alerts/monitor",
    json={
        "price_watchlist": [
            {
                "symbol": "BTCUSDT",
                "alert_above": 50000,
                "alert_below": 40000
            }
        ],
        "symbols": ["BTCUSDT", "ETHUSDT"]
    }
)
alerts = response.json()

print(f"Total Alerts: {alerts['total_alerts']}")
print(f"Whale Alerts: {len(alerts['whale_alerts'])}")
print(f"Funding Alerts: {len(alerts['funding_alerts'])}")
```

## Architecture

### Service Layer

- `app/services/crypto_data.py` - Data source integrations
- `app/services/crypto_patterns.py` - Pattern detection
- `app/services/defi_analytics.py` - DeFi analysis
- `app/services/correlation_analysis.py` - Cross-asset correlation
- `app/services/crypto_alerts.py` - Alert system

### API Layer

- `app/api/crypto.py` - FastAPI endpoints

### Data Flow

```
Client Request
    ↓
FastAPI Endpoint (app/api/crypto.py)
    ↓
Service Layer (app/services/crypto_*.py)
    ↓
Data Sources (Binance, CoinGecko, Coinbase)
    ↓
Response with Analysis
```

## Rate Limits

### Binance
- Public endpoints: 1200 requests/minute
- No API key required for public data

### CoinGecko
- Free tier: ~30 requests/minute
- No API key required

### Coinbase
- Public endpoints: No rate limit
- No API key required

All services include automatic rate limiting and retry logic.

## Testing

Run crypto analysis tests:

```bash
pytest tests/test_crypto_analysis.py -v
```

Test coverage includes:
- Data source integrations
- Pattern detection algorithms
- Correlation calculations
- DeFi analytics
- Alert system
- API endpoints

## Error Handling

All services include comprehensive error handling:

- Automatic fallback to secondary data sources
- Rate limit management with cooldowns
- Network error retry logic
- Graceful degradation when services are unavailable

## Performance

- **Parallel Analysis**: All analyses run concurrently using asyncio
- **Caching**: Redis caching for frequently accessed data
- **Rate Limiting**: Built-in rate limiting to respect API limits
- **Multi-Source**: Automatic fallback ensures high availability

## Roadmap

### Future Enhancements

1. **Historical Analysis**
   - Backtest correlation patterns
   - Historical funding rate analysis
   - Pattern success rates

2. **Advanced DeFi**
   - Liquidity pool comparison
   - Yield optimization strategies
   - Smart contract security scoring

3. **Machine Learning**
   - Whale movement prediction
   - Funding rate forecasting
   - Correlation regime prediction

4. **Additional Integrations**
   - DEX aggregators (1inch, Paraswap)
   - On-chain analytics (Dune, Nansen)
   - News sentiment analysis

## Support

For issues or questions:
1. Check API documentation at `/docs`
2. Review example usage above
3. Check service logs for debugging

## License

Part of Legend AI Trading Platform - Professional-grade trading analysis tools.
