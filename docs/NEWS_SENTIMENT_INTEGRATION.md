# News Sentiment Integration

## Overview

The Legend AI platform now includes comprehensive real-time news sentiment analysis capabilities. This integration provides multi-source news aggregation, AI-powered sentiment scoring, trend detection, and market impact analysis.

## Features

### 1. News Aggregation

- **Multiple News Sources**: Aggregates news from:
  - Alpha Vantage (with built-in sentiment)
  - Finnhub
  - NewsAPI
  - Benzinga (premium)

- **Real-time Updates**: Continuous news fetching with configurable refresh intervals
- **Ticker-specific Filtering**: Automatically filters news by stock ticker
- **Breaking News Detection**: Identifies and highlights urgent/breaking news based on keywords

### 2. Sentiment Scoring

- **AI-Powered Analysis**: Uses multiple sentiment analyzers:
  - **VADER**: Fast, lexicon-based, great for social media and news
  - **FinBERT**: Transformer model specialized for financial text
  - **OpenAI**: GPT-based analysis (optional, more expensive but very accurate)

- **Sentiment Metrics**:
  - Overall score (-1 to 1)
  - Positive/negative/neutral probabilities
  - Confidence level
  - Sentiment label classification

- **Historical Trends**: Track sentiment changes over time
- **Shift Detection**: Automatically detects significant sentiment changes

### 3. News Impact Analysis

- **Price Correlation**: Analyzes correlation between sentiment and price movements
- **Volume Analysis**: Tracks news frequency vs trading volume
- **Pattern Invalidation Warnings**: Alerts when negative sentiment may invalidate technical patterns
- **Opportunity Detection**: Identifies potential trading opportunities based on sentiment:
  - Bullish sentiment shifts
  - Contrarian setups
  - Breaking news catalysts
  - Sentiment confirmation with technical analysis

### 4. Dashboard Integration

- **News Feed Widget**: Integrated dashboard view with:
  - Real-time sentiment indicators
  - Quick-read summaries
  - Color-coded sentiment labels
  - Breaking news badges
  - Source attribution

- **Sentiment Summary Card**:
  - Overall sentiment score
  - Positive/negative/neutral counts
  - Trend indicators
  - Sentiment shift alerts

- **Auto-refresh**: Configurable auto-refresh (default: 5 minutes)

## API Endpoints

### Get News Articles

```bash
GET /api/sentiment/news/{symbol}?limit=50
```

Returns aggregated news from all available sources.

### Get News with Sentiment

```bash
GET /api/sentiment/news/{symbol}/with-sentiment?limit=50&analyzer=vader
```

Returns news articles with AI-powered sentiment analysis attached.

**Parameters**:
- `symbol`: Stock ticker (e.g., AAPL)
- `limit`: Number of articles (1-100)
- `analyzer`: Sentiment analyzer (vader, finbert, openai)

### Get Sentiment Score & Trend

```bash
GET /api/sentiment/score/{symbol}?hours_back=24
```

Returns current sentiment score and trend analysis.

**Response**:
```json
{
  "symbol": "AAPL",
  "current_sentiment": 0.45,
  "sentiment_label": "positive",
  "article_count": 42,
  "trend": "improving",
  "shift_detected": true,
  "shift_magnitude": 0.35,
  "positive_count": 28,
  "negative_count": 8,
  "neutral_count": 6,
  "breaking_news_count": 2
}
```

### Get Breaking News

```bash
GET /api/sentiment/breaking/{symbol}?hours_back=2
```

Returns only breaking/urgent news for the symbol.

### Analyze News Impact

```bash
GET /api/sentiment/impact/{symbol}?hours_back=24
```

Returns detailed impact analysis including:
- News impact scores
- Pattern invalidation warnings
- Opportunity alerts
- Top impact news articles

**Response**:
```json
{
  "symbol": "AAPL",
  "current_price": 185.50,
  "sentiment_trend": {...},
  "impact_analysis": {
    "total_articles_analyzed": 45,
    "total_impact_score": 12.5,
    "average_impact_score": 0.28,
    "has_high_impact": false
  },
  "pattern_invalidation_warning": {
    "risk_detected": false,
    "reason": null,
    "recommendation": null
  },
  "opportunity_alerts": [
    {
      "type": "sentiment_confirmation",
      "signal": "Strong positive sentiment consensus",
      "action": "Look for technical confirmation",
      "confidence": "medium"
    }
  ]
}
```

