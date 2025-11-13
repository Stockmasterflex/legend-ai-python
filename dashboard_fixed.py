"""
Legend AI - Fixed Trading Dashboard
Works with both local and production APIs
"""
import gradio as gr
import httpx
import json
import os
from datetime import datetime

# Try Railway first, fallback to localhost
API_BASE = os.getenv("API_BASE", "http://localhost:8000")
TIMEOUT = 30

def analyze_pattern(ticker):
    """Analyze single ticker for patterns - SYNCHRONOUS"""
    if not ticker or not ticker.strip():
        return "❌ Please enter a valid ticker symbol"

    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{API_BASE}/api/patterns/detect", json={"ticker": ticker.strip().upper()})
            r.raise_for_status()
            data = r.json()

            if data.get("success"):
                d = data["data"]
                result = f"""## 📊 {ticker.upper()} Pattern Analysis

**Pattern Found:** {d.get('pattern', 'NONE')}
**Setup Score:** {d.get('score', 0)}/10 ⭐

### Trading Levels
- **Entry:** ${d.get('entry', 0):.2f}
- **Stop Loss:** ${d.get('stop', 0):.2f}
- **Target:** ${d.get('target', 0):.2f}
- **Risk/Reward:** {d.get('risk_reward', 0):.2f}:1

### Technical Metrics
- **Current Price:** ${d.get('current_price', 0):.2f}
- **RS Rating:** {d.get('rs_rating', 0):.0f}

**Analysis Time:** {data.get('processing_time', 0)}s | **Cached:** {"Yes" if data.get('cached') else "No"}
"""
                return result
            else:
                return f"❌ Error: {data.get('error', 'Unknown error')}"
    except httpx.TimeoutException:
        return f"❌ Request timed out. API might be down or slow."
    except httpx.HTTPStatusError as e:
        return f"❌ HTTP Error {e.response.status_code}: {e.response.text[:200]}"
    except Exception as e:
        return f"❌ Error analyzing {ticker}: {str(e)}\n\nAPI Base: {API_BASE}"

def scan_universe():
    """Scan universe for top setups - SYNCHRONOUS"""
    try:
        with httpx.Client(timeout=60) as client:
            r = client.post(f"{API_BASE}/api/universe/scan/quick")
            r.raise_for_status()
            data = r.json()

            if data.get("success"):
                results = data.get("results", [])
                if not results:
                    return "No strong setups found in quick scan. Try again later."

                output = f"""## 🔍 Universe Scan Results
**Scanned:** {data.get('total_scanned', 0)} stocks | **Found:** {len(results)} strong setups

"""
                for i, item in enumerate(results[:15], 1):
                    output += f"""### {i}. {item['ticker']} - {item['pattern']} ({item['score']}/10)
- Entry: ${item['entry']:.2f} | Stop: ${item['stop']:.2f} | Target: ${item['target']:.2f}
- R:R: {item.get('risk_reward', 0):.2f}:1

"""
                return output
            return "❌ Scan failed"
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nAPI Base: {API_BASE}"

def get_watchlist_display():
    """Get watchlist - SYNCHRONOUS"""
    try:
        with httpx.Client(timeout=10) as client:
            r = client.get(f"{API_BASE}/api/watchlist")
            r.raise_for_status()
            data = r.json()

            if data.get("success"):
                items = data.get("items", [])
                if not items:
                    return "📝 Watchlist is empty. Add tickers below!"

                output = f"""## 📋 Your Watchlist ({len(items)} tickers)

"""
                for item in items:
                    output += f"""### {item['ticker']}
- **Status:** {item.get('status', 'Watching')}
- **Reason:** {item.get('reason', 'N/A')}
- **Added:** {item.get('added_date', 'Unknown')[:10]}

"""
                return output
            return "❌ Error loading watchlist"
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nAPI Base: {API_BASE}"

