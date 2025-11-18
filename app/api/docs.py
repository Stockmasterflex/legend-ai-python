"""
Custom API Documentation Router
Provides enhanced documentation landing page with error codes and guides
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/docs", tags=["documentation"])


@router.get("/errors", response_class=HTMLResponse)
async def error_codes_reference():
    """
    📚 **Error Code Reference**

    Comprehensive guide to all API error codes and how to handle them.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Legend AI - Error Code Reference</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                line-height: 1.6;
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
            }

            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }

            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }

            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }

            .header p {
                font-size: 1.2em;
                opacity: 0.9;
            }

            .content {
                padding: 40px;
            }

            .nav-links {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                justify-content: center;
            }

            .nav-link {
                background: white;
                color: #667eea;
                padding: 10px 20px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s;
                border: 2px solid #667eea;
            }

            .nav-link:hover {
                background: #667eea;
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }

            .section {
                margin-bottom: 40px;
            }

            .section h2 {
                color: #667eea;
                font-size: 2em;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #667eea;
            }

            .error-card {
                background: #f8f9fa;
                border-left: 5px solid #dc3545;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 8px;
                transition: all 0.3s;
            }

            .error-card:hover {
                transform: translateX(5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }

            .error-card.success {
                border-left-color: #28a745;
            }

            .error-card.warning {
                border-left-color: #ffc107;
            }

            .error-card.info {
                border-left-color: #17a2b8;
            }

            .error-code {
                font-size: 1.5em;
                font-weight: bold;
                color: #dc3545;
                margin-bottom: 10px;
            }

            .error-card.success .error-code {
                color: #28a745;
            }

            .error-title {
                font-size: 1.3em;
                font-weight: 600;
                margin-bottom: 10px;
                color: #333;
            }

            .error-description {
                color: #666;
                margin-bottom: 15px;
            }

            .error-example {
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }

            .solution {
                background: #e8f5e9;
                border-left: 3px solid #28a745;
                padding: 15px;
                margin-top: 15px;
                border-radius: 5px;
            }

            .solution strong {
                color: #28a745;
                display: block;
                margin-bottom: 5px;
            }

            code {
                background: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                color: #e83e8c;
            }

            .footer {
                background: #f8f9fa;
                padding: 30px;
                text-align: center;
                color: #666;
            }

            @media (max-width: 768px) {
                .header h1 {
                    font-size: 2em;
                }

                .content {
                    padding: 20px;
                }

                .nav-links {
                    flex-direction: column;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Legend AI API</h1>
                <p>Error Code Reference Guide</p>
            </div>

            <div class="content">
                <div class="nav-links">
                    <a href="/docs" class="nav-link">📖 Interactive API Docs</a>
                    <a href="/redoc" class="nav-link">📄 ReDoc</a>
                    <a href="/openapi.json" class="nav-link">📋 OpenAPI Spec</a>
                    <a href="/api/docs/errors" class="nav-link">⚠️ Error Codes</a>
                </div>

                <div class="section">
                    <h2>📊 HTTP Status Codes</h2>

                    <div class="error-card success">
                        <div class="error-code">200 OK</div>
                        <div class="error-title">✅ Success</div>
                        <div class="error-description">
                            Request completed successfully. Response contains requested data.
                        </div>
                        <div class="error-example">
{
  "success": true,
  "data": { ... },
  "cached": false,
  "processing_time": 1.23
}
                        </div>
                    </div>

                    <div class="error-card">
                        <div class="error-code">400 Bad Request</div>
                        <div class="error-title">Invalid Request Parameters</div>
                        <div class="error-description">
                            The request contains invalid or malformed parameters. Check your input data.
                        </div>
                        <div class="error-example">
{
  "detail": "Invalid ticker symbol format"
}
                        </div>
                        <div class="solution">
                            <strong>💡 Solution:</strong>
                            Validate your input parameters. Ticker symbols should be alphanumeric (e.g., "AAPL", "TSLA").
                            Ensure required fields are provided and match expected format.
                        </div>
                    </div>

                    <div class="error-card">
                        <div class="error-code">404 Not Found</div>
                        <div class="error-title">Resource Not Found</div>
                        <div class="error-description">
                            The requested resource (ticker, endpoint, etc.) could not be found.
                        </div>
                        <div class="error-example">
{
  "detail": "No price data available for INVALID"
}
                        </div>
                        <div class="solution">
                            <strong>💡 Solution:</strong>
                            Verify the ticker symbol exists and is actively traded. Check for typos.
                            Try major tickers like "AAPL", "MSFT", "GOOGL" to test connectivity.
                        </div>
                    </div>

                    <div class="error-card warning">
                        <div class="error-code">429 Too Many Requests</div>
                        <div class="error-title">Rate Limit Exceeded</div>
                        <div class="error-description">
                            You've exceeded the rate limit of 60 requests per minute.
                        </div>
                        <div class="error-example">
{
  "error": "Rate limit exceeded",
  "detail": "Maximum 60 requests per minute. Try again in 30 seconds."
}
                        </div>
                        <div class="solution">
                            <strong>💡 Solution:</strong>
                            Implement exponential backoff in your client. Wait for the specified retry time.
                            Consider caching responses on your end to reduce API calls.
                            Contact support for higher rate limits.
                        </div>
                    </div>

                    <div class="error-card">
                        <div class="error-code">500 Internal Server Error</div>
                        <div class="error-title">Server Error</div>
                        <div class="error-description">
                            An unexpected error occurred on the server while processing your request.
                        </div>
                        <div class="error-example">
{
  "success": false,
  "error": "Pattern analysis failed",
  "detail": "Internal processing error"
}
                        </div>
                        <div class="solution">
                            <strong>💡 Solution:</strong>
                            Retry the request after a short delay. If the error persists, check system status.
                            Report persistent errors with request details for investigation.
                        </div>
                    </div>

                    <div class="error-card">
                        <div class="error-code">503 Service Unavailable</div>
                        <div class="error-title">Service Temporarily Unavailable</div>
                        <div class="error-description">
                            The service or an external dependency is temporarily unavailable.
                        </div>
                        <div class="error-example">
{
  "detail": "AI Assistant is not available. Please check OPENAI_API_KEY configuration."
}
                        </div>
                        <div class="solution">
                            <strong>💡 Solution:</strong>
                            Wait a few moments and retry. External data providers may be experiencing downtime.
                            Check /health endpoint for service status details.
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>🔍 Common Error Scenarios</h2>

                    <div class="error-card info">
                        <div class="error-title">Invalid Ticker Symbol</div>
                        <div class="error-description">
                            <strong>Cause:</strong> Ticker symbol contains invalid characters or format.<br>
                            <strong>Example:</strong> <code>"AAPL!"</code>, <code>"123"</code>, <code>""</code>
                        </div>
                        <div class="solution">
                            <strong>💡 Fix:</strong>
                            Use valid ticker symbols (alphanumeric with optional dots/dashes).
                            Examples: "AAPL", "BRK.B", "SPY"
                        </div>
                    </div>

                    <div class="error-card info">
                        <div class="error-title">No Market Data Available</div>
                        <div class="error-description">
                            <strong>Cause:</strong> Symbol not found in any data provider, or markets closed for extended period.<br>
                            <strong>Example:</strong> Delisted stocks, invalid symbols, very small-cap stocks.
                        </div>
                        <div class="solution">
                            <strong>💡 Fix:</strong>
                            Verify symbol is actively traded on major exchanges.
                            Check if company has been delisted or merged.
                            Try alternative data sources or wait for market hours.
                        </div>
                    </div>

                    <div class="error-card info">
                        <div class="error-title">Pattern Analysis Failed</div>
                        <div class="error-description">
                            <strong>Cause:</strong> Insufficient data, data quality issues, or no clear pattern detected.<br>
                            <strong>Example:</strong> Very volatile stocks, insufficient price history, flat price action.
                        </div>
                        <div class="solution">
                            <strong>💡 Fix:</strong>
                            Ensure stock has sufficient trading history (at least 3 months).
                            Try different timeframes (1day vs 1week).
                            Some stocks may not show clear patterns at given moment.
                        </div>
                    </div>

                    <div class="error-card info">
                        <div class="error-title">AI Service Unavailable</div>
                        <div class="error-description">
                            <strong>Cause:</strong> OpenAI API key not configured or quota exceeded.<br>
                            <strong>Example:</strong> Missing <code>OPENAI_API_KEY</code>, API quota exhausted.
                        </div>
                        <div class="solution">
                            <strong>💡 Fix:</strong>
                            Check environment variables are properly set.
                            Verify OpenAI API key is valid and has sufficient credits.
                            Contact administrator if self-hosted.
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>📚 Best Practices</h2>

                    <div class="error-card success">
                        <div class="error-title">✅ Error Handling Example (Python)</div>
                        <div class="error-example">
import requests
from time import sleep

def get_pattern_with_retry(ticker, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                'https://your-api.com/api/patterns/detect',
                json={'ticker': ticker, 'interval': '1day'},
                timeout=10
            )

            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"Rate limited. Waiting {retry_after}s...")
                sleep(retry_after)
                continue

            # Raise for other error codes
            response.raise_for_status()

            result = response.json()
            if result['success']:
                return result['data']
            else:
                print(f"Error: {result.get('error')}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                sleep(2 ** attempt)  # Exponential backoff

    return None

# Usage
pattern = get_pattern_with_retry('AAPL')
if pattern:
    print(f"Pattern: {pattern['pattern']} (Score: {pattern['score']}/10)")
                        </div>
                    </div>

                    <div class="error-card success">
                        <div class="error-title">✅ Error Handling Example (JavaScript)</div>
                        <div class="error-example">
async function getPatternWithRetry(ticker, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fetch('/api/patterns/detect', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ticker, interval: '1day'})
      });

      // Handle rate limiting
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After') || 60;
        console.log(`Rate limited. Waiting ${retryAfter}s...`);
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
        continue;
      }

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      if (result.success) {
        return result.data;
      } else {
        console.error('Error:', result.error);
        return null;
      }

    } catch (error) {
      console.error(`Attempt ${attempt + 1} failed:`, error);
      if (attempt < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
      }
    }
  }

  return null;
}