### Get News Feed (Dashboard Widget)

```bash
GET /api/sentiment/feed/{symbol}?limit=20
```

Returns formatted feed optimized for dashboard display with sentiment indicators.

### Analyze Arbitrary Text

```bash
POST /api/sentiment/analyze
Content-Type: application/json

{
  "text": "Your text to analyze",
  "analyzer": "vader"
}
```

Analyze sentiment of any text (useful for testing).

### API Usage Statistics

```bash
GET /api/sentiment/usage
```

Returns API usage statistics for all news sources.

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# News API Keys
NEWSAPI_API_KEY=your_newsapi_key
BENZINGA_API_KEY=your_benzinga_key

# Alpha Vantage and Finnhub keys (reused from existing config)
ALPHA_VANTAGE_API_KEY=your_key
FINNHUB_API_KEY=your_key

# Sentiment Analysis Settings
SENTIMENT_ANALYZER=vader  # vader, finbert, or openai
SENTIMENT_THRESHOLD_POSITIVE=0.05
SENTIMENT_THRESHOLD_NEGATIVE=-0.05
SENTIMENT_SHIFT_THRESHOLD=0.3
NEWS_LOOKBACK_HOURS=24
BREAKING_NEWS_KEYWORDS=breaking,alert,urgent,emergency,halt

# Cache TTL
CACHE_TTL_NEWS=3600  # 1 hour
CACHE_TTL_SENTIMENT=900  # 15 minutes

# Rate Limits
NEWSAPI_DAILY_LIMIT=100
BENZINGA_DAILY_LIMIT=200
```

### Sentiment Analyzer Options

1. **VADER** (Default)
   - Fast and lightweight
   - No additional setup required
   - Great for news headlines and social media
   - Best for real-time applications

2. **FinBERT**
   - Specialized for financial text
   - More accurate than VADER for financial news
   - Requires transformers and torch (automatically installed)
   - Slower but more accurate

3. **OpenAI**
   - Most accurate
   - Requires OpenAI API key
   - More expensive
   - Best for high-value analysis

## Database Schema

### News Articles Table

```sql
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    ticker_id INTEGER REFERENCES tickers(id),
    symbol VARCHAR(10) NOT NULL,
    title TEXT NOT NULL,
    summary TEXT,
    url TEXT,
    source VARCHAR(100),
    author VARCHAR(255),
    published_at TIMESTAMP WITH TIME ZONE,
    category VARCHAR(50),
    tags JSONB,
    image_url TEXT,
    is_breaking BOOLEAN DEFAULT FALSE,
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Sentiment Scores Table

```sql
CREATE TABLE sentiment_scores (
    id SERIAL PRIMARY KEY,
    ticker_id INTEGER REFERENCES tickers(id),
    symbol VARCHAR(10) NOT NULL,
    news_article_id INTEGER REFERENCES news_articles(id),
    score FLOAT NOT NULL,
    positive FLOAT DEFAULT 0.0,
    negative FLOAT DEFAULT 0.0,
    neutral FLOAT DEFAULT 0.0,
    analyzer VARCHAR(50),
    confidence FLOAT,
    sentiment_label VARCHAR(20),
    price_change_1h FLOAT,
    price_change_24h FLOAT,
    volume_change FLOAT,
    is_shift BOOLEAN DEFAULT FALSE,
    shift_magnitude FLOAT,
    previous_sentiment FLOAT,
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## Migration

Run the SQL migration to create the new tables:

```bash
psql $DATABASE_URL < migrations/001_add_sentiment_tables.sql
```

Or use Alembic (if configured):

```bash
alembic upgrade head
```

## Dependencies

The following Python packages are required (automatically installed from requirements.txt):

- `vaderSentiment==3.3.2` - VADER sentiment analyzer
- `transformers==4.46.3` - For FinBERT model
- `torch==2.5.1` - PyTorch for transformers
- `sentencepiece==0.2.0` - Tokenization
- `feedparser==6.0.11` - RSS feed parsing
- `beautifulsoup4==4.12.3` - HTML parsing

## Usage Examples

### Python Service

```python
from app.services.sentiment_service import get_sentiment_service