def add_to_watchlist(ticker, reason):
    """Add ticker to watchlist - SYNCHRONOUS"""
    if not ticker or not ticker.strip():
        return "❌ Please enter a valid ticker"

    try:
        with httpx.Client(timeout=10) as client:
            r = client.post(f"{API_BASE}/api/watchlist/add",
                          json={"ticker": ticker.upper().strip(), "reason": reason or "Monitoring"})
            r.raise_for_status()
            data = r.json()

            if data.get("success"):
                # Auto-refresh watchlist
                return f"✅ Added {ticker.upper()} to watchlist!"
            return f"❌ Error: {data.get('detail', 'Unknown error')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def create_trade_plan(ticker, entry, stop, account_size, risk_pct):
    """Create trade plan - SYNCHRONOUS"""
    try:
        with httpx.Client(timeout=10) as client:
            r = client.post(f"{API_BASE}/api/trade/plan", json={
                "ticker": ticker.upper().strip(),
                "entry": float(entry),
                "stop": float(stop),
                "account_size": float(account_size),
                "risk_percent": float(risk_pct)
            })
            r.raise_for_status()
            data = r.json()

            return f"""## 💼 Trade Plan: {data['ticker']}

### Position Details
- **Entry Price:** ${data['entry']:.2f}
- **Stop Loss:** ${data['stop']:.2f}
- **Target:** ${data['target']:.2f}

### Position Sizing
- **Shares to Buy:** {data['position_size']} shares
- **Position Value:** ${data['position_value']:,.2f}
- **Risk Amount:** ${data['risk_amount']:.2f} ({risk_pct}% of account)

### Risk/Reward
- **R:R Ratio:** {data['risk_reward']:.2f}:1
- **Potential Profit:** ${(data['target'] - data['entry']) * data['position_size']:.2f}
- **Potential Loss:** ${data['risk_amount']:.2f}

---
**Account Size:** ${account_size:,.2f}
"""
    except Exception as e:
        return f"❌ Error: {str(e)}"

def check_api_health():
    """Check if API is accessible"""
    try:
        with httpx.Client(timeout=5) as client:
            r = client.get(f"{API_BASE}/health")
            data = r.json()
            return f"""## 🟢 API Status: Online

**API Base:** {API_BASE}
**Status:** {data.get('status', 'unknown')}
**Telegram:** {data.get('telegram', 'unknown')}
**Redis:** {data.get('redis', 'unknown')}
**Version:** {data.get('version', 'unknown')}
"""
    except Exception as e:
        return f"""## 🔴 API Status: Offline

**API Base:** {API_BASE}
**Error:** {str(e)}

**Troubleshooting:**
1. Make sure FastAPI server is running: `uvicorn app.main:app --port 8000`
2. Or set API_BASE environment variable to Railway URL
3. Check Railway deployment status if using production
"""

# Custom CSS
custom_css = """
.gradio-container {
    font-family: 'Inter', sans-serif;
    max-width: 1400px !important;
}
.tab-nav button {
    font-size: 16px;
    font-weight: 600;
}
h1 {
    text-align: center;
    color: #1f2937;
    margin-bottom: 20px;
}
"""

