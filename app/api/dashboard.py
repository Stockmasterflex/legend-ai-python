from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os
import logging
from pathlib import Path
import subprocess

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# Resolve the dashboard template relative to the repository root so it works
# locally and inside Railway containers.
TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "templates" / "dashboard.html"
MARKET_VIZ_TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "templates" / "market_viz.html"
TV_TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "templates" / "partials" / "tv_widget_templates.html"


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
        # Resolve build SHA for cache-busting and display
        build_sha = _resolve_build_sha()
        # Back-compat for any assets using __VERSION__ token elsewhere
        html_content = html_content.replace("__VERSION__", build_sha)
        # Inject build sha placeholder for dashboard.js and header text
        html_content = html_content.replace("{{ build_sha }}", build_sha)
        html_content = _inject_tv_templates(html_content)

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


@router.get("/viz", response_class=HTMLResponse)
async def get_market_viz_dashboard():
    """
    Serve the Market Visualization Dashboard

    Interactive visualizations including:
    - Sector Heatmap (11 sectors with real-time performance)
    - Stock Screener Heatmap (S&P 500 + NASDAQ 100)
    - Pattern Distribution Map (detected patterns across universe)
    - Correlation Matrix (identify leading/lagging stocks)
    - Market Breadth Dashboard (advance/decline, new highs/lows, sector rotation)
    """
    try:
        html_content = MARKET_VIZ_TEMPLATE_PATH.read_text(encoding="utf-8")
        # Resolve build SHA for cache-busting
        build_sha = _resolve_build_sha()
        html_content = html_content.replace("{{ build_sha }}", build_sha)

        logger.info("📊 Serving market visualization dashboard")
        return html_content

    except Exception as e:
        logger.error(f"Error loading market viz dashboard: {e}")
        return f"""
        <html>
        <head>
            <title>Legend AI - Viz Dashboard Error</title>
            <style>
                body {{ background: #0f0f0f; color: #e5e7eb; font-family: sans-serif; padding: 40px; }}
                .error {{ color: #ef4444; }}
            </style>
        </head>
        <body>
            <h1>Visualization Dashboard Error</h1>
            <p class="error">Could not load visualization dashboard: {str(e)}</p>
            <p><a href="/dashboard" style="color: #3b82f6;">← Back to Dashboard</a></p>
        </body>
        </html>
        """


def _resolve_build_sha() -> str:
    """Resolve a short build SHA for cache-busting and display.

    Order of precedence:
    1) BUILD_SHA
    2) GIT_COMMIT
    3) RAILWAY_GIT_COMMIT_SHA
    4) `git rev-parse --short HEAD`
    Fallback: "unknown"
    """
    for key in ("BUILD_SHA", "GIT_COMMIT", "RAILWAY_GIT_COMMIT_SHA"):
        v = os.getenv(key)
        if v:
            s = str(v).strip()
            # If it's a full SHA, keep short 7 chars for display/cache param
            return s[:7]
    try:
        sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
        return sha or "unknown"
    except Exception:
        return "unknown"


def _inject_tv_templates(html: str) -> str:
    """Insert shared TradingView templates into the page."""
    if "<!--TV_WIDGET_TEMPLATES-->" not in html:
        return html
    try:
        partial = TV_TEMPLATE_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        partial = ""
    return html.replace("<!--TV_WIDGET_TEMPLATES-->", partial)