# Get sentiment service
sentiment_service = get_sentiment_service()

# Fetch news with sentiment
news = await sentiment_service.get_news_with_sentiment("AAPL", limit=50)

# Get sentiment trend
trend = await sentiment_service.get_sentiment_trend("AAPL", hours_back=24)

# Analyze news impact
impact = await sentiment_service.analyze_news_impact("AAPL")

# Get breaking news
breaking = await sentiment_service.get_breaking_news("AAPL")
```

### JavaScript Dashboard

The sentiment widget is automatically loaded on the dashboard:

```javascript
// Widget is auto-initialized
// It listens for symbol changes and updates automatically

// Manual refresh
sentimentWidget.loadSentiment('AAPL', true);

// Update symbol
sentimentWidget.updateSymbol('TSLA');
```

## Performance & Caching

- **Multi-tier caching**: Redis (hot), Database (warm), CDN (cold)
- **Cache TTL**:
  - News articles: 1 hour
  - Sentiment scores: 15 minutes
  - Sentiment trends: 5 minutes
- **Rate limiting**: Respects API limits for all sources
- **Deduplication**: Automatically deduplicates articles from multiple sources
- **Background refresh**: Optional auto-refresh for real-time updates

## Alerts & Warnings

### Pattern Invalidation Warnings

The system automatically detects when negative sentiment may invalidate technical patterns:

- Significant negative sentiment shift (< -0.3)
- Breaking news with negative sentiment
- Recommendation: "Monitor price action closely and consider tightening stops"

### Opportunity Alerts

The system detects potential trading opportunities:

1. **Bullish Sentiment Shift**: Strong positive sentiment shift detected
2. **Contrarian Setup**: Negative sentiment but price holding
3. **Breaking News Catalyst**: Breaking news with positive sentiment
4. **Sentiment Confirmation**: Positive sentiment aligning with technical setup

## Troubleshooting

### No News Appearing

1. Check API keys are configured:
   ```bash
   echo $ALPHA_VANTAGE_API_KEY
   echo $NEWSAPI_API_KEY
   ```

2. Check API usage:
   ```bash
   curl http://localhost:8000/api/sentiment/usage
   ```

3. Check logs:
   ```bash
   tail -f logs/app.log | grep sentiment
   ```

### Sentiment Analysis Errors

1. Ensure dependencies are installed:
   ```bash
   pip install vaderSentiment transformers torch
   ```

2. Check analyzer configuration:
   ```bash
   echo $SENTIMENT_ANALYZER
   ```

3. Test with simple text:
   ```bash
   curl -X POST http://localhost:8000/api/sentiment/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "This is great news!", "analyzer": "vader"}'
   ```

### Dashboard Widget Not Loading

1. Check browser console for errors
2. Verify JavaScript files are loaded:
   - `/static/js/sentiment-widget.js`
3. Check CSS is loaded:
   - `/static/css/sentiment-widget.css`
4. Clear browser cache and reload

## Future Enhancements

Potential improvements for future releases:

1. **Social Media Integration**: Twitter/X sentiment analysis
2. **Insider Trading Correlation**: Correlate sentiment with insider activity
3. **Earnings Call Sentiment**: Analyze earnings call transcripts
4. **Sector Sentiment**: Aggregate sentiment across sectors
5. **Predictive Models**: ML models to predict price impact from sentiment
6. **Mobile App**: Native mobile sentiment dashboard
7. **Custom Alerts**: User-configurable sentiment alerts
8. **Sentiment Backtesting**: Historical sentiment analysis for strategy testing

## Support

For issues or questions:
- GitHub Issues: [github.com/your-repo/issues](https://github.com/your-repo/issues)
- Documentation: [docs.legendai.com](https://docs.legendai.com)
- API Reference: [api.legendai.com/docs](http://localhost:8000/docs)

---

**Built with ❤️ by the Legend AI team**