# Build Gradio Interface
with gr.Blocks(title="Legend AI Trading Dashboard", theme=gr.themes.Soft(), css=custom_css) as dashboard:
    gr.Markdown("# 🚀 Legend AI Trading Dashboard")
    gr.Markdown(f"*Professional Pattern Scanner & Trading Intelligence Platform*")
    gr.Markdown(f"**API:** `{API_BASE}`")

    # API Health Check
    with gr.Accordion("🔍 API Status", open=False):
        health_output = gr.Markdown()
        health_btn = gr.Button("Check API Health")
        health_btn.click(check_api_health, inputs=None, outputs=health_output)
        # Auto-check on load
        dashboard.load(check_api_health, inputs=None, outputs=health_output)

    with gr.Tab("📊 Pattern Scanner"):
        gr.Markdown("### Analyze individual stocks for Minervini-style pattern setups")
        with gr.Row():
            pattern_ticker = gr.Textbox(label="Ticker Symbol", placeholder="AAPL", value="NVDA")
            pattern_btn = gr.Button("🔍 Analyze Pattern", variant="primary", scale=0)
        pattern_output = gr.Markdown()
        pattern_btn.click(analyze_pattern, inputs=[pattern_ticker], outputs=pattern_output)

    with gr.Tab("🌐 Universe Scanner"):
        gr.Markdown("### Scan S&P 500 & NASDAQ 100 for top setups")
        scan_btn = gr.Button("🔍 Run Quick Scan", variant="primary", size="lg")
        scan_output = gr.Markdown()
        scan_btn.click(scan_universe, inputs=None, outputs=scan_output)

    with gr.Tab("📋 Watchlist"):
        gr.Markdown("### Manage your trading watchlist")
        with gr.Row():
            with gr.Column():
                wl_ticker = gr.Textbox(label="Ticker Symbol", placeholder="TSLA")
                wl_reason = gr.Textbox(label="Reason / Notes", placeholder="VCP setup breaking out")
                add_btn = gr.Button("➕ Add to Watchlist", variant="primary")
                add_output = gr.Textbox(label="Status", lines=2)
                add_btn.click(add_to_watchlist, inputs=[wl_ticker, wl_reason], outputs=add_output)

            with gr.Column():
                refresh_btn = gr.Button("🔄 Refresh Watchlist", variant="secondary")
                watchlist_output = gr.Markdown()
                refresh_btn.click(get_watchlist_display, inputs=None, outputs=watchlist_output)
                # Auto-load on start
                dashboard.load(get_watchlist_display, inputs=None, outputs=watchlist_output)

    with gr.Tab("💼 Trade Planner"):
        gr.Markdown("### Calculate position size and risk/reward")
        with gr.Row():
            with gr.Column():
                tp_ticker = gr.Textbox(label="Ticker", value="NVDA")
                tp_entry = gr.Number(label="Entry Price", value=145.50)
                tp_stop = gr.Number(label="Stop Loss", value=140.00)
            with gr.Column():
                tp_account = gr.Number(label="Account Size ($)", value=10000)
                tp_risk = gr.Number(label="Risk Per Trade (%)", value=2.0)

        plan_btn = gr.Button("📋 Create Trade Plan", variant="primary")
        plan_output = gr.Markdown()
        plan_btn.click(create_trade_plan,
                      inputs=[tp_ticker, tp_entry, tp_stop, tp_account, tp_risk],
                      outputs=plan_output)

    with gr.Tab("ℹ️ About"):
        gr.Markdown(f"""## About Legend AI

**Legend AI** is a professional trading intelligence platform that helps you:

- 🔍 **Scan thousands of stocks** for Minervini-style pattern setups
- 📊 **Analyze technical patterns** (VCP, Cup & Handle, Flat Base)
- 💼 **Plan trades** with proper position sizing
- 📈 **Track performance** and improve your edge
- 🤖 **Telegram bot** for on-the-go analysis

### Current Configuration
- **API Base:** `{API_BASE}`
- **Dashboard Port:** 7860
- **Version:** 1.0.0

### How to Use
1. **Pattern Scanner:** Enter any ticker to analyze
2. **Universe Scanner:** Find top setups automatically
3. **Watchlist:** Track tickers you're monitoring
4. **Trade Planner:** Calculate position sizes

### Troubleshooting
- If you see "Connection Error", make sure the API server is running
- For local testing: `uvicorn app.main:app --port 8000`
- For production: Set `API_BASE` environment variable
""")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Legend AI Trading Dashboard")
    print("=" * 60)
    print(f"API Base: {API_BASE}")
    print(f"Dashboard: http://localhost:7860")
    print("=" * 60)

    dashboard.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        favicon_path=None
    )
