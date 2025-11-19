"""
Legend AI - Ultimate Trading Dashboard
Professional web interface with all features
"""
import gradio as gr
import httpx
import json
import pandas as pd
from datetime import datetime

API_BASE = "https://legend-ai-python-production.up.railway.app"

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

async def analyze_pattern(ticker):
    """Analyze single ticker for patterns"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{API_BASE}/api/patterns/detect", json={"ticker": ticker})
            data = r.json()
            if data.get("success"):
                d = data["data"]
                result = f"""## 📊 {ticker} Pattern Analysis

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
            return f"❌ Error: {data.get('error', 'Unknown error')}"
    except Exception as e:
        return f"❌ Error analyzing {ticker}: {str(e)}"

async def scan_universe():
    """Scan universe for top setups"""
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(f"{API_BASE}/api/universe/scan/quick")
            data = r.json()
            if data.get("success"):
                results = data.get("results", [])
                if not results:
                    return "No strong setups found in quick scan. Try full universe scan later."
                
                output = f"""## 🔍 Universe Scan Results
**Scanned:** {data.get('scanned', 0)} stocks | **Found:** {len(results)} strong setups

"""
                for i, item in enumerate(results[:15], 1):
                    output += f"""### {i}. {item['ticker']} - {item['pattern']} ({item['score']}/10)
- Entry: ${item['entry']:.2f} | Stop: ${item['stop']:.2f} | Target: ${item['target']:.2f}
- R:R: {item.get('risk_reward', 0):.2f}:1

"""
                return output
            return "❌ Scan failed"
    except Exception as e:
        return f"❌ Error: {str(e)}"

async def get_watchlist_display():
    """Get watchlist"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{API_BASE}/api/watchlist")
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
        return f"❌ Error: {str(e)}"

async def add_to_watchlist(ticker, reason):
    """Add ticker to watchlist"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(f"{API_BASE}/api/watchlist/add", 
                                json={"ticker": ticker.upper(), "reason": reason})
            data = r.json()
            if data.get("success"):
                return f"✅ Added {ticker.upper()} to watchlist!"
            return f"❌ Error: {data.get('detail', 'Unknown error')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

async def create_trade_plan(ticker, entry, stop, account_size, risk_pct):
    """Create trade plan with position sizing"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(f"{API_BASE}/api/trade/plan", json={
                "ticker": ticker.upper(),
                "entry": float(entry),
                "stop": float(stop),
                "account_size": float(account_size),
                "risk_percent": float(risk_pct)
            })
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

async def get_market_status():
    """Get market internals"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{API_BASE}/api/market/internals")
            data = r.json()
            return f"""## 📈 Market Internals

**S&P 500:** ${data.get('spy_price', 0):.2f}  
**VIX:** {data.get('vix', 0):.2f}  
**Market Regime:** {data.get('regime', 'Unknown')}  
**Status:** {data.get('market_status', 'Unknown')}

---
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    except:
        return "❌ Error loading market data"

async def get_performance():
    """Get trading performance"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{API_BASE}/api/analytics/performance")
            data = r.json()
            if data.get("total_trades", 0) == 0:
                return "📊 No trades logged yet. Start tracking your trades!"
            
            return f"""## 📊 Trading Performance

### Overall Statistics
- **Total Trades:** {data['total_trades']}
- **Wins:** {data['wins']} | **Losses:** {data['losses']}
- **Win Rate:** {data['win_rate']}%

### Performance Metrics
- **Average R:R:** {data['avg_rr']}:1
- **Total P&L:** ${data['total_pnl']:,.2f}
- **Best Trade:** ${data['best_trade']:,.2f}
- **Worst Trade:** ${data['worst_trade']:,.2f}
"""
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Build Gradio Interface
with gr.Blocks(title="Legend AI Trading Dashboard", theme=gr.themes.Soft(), css=custom_css) as dashboard:
    gr.Markdown("# 🚀 Legend AI Trading Dashboard")
    gr.Markdown("*Professional Pattern Scanner & Trading Intelligence Platform*")
    
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
    
    with gr.Tab("📈 Market Internals"):
        gr.Markdown("### Real-time market conditions and regime")
        market_btn = gr.Button("🔄 Refresh Market Data", variant="secondary")
        market_output = gr.Markdown()
        market_btn.click(get_market_status, inputs=None, outputs=market_output)
        
        # Auto-load on page load
        dashboard.load(get_market_status, inputs=None, outputs=market_output)
    
    with gr.Tab("📊 Performance"):
        gr.Markdown("### Track your trading performance")
        perf_btn = gr.Button("🔄 Refresh Stats", variant="secondary")
        perf_output = gr.Markdown()
        perf_btn.click(get_performance, inputs=None, outputs=perf_output)
    
    with gr.Tab("ℹ️ About"):
        gr.Markdown("""## About Legend AI

**Legend AI** is a professional trading intelligence platform that helps you:

- 🔍 **Scan thousands of stocks** for Minervini-style pattern setups
- 📊 **Analyze technical patterns** (VCP, Cup & Handle, Flat Base)
- 💼 **Plan trades** with proper position sizing
- 📈 **Track performance** and improve your edge
- 🤖 **Telegram bot** for on-the-go analysis

### Features
- Real-time pattern detection
- S&P 500 & NASDAQ 100 coverage
- Entry/Stop/Target levels
- Risk/Reward analysis
- Market regime detection
- Trading journal & analytics

### API Endpoints
- Pattern Detection: `/api/patterns/detect`
- Universe Scanner: `/api/universe/scan`
- Watchlist: `/api/watchlist`
- Trade Plans: `/api/trade/plan`
- Analytics: `/api/analytics/performance`

**Version:** 1.0.0 | **Status:** Production Ready ✅

[API Documentation](https://legend-ai-python-production.up.railway.app/docs)
""")

if __name__ == "__main__":
    dashboard.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        favicon_path=None
    )

