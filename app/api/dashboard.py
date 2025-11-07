from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# Resolve the dashboard template relative to the repository root so it works
# locally and inside Railway containers.
TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "templates" / "dashboard.html"


@router.get("", response_class=HTMLResponse)
async def get_dashboard():
    """
    Serve the main Legend AI dashboard
    
    Modern dashboard with:
    - Pattern scanner (single ticker)
    - Universe scanner (bulk analysis)
    - Watchlist management
    - Market internals display
    - Multi-timeframe charts
    - Real-time KPI tiles
    """
    try:
        html_content = TEMPLATE_PATH.read_text(encoding="utf-8")
        ver = os.getenv("GIT_COMMIT", "unknown")[:7]
        # Cache-busting for static assets and inline version token
        html_content = html_content.replace("__VERSION__", ver)

        logger.info("📊 Serving dashboard")
        return html_content
        
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return f"""
        <html>
        <head>
            <title>Legend AI - Dashboard Error</title>
            <style>
                body {{ background: #0f0f0f; color: #e5e7eb; font-family: sans-serif; padding: 40px; }}
                .error {{ color: #ef4444; }}
            </style>
        </head>
        <body>
            <h1>Dashboard Error</h1>
            <p class="error">Could not load dashboard: {str(e)}</p>
            <p><a href="/docs" style="color: #3b82f6;">View API Documentation</a></p>
        </body>
        </html>
        """


@router.get("/test", response_class=HTMLResponse)
async def dashboard_test():
    """Test endpoint to verify dashboard is accessible"""
    return """
    <html>
    <head>
        <title>Legend AI - Dashboard Test</title>
        <style>
            body {
                background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
                color: #e5e7eb;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                padding: 40px;
                margin: 0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                color: #3b82f6;
                margin-bottom: 20px;
            }
            .status {
                background: rgba(34, 197, 94, 0.1);
                border: 1px solid #22c55e;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }
            .link {
                color: #3b82f6;
                text-decoration: none;
                margin-right: 20px;
            }
            .link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ Legend AI Dashboard</h1>
            <div class="status">
                <strong>Status:</strong> Dashboard service is running
            </div>
            <p>
                <a href="/dashboard" class="link">← Back to Dashboard</a>
                <a href="/docs" class="link">API Docs →</a>
            </p>
            <h2>Available Features</h2>
            <ul>
                <li>🔍 Pattern Scanner - Analyze single tickers for pattern setups</li>
                <li>🌌 Universe Scan - Bulk scan S&P 500 or NASDAQ 100</li>
                <li>👁️ Watchlist - Manage watched stocks with status tracking</li>
                <li>📊 Market Internals - Real-time market regime and breadth</li>
                <li>📈 Multi-Timeframe Charts - Generate Chart-IMG charts across timeframes</li>
            </ul>
        </div>
    </body>
    </html>
    """