// Usage
const pattern = await getPatternWithRetry('AAPL');
if (pattern) {
  console.log(`Pattern: ${pattern.pattern} (Score: ${pattern.score}/10)`);
}
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>🆘 Getting Help</h2>
                    <p style="margin-bottom: 15px;">If you encounter errors not covered in this guide:</p>
                    <ul style="margin-left: 20px; color: #666;">
                        <li style="margin-bottom: 10px;">Check the <code>/health</code> endpoint for service status</li>
                        <li style="margin-bottom: 10px;">Review the <a href="/docs" style="color: #667eea;">interactive API documentation</a></li>
                        <li style="margin-bottom: 10px;">Check GitHub issues for known problems</li>
                        <li style="margin-bottom: 10px;">Enable debug logging to see detailed error information</li>
                    </ul>
                </div>
            </div>

            <div class="footer">
                <p><strong>Legend AI Trading Platform</strong></p>
                <p>© 2024 - Professional Pattern Scanner API</p>
                <p style="margin-top: 10px;">
                    <a href="https://github.com/Stockmasterflex/legend-ai-python" style="color: #667eea; text-decoration: none;">GitHub</a> |
                    <a href="/docs" style="color: #667eea; text-decoration: none;">API Docs</a> |
                    <a href="/health" style="color: #667eea; text-decoration: none;">Status</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.get("/getting-started", response_class=HTMLResponse)
