# NLP-Based Stock Search System

## Overview

The NLP Search system provides natural language query parsing for stock pattern searches, allowing users to search using plain English instead of complex filter syntax.

## Features

### 1. 🧠 NLP Query Parser

Parse natural language queries and extract structured information:

- **Intent Classification**: Automatically determine what the user wants to do (scan, analyze, compare, etc.)
- **Entity Extraction**: Extract tickers, patterns, price levels, sectors, and timeframes
- **Confidence Scoring**: Measure how confident the parser is in understanding the query
- **Fuzzy Matching**: Handle typos and variations in pattern names

**Example Queries:**
```
"Find VCP patterns in tech stocks"
"Show me breakouts above $100"
"Which stocks are pulling back to 21 EMA?"
"Compare AAPL and MSFT patterns"
"Analyze NVDA on the daily chart"
"Tech stocks breaking out today"
```

### 2. 🎯 Intelligent Filters

Automatically extract and apply filters:

- **Ticker Symbols**: Recognizes $AAPL, AAPL, or "Apple"
- **Pattern Names**: VCP, Cup & Handle, Head & Shoulders, etc.
- **Price Levels**: "above $100", "between $20 and $30", "under 50"
- **Sectors**: Technology, Healthcare, Financial, etc.
- **Timeframes**: Daily, weekly, monthly, intraday

### 3. 🤖 Contextual Understanding

Smart features that learn from usage:

- **Search History**: Track all queries with analytics
- **Query Suggestions**: Personalized based on user's past searches
- **Popular Queries**: Discover trending searches across all users
- **Auto-complete**: Real-time suggestions as you type
- **Typo Correction**: Automatically fix common misspellings

### 4. 🎤 Voice Search

Hands-free operation with voice-to-text:

- **Multi-language Support**: English, Spanish, French, German, and more
- **Audio Enhancement**: Automatic noise reduction and normalization
- **Multiple Formats**: WAV, MP3, OGG, FLAC, M4A, WEBM
- **High Accuracy**: Uses Google Speech Recognition
- **Accent Handling**: Works with various accents and dialects

### 5. 📚 Search History & Templates

Powerful search management:

- **Save Searches**: Save frequently used queries as templates
- **Quick Re-run**: Execute saved searches with one click
- **Share Templates**: Share search templates with other users
- **Search Analytics**: Track your search patterns and preferences
- **Tagged Organization**: Organize templates with custom tags

## API Endpoints

### Search with Natural Language

**POST** `/api/nlp/search`

Parse and execute a natural language query.

```json
{
  "query": "Find VCP patterns in tech stocks above $100",
  "user_id": "user123",
  "execute_search": true,
  "save_history": true
}
```

**Response:**
```json
{
  "original_query": "Find VCP patterns in tech stocks above $100",
  "intent": "scan",
  "confidence": 0.95,
  "tickers": [],
  "patterns": ["vcp"],
  "sectors": ["technology"],
  "price_filters": {
    "min_price": 100.0
  },
  "timeframe": "daily",
  "comparison": false,
  "suggestions": [
    "Show VCP patterns in top stocks",
    "Find breakouts in technology sector"
  ],
  "results": [...],
  "results_count": 15,
  "execution_time": 0.234
}
```

### Voice Search

**POST** `/api/nlp/voice/search`

Upload audio file for voice-to-text search.

```bash
curl -X POST "http://localhost:8000/api/nlp/voice/search?user_id=user123&language=en" \
  -F "audio_file=@query.wav"
```

**Response:**
```json
{
  "success": true,
  "text": "find vcp patterns in tech stocks",
  "alternatives": ["find bcp patterns in tech stocks"],
  "confidence": 0.92,
  "language": "en",
  "duration": 2.5,
  "query_result": {
    "intent": "scan",
    "patterns": ["vcp"],
    "sectors": ["technology"],
    ...
  }
}
```

### Autocomplete

**GET** `/api/nlp/autocomplete?query=find vcp&limit=5`

Get autocomplete suggestions for partial queries.

**Response:**
```json
{
  "query": "find vcp",
  "suggestions": [
    "Find VCP patterns in tech stocks",
    "Find VCP patterns",
    "Find VCP in high RS stocks"
  ]
}
```

### Search History

**GET** `/api/nlp/history?user_id=user123&limit=50`

Retrieve user's search history.

