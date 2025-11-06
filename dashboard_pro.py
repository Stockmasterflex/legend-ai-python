import gradio as gr
import httpx
import json
import os
import asyncio

# Use environment variable or default to localhost
API_BASE = os.getenv("API_BASE", "http://localhost:8000")

async def scan_pattern(ticker, interval):
    """Analyze a stock pattern with timeout"""
    try:
        if not ticker:
            return "❌ Please enter a ticker", ""

        ticker = ticker.upper().strip()

        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                f"{API_BASE}/api/patterns/detect",
                json={"ticker": ticker, "interval": interval}
            )

            if r.status_code != 200:
                return f"❌ API Error: {r.status_code}", ""

            data = r.json()
            if data.get("success"):
                d = data["data"]
                return f"""# {ticker} Pattern Analysis

**Pattern:** {d.get('pattern')}
**Score:** {d.get('score')}/10
**Entry:** ${d.get('entry', 0):.2f}
**Stop:** ${d.get('stop', 0):.2f}
**Target:** ${d.get('target', 0):.2f}
**Risk/Reward:** {d.get('risk_reward', 0):.2f}

_Data Source: {d.get('source', 'Unknown')}_
""", data.get("chart_url", "")
            else:
                return f"❌ {data.get('detail', 'Could not analyze pattern')}", ""
    except asyncio.TimeoutError:
        return "❌ Request timed out (60s)", ""
    except Exception as e:
        return f"❌ Error: {str(e)}", ""

async def scan_universe(min_score):
    """Scan universe for setups with timeout"""
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(
                f"{API_BASE}/api/universe/scan",
                json={"min_score": min_score, "limit": 20}
            )

            if r.status_code != 200:
                return f"❌ Scan failed: {r.status_code}"

            data = r.json()
            if data.get("success"):
                results = data.get("results", [])
                if results:
                    text = f"# Universe Scan Results ({len(results)} setups)\n\n"
                    for item in results[:15]:
                        emoji = "🔥" if item['score'] >= 8 else "⭐"
                        text += f"{emoji} **{item['ticker']}** - {item['pattern']} ({item['score']}/10)\n"
                        text += f"   Entry: ${item['entry']:.2f} | Stop: ${item['stop']:.2f} | R:R: {item['risk_reward']:.1f}:1\n\n"
                    return text
                return "📊 No results found"
            return f"❌ {data.get('detail', 'Scan failed')}"
    except asyncio.TimeoutError:
        return "❌ Scan timed out (120s) - too many stocks or slow APIs"
    except Exception as e:
        return f"❌ Error: {str(e)}"

async def get_watchlist():
    """Get watchlist with error handling"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{API_BASE}/api/watchlist")

            if r.status_code != 200:
                return f"❌ Error: {r.status_code}"

            data = r.json()
            if data.get("success"):
                items = data.get("items", [])
                if items:
                    text = f"# Your Watchlist ({len(items)} stocks)\n\n"
                    for item in items:
                        text += f"• **{item['ticker']}**\n"
                        text += f"  Reason: {item.get('reason', 'N/A')}\n"
                        text += f"  Added: {item.get('added_date', 'Unknown')[:10]}\n\n"
                    return text
                return "📝 Watchlist is empty"
            return "❌ Could not fetch watchlist"
    except Exception as e:
        return f"❌ Error: {str(e)}"

async def add_watchlist(ticker, reason):
    """Add to watchlist with error handling"""
    try:
        if not ticker:
            return "❌ Please enter a ticker"

        ticker = ticker.upper().strip()

        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                f"{API_BASE}/api/watchlist/add",
                json={"ticker": ticker, "reason": reason or "Monitoring"}
            )

            if r.status_code != 200:
                return f"❌ Error: {r.status_code}"

            data = r.json()
            if data.get("success"):
                return f"✅ Added **{ticker}** to watchlist!\n\n_Reason: {reason or 'Monitoring'}_"
            else:
                return f"❌ {data.get('detail', 'Could not add to watchlist')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

with gr.Blocks(title="Legend AI Trading Dashboard", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🚀 Legend AI Trading Dashboard")
    
    with gr.Tab("Pattern Scanner"):
        with gr.Row():
            ticker_input = gr.Textbox(label="Ticker", value="AAPL")
            interval_input = gr.Dropdown(["1day", "1week"], value="1day", label="Interval")
        scan_btn = gr.Button("Analyze Pattern", variant="primary")
        pattern_output = gr.Markdown()
        scan_btn.click(scan_pattern, [ticker_input, interval_input], pattern_output)
    
    with gr.Tab("Universe Scanner"):
        gr.Markdown("Scan S&P 500 & NASDAQ 100 for top setups")
        min_score_input = gr.Slider(6, 10, value=7, label="Min Score")
        universe_scan_btn = gr.Button("Run Quick Scan", variant="primary")
        universe_output = gr.Markdown()
        universe_scan_btn.click(scan_universe, min_score_input, universe_output)
    
    with gr.Tab("Watchlist"):
        with gr.Row():
            wl_ticker = gr.Textbox(label="Ticker")
            wl_reason = gr.Textbox(label="Reason")
        add_wl_btn = gr.Button("Add to Watchlist")
        wl_output = gr.Markdown()
        add_wl_btn.click(add_watchlist, [wl_ticker, wl_reason], wl_output)
        
        refresh_wl_btn = gr.Button("Refresh Watchlist")
        watchlist_display = gr.Markdown()
        refresh_wl_btn.click(get_watchlist, None, watchlist_display)

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)