async def getting_started_guide():
    """
    🚀 **Getting Started Guide**

    Quick start guide for using the Legend AI API.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Legend AI - Getting Started</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
            }

            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }

            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }

            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }

            .content {
                padding: 40px;
            }

            .section {
                margin-bottom: 40px;
            }

            h2 {
                color: #667eea;
                font-size: 2em;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #667eea;
            }

            .code-block {
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 20px;
                border-radius: 10px;
                overflow-x: auto;
                margin: 20px 0;
                font-family: 'Courier New', monospace;
            }

            .step {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                border-left: 5px solid #667eea;
            }

            .step-number {
                background: #667eea;
                color: white;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Getting Started</h1>
                <p>Legend AI Pattern Scanner API</p>
            </div>

            <div class="content">
                <div class="section">
                    <h2>Quick Start</h2>

                    <div class="step">
                        <span class="step-number">1</span>
                        <strong>Make Your First Request</strong>
                        <div class="code-block">
curl -X POST "http://localhost:8000/api/patterns/detect" \\
  -H "Content-Type: application/json" \\
  -d '{"ticker": "AAPL", "interval": "1day"}'
                        </div>
                    </div>

                    <div class="step">
                        <span class="step-number">2</span>
                        <strong>Explore the Interactive Docs</strong>
                        <p style="margin-top: 10px;">Visit <a href="/docs">/docs</a> to try all endpoints in your browser</p>
                    </div>

                    <div class="step">
                        <span class="step-number">3</span>
                        <strong>Check Service Health</strong>
                        <div class="code-block">
curl http://localhost:8000/health
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>Popular Endpoints</h2>

                    <h3>🎯 Pattern Detection</h3>
                    <div class="code-block">
POST /api/patterns/detect
{
  "ticker": "AAPL",
  "interval": "1day"
}
                    </div>

                    <h3>🤖 AI Chat</h3>
                    <div class="code-block">
POST /api/ai/chat
{
  "message": "What are the best tech stocks?",
  "include_market_data": true
}
                    </div>

                    <h3>📊 AI Stock Analysis</h3>
                    <div class="code-block">
POST /api/ai/analyze
{
  "symbol": "TSLA"
}
                    </div>
                </div>

                <div class="section">
                    <h2>📚 Resources</h2>
                    <ul>
                        <li><a href="/docs">📖 Interactive API Docs (Swagger UI)</a></li>
                        <li><a href="/redoc">📄 Alternative Docs (ReDoc)</a></li>
                        <li><a href="/api/docs/errors">⚠️ Error Code Reference</a></li>
                        <li><a href="/openapi.json">📋 OpenAPI Schema</a></li>
                        <li><a href="/health">💚 Health Check</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