**Response:**
```json
[
  {
    "id": 123,
    "query": "find vcp patterns in tech",
    "intent": "scan",
    "query_type": "pattern",
    "results_count": 15,
    "confidence": 0.95,
    "created_at": "2024-01-15T10:30:00Z",
    "is_template": false,
    "template_name": null
  }
]
```

### Save Search Template

**POST** `/api/nlp/template/save`

Save a search as a reusable template.

```json
{
  "search_id": 123,
  "template_name": "Daily Tech VCP Scan",
  "tags": ["vcp", "tech", "daily"]
}
```

### Get Templates

**GET** `/api/nlp/templates?user_id=user123&include_shared=true`

Get saved search templates.

### Search Analytics

**GET** `/api/nlp/analytics?user_id=user123&days=30`

Get analytics about search patterns.

**Response:**
```json
{
  "period_days": 30,
  "total_searches": 156,
  "voice_searches": 23,
  "text_searches": 133,
  "intent_distribution": {
    "scan": 89,
    "analyze": 45,
    "compare": 22
  },
  "top_tickers": {
    "AAPL": 15,
    "NVDA": 12,
    "MSFT": 10
  },
  "top_patterns": {
    "vcp": 45,
    "cup_and_handle": 23,
    "breakout": 18
  },
  "avg_confidence": 0.87,
  "avg_results_per_query": 12.5,
  "avg_execution_time": 0.189
}
```

### Contextual Suggestions

**GET** `/api/nlp/suggestions?user_id=user123&limit=5`

Get personalized query suggestions based on search history.

### Typo Correction

**POST** `/api/nlp/correct`

Auto-correct typos in queries.

```json
{
  "query": "find cupp and handl patern"
}
```

**Response:**
```json
{
  "original": "find cupp and handl patern",
  "corrected": "find cup and handle pattern",
  "changed": true
}
```

### Supported Languages (Voice)

**GET** `/api/nlp/voice/languages`

Get list of supported languages for voice search.

**Response:**
```json
{
  "languages": {
    "en": "English (US)",
    "en-gb": "English (UK)",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese (Brazil)",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese (Simplified)"
  }
}
```

## Pattern Mappings

The system recognizes various ways to refer to patterns:

| Canonical Name | Variations |
|---------------|------------|
| `vcp` | "vcp", "volatility contraction", "vol contraction", "minervini" |
| `cup_and_handle` | "cup and handle", "cup & handle", "cup handle", "cup-and-handle" |
| `ascending_triangle` | "ascending triangle", "asc triangle", "bullish triangle" |
| `descending_triangle` | "descending triangle", "desc triangle", "bearish triangle" |
| `head_and_shoulders` | "head and shoulders", "h&s", "hs" |
| `double_top` | "double top", "twin peaks" |
| `double_bottom` | "double bottom", "twin valleys" |
| `breakout` | "breakout", "break out", "breaking out" |

## Intent Classification

Queries are classified into these intents:

- **scan**: Find stocks matching criteria ("find", "search", "show")
- **analyze**: Analyze specific stocks ("analyze", "check", "review")
- **compare**: Compare multiple stocks ("compare", "vs", "versus")
- **chart**: Display charts ("chart", "graph", "show me")
- **watchlist**: Manage watchlist ("add to watchlist", "track")
- **market**: Market overview ("market", "spy", "indices")
- **plan**: Trading planning ("position size", "risk", "entry")

## Usage Examples

### Example 1: Basic Pattern Search

```python
import httpx

response = httpx.post(
    "http://localhost:8000/api/nlp/search",
    json={
        "query": "Find VCP patterns in tech stocks",
        "user_id": "user123"
    }
)

result = response.json()
print(f"Found {result['results_count']} matches")
print(f"Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
```

### Example 2: Voice Search

```python
import httpx

with open("voice_query.wav", "rb") as f:
    response = httpx.post(
        "http://localhost:8000/api/nlp/voice/search",
        params={"user_id": "user123", "language": "en"},
        files={"audio_file": f}
    )

result = response.json()
print(f"Transcribed: {result['text']}")
print(f"Confidence: {result['confidence']:.2f}")
```

### Example 3: Complex Query with Filters

```python
response = httpx.post(
    "http://localhost:8000/api/nlp/search",
    json={
        "query": "Show me cup and handle patterns in healthcare stocks "
                 "between $50 and $150 on the weekly chart",
        "user_id": "user123"
    }
)

result = response.json()
print(f"Patterns: {result['patterns']}")
print(f"Sectors: {result['sectors']}")
print(f"Price range: ${result['price_filters']['min_price']:.0f} - "
      f"${result['price_filters']['max_price']:.0f}")
print(f"Timeframe: {result['timeframe']}")
```

