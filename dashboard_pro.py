import gradio as gr
import httpx
import json

API_BASE = "http://localhost:8000"

async def scan_pattern(ticker, interval):
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{API_BASE}/api/patterns/detect", json={"ticker": ticker, "interval": interval})
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
""", data.get("chart_url", "")
        return "Error analyzing pattern", ""

async def scan_universe(min_score):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{API_BASE}/api/universe/scan/quick")
        data = r.json()
        if data.get("success"):
            results = data.get("results", [])
            if results:
                text = "# Universe Scan Results\n\n"
                for item in results[:10]:
                    text += f"**{item['ticker']}** - {item['pattern']} ({item['score']}/10)\n"
                    text += f"Entry: ${item['entry']:.2f} | Stop: ${item['stop']:.2f}\n\n"
                return text
        return "No results found"

async def get_watchlist():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/api/watchlist")
        data = r.json()
        if data.get("success"):
            items = data.get("items", [])
            if items:
                text = "# Watchlist\n\n"
                for item in items:
                    text += f"**{item['ticker']}** - {item.get('status', 'Watching')}\n"
                    text += f"Reason: {item.get('reason', 'N/A')}\n\n"
                return text
        return "Watchlist empty"

async def add_watchlist(ticker, reason):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_BASE}/api/watchlist/add", json={"ticker": ticker, "reason": reason})
        return f"✅ Added {ticker} to watchlist"

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

