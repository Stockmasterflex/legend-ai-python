# 🚀 API Documentation Guide

## Overview

Beautiful, comprehensive API documentation has been auto-generated for the Legend AI Trading Platform. This guide explains all the new documentation features and how to access them.

## 📚 Documentation Endpoints

### 1. Interactive Swagger UI
**URL:** `/docs`

The primary interactive API documentation interface with:
- ✅ All endpoints organized by tags
- ✅ Interactive "Try it out" functionality
- ✅ Code examples in Python, JavaScript, and cURL
- ✅ Request/response schemas
- ✅ Real-time testing
- ✅ Monokai syntax highlighting

### 2. ReDoc Alternative View
**URL:** `/redoc`

Alternative documentation view with:
- Clean, professional layout
- Three-column design
- Better for reading and reference
- Mobile-responsive

### 3. OpenAPI Schema
**URL:** `/openapi.json`

Raw OpenAPI 3.0 specification:
- Use with code generators
- Import into API testing tools
- Integrate with CI/CD pipelines

### 4. Error Code Reference
**URL:** `/api/docs/errors`

**NEW!** Beautiful HTML page documenting:
- All HTTP status codes (200, 400, 404, 429, 500, 503)
- Common error scenarios
- Solutions for each error
- Best practices for error handling
- Code examples in Python and JavaScript

### 5. Getting Started Guide
**URL:** `/api/docs/getting-started`

**NEW!** Quick start guide with:
- First API request examples
- Popular endpoint references
- Quick navigation links

## 🎯 Key Features Implemented

### Enhanced OpenAPI Configuration

**File:** `app/docs_config.py`

New centralized documentation configuration including:
- Rich tag metadata with descriptions and emojis
- Detailed API description with markdown formatting
- Contact information
- License information
- Code examples repository
- Error response templates

### Customized Swagger UI

**Configuration:**
```python
swagger_ui_parameters={
    "defaultModelsExpandDepth": -1,  # Hide schemas by default
    "docExpansion": "list",          # Expand tag lists
    "filter": True,                  # Enable search
    "syntaxHighlight.theme": "monokai",  # Beautiful highlighting
    "tryItOutEnabled": True,         # Enable testing
}
```

### Enhanced Endpoint Documentation

#### Pattern Detection (`/api/patterns/detect`)
- ✅ Rich docstring with markdown formatting
- ✅ Code examples in 3 languages
- ✅ Response examples
- ✅ Error scenarios (400, 404)
- ✅ Field descriptions table
- ✅ Usage notes

#### AI Chat (`/api/ai/chat`)
- ✅ Comprehensive usage guide
- ✅ Multi-language code examples
- ✅ Tips for best results
- ✅ Response format documentation

#### AI Analysis (`/api/ai/analyze`)
- ✅ What you get section
- ✅ Code examples
- ✅ Response format details

### Pydantic Model Examples

All request/response models now include:
- Field-level descriptions
- Examples in Config class
- Type annotations
- Default values

**Example:**
```python
class PatternRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol", example="AAPL")
    interval: str = Field("1day", description="Time interval", example="1day")

    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "AAPL",
                "interval": "1day"
            }
        }
```

### Enhanced Root Endpoint

**URL:** `/`

Now returns comprehensive API information:
- Service status
- Documentation links
- Popular endpoints
- Feature list
- Quick navigation

## 📊 Tag Organization

All endpoints are organized into logical groups:

| Tag | Description | Endpoints |
|-----|-------------|-----------|
| 🎯 patterns | Pattern Detection & Analysis | `/api/patterns/*` |
| 🤖 AI Assistant | AI-Powered Trading Assistant | `/api/ai/*` |
| 📊 charts | Professional Chart Generation | `/api/charts/*` |
| 🌌 universe | Market Universe Scanner | `/api/universe/*` |
| 👁️ watchlist | Watchlist Management | `/api/watchlist/*` |
| 📈 analytics | Market Analytics | `/api/analytics/*` |
| 💹 market | Real-time Market Data | `/api/market/*` |

...and more!

## 🔥 Code Examples

Every major endpoint includes code examples in:

### Python
```python
import requests

response = requests.post(
    'https://your-api.com/api/patterns/detect',
    json={'ticker': 'AAPL', 'interval': '1day'}
)

result = response.json()
if result['success']:
    print(f"Pattern: {result['data']['pattern']}")
```

### JavaScript
```javascript
const response = await fetch('/api/patterns/detect', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({ticker: 'AAPL', interval: '1day'})
});
const result = await response.json();
```

### cURL
```bash
curl -X POST "https://your-api.com/api/patterns/detect" \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "interval": "1day"}'
```

## ⚠️ Error Code Reference

Comprehensive error documentation including:

### HTTP Status Codes
- **200 OK** - Success with response examples
- **400 Bad Request** - Invalid parameters with solutions
- **404 Not Found** - Resource not found with fixes
- **429 Too Many Requests** - Rate limiting with retry logic
- **500 Internal Server Error** - Server errors with debugging
- **503 Service Unavailable** - Service down with status checks

### Common Scenarios
- Invalid ticker symbols
- No market data available
- Pattern analysis failures
- AI service unavailable
- Rate limit exceeded

### Best Practices
- Retry logic with exponential backoff
- Rate limit handling
- Error response parsing
- Timeout configuration

## 🎨 Beautiful Design

The custom documentation pages feature:
- Gradient backgrounds
- Responsive design
- Professional color scheme
- Syntax highlighting
- Interactive hover effects
- Mobile-friendly layout
- Clean typography

## 🚀 Quick Start

1. **Start the API:**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Access Documentation:**
   - Main docs: http://localhost:8000/docs
   - Error reference: http://localhost:8000/api/docs/errors
   - Getting started: http://localhost:8000/api/docs/getting-started

3. **Test an Endpoint:**
   - Click on `/api/patterns/detect`
   - Click "Try it out"
   - Enter ticker (e.g., "AAPL")
   - Click "Execute"

## 📝 Files Modified/Created

### New Files
- `app/docs_config.py` - OpenAPI configuration and metadata
- `app/api/docs.py` - Custom documentation endpoints
- `docs/API_DOCUMENTATION_GUIDE.md` - This guide

### Modified Files
- `app/main.py` - Enhanced FastAPI app with custom config
- `app/api/patterns.py` - Added rich examples and documentation
- `app/routers/ai_chat.py` - Enhanced endpoint documentation

## 🎯 Benefits

1. **Easier to Use** - Interactive testing right in the browser
2. **Better Reference** - Comprehensive code examples
3. **Error Handling** - Clear guidance on handling errors
4. **Onboarding** - Quick start guide for new developers
5. **Professional** - Beautiful, polished documentation
6. **Self-Service** - Users can explore without asking questions

## 🔗 External Links

- **GitHub:** https://github.com/Stockmasterflex/legend-ai-python
- **OpenAPI Spec:** http://localhost:8000/openapi.json
- **Health Check:** http://localhost:8000/health

## 💡 Tips

1. Use the **filter/search** feature in Swagger UI to find endpoints quickly
2. Check the **error reference** when debugging API issues
3. Copy code examples directly from the docs
4. Use the "Try it out" feature to test before integrating
5. Bookmark `/api/docs/errors` for quick reference

---

**Built with:** FastAPI OpenAPI 3.0, Swagger UI, ReDoc, Custom HTML/CSS

**Author:** Legend AI Team

**License:** MIT