### Example 4: Save and Reuse Templates

```python
# Search and save as template
search_response = httpx.post(
    "http://localhost:8000/api/nlp/search",
    json={"query": "Find VCP in tech above $100", "user_id": "user123"}
)

search_id = search_response.json()["id"]

# Save as template
template_response = httpx.post(
    "http://localhost:8000/api/nlp/template/save",
    json={
        "search_id": search_id,
        "template_name": "Daily Tech VCP Scan",
        "tags": ["vcp", "tech", "daily"]
    }
)

# Later, retrieve and reuse
templates = httpx.get(
    "http://localhost:8000/api/nlp/templates",
    params={"user_id": "user123"}
).json()

for template in templates:
    print(f"{template['template_name']}: {template['query']}")
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### 3. Initialize Database Tables

```bash
python scripts/init_nlp_search.py
```

### 4. Start the Server

```bash
uvicorn app.main:app --reload
```

### 5. Test the API

Visit: http://localhost:8000/docs#/NLP%20Search

## Configuration

No additional configuration required! The NLP search system works out of the box with the existing Legend AI setup.

### Optional: Voice Search Audio Enhancement

For better voice recognition, consider:

1. Using high-quality audio input (16kHz+ sample rate)
2. Minimizing background noise
3. Speaking clearly and at moderate pace
4. Using the audio enhancement feature (`enhance_audio: true`)

## Database Schema

### SearchHistory Table

Stores all search queries with parsed data and analytics.

```sql
CREATE TABLE search_history (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    query TEXT NOT NULL,
    query_type VARCHAR(50),
    extracted_tickers TEXT,
    extracted_patterns TEXT,
    extracted_filters TEXT,
    intent VARCHAR(100),
    confidence FLOAT,
    results_count INTEGER,
    execution_time FLOAT,
    is_template BOOLEAN DEFAULT FALSE,
    template_name VARCHAR(200),
    shared_with TEXT,
    tags TEXT,
    voice_query BOOLEAN DEFAULT FALSE,
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP
);
```

### QuerySuggestion Table

Stores contextual query suggestions.

```sql
CREATE TABLE query_suggestions (
    id SERIAL PRIMARY KEY,
    suggestion_text VARCHAR(500) NOT NULL,
    category VARCHAR(50),
    popularity_score FLOAT DEFAULT 1.0,
    context_patterns TEXT,
    context_sectors TEXT,
    example_queries TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

## Performance

- **Query Parsing**: < 50ms average
- **Voice Transcription**: 1-3 seconds (depending on audio length)
- **Search Execution**: 100-500ms (depending on complexity)
- **Autocomplete**: < 10ms
- **History Retrieval**: < 50ms

## Limitations

1. **Voice Search**: Requires internet connection for Google Speech Recognition
2. **Language Support**: Best results with English; other languages may have lower accuracy
3. **Audio Quality**: Poor audio quality will reduce transcription accuracy
4. **Ticker Recognition**: Limited to known ticker symbols (can be extended)
5. **Pattern Names**: Must match known pattern variations

## Future Enhancements

- [ ] Machine learning for better intent classification
- [ ] Semantic search with sentence embeddings
- [ ] Multi-language NLP models
- [ ] Offline voice recognition
- [ ] Custom pattern name learning
- [ ] Query result ranking
- [ ] Advanced query expansion
- [ ] RAG (Retrieval-Augmented Generation) for knowledge base

## Troubleshooting

### Issue: Low confidence scores

**Solution**: Use more specific queries with clear intent and known ticker/pattern names.

### Issue: Voice recognition fails

**Solution**:
- Check audio format is supported
- Ensure audio is not silent or too quiet
- Try audio enhancement
- Speak clearly and minimize background noise

### Issue: Pattern not recognized

**Solution**: Use full pattern names or check supported variations in Pattern Mappings table.

### Issue: No results returned

**Solution**:
- Check if filters are too restrictive
- Verify tickers/patterns are in the database
- Review parsed query to ensure correct interpretation

## Support

For issues or questions:
- Check the API docs: `/docs`
- Review examples in this guide
- Check logs for detailed error messages

## License

Part of Legend AI Trading Pattern Scanner - See main project LICENSE
