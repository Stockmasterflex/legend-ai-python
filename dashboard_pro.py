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

            if r.status_code == 422:
                return f"❌ Invalid input. Please check ticker symbol and interval.", ""
            elif r.status_code != 200:
                return f"❌ API Error: HTTP {r.status_code}\n\nCheck API health at {API_BASE}/health", ""

            data = r.json()
            if data.get("success"):
                d = data["data"]
                chart_url = data.get("chart_url") or d.get("chart_url", "")
                return f"""# {ticker} Pattern Analysis

**Pattern:** {d.get('pattern', 'No Pattern')}
**Score:** {d.get('score', 0)}/10
**Entry:** ${d.get('entry', 0):.2f}
**Stop:** ${d.get('stop', 0):.2f}
**Target:** ${d.get('target', 0):.2f}
**Risk/Reward:** {d.get('risk_reward', 0):.2f}

_Data Source: {d.get('source', 'Unknown')}_
_RS Rating: {d.get('rs_rating', 'N/A')}_
""", chart_url
            else:
                return f"❌ {data.get('detail', 'Could not analyze pattern')}", ""
    except asyncio.TimeoutError:
        return "❌ Request timed out (60s). Try again or use a shorter interval.", ""
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}\n\nCheck that the API is running at {API_BASE}", ""
    except Exception as e:
        return f"❌ Error: {str(e)}", ""

async def scan_universe(min_score):
    """Scan universe for setups with timeout"""
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(
                f"{API_BASE}/api/universe/scan",
                json={"min_score": min_score, "max_results": 20}  # Fixed: use 'max_results' not 'limit'
            )

            if r.status_code != 200:
                return f"❌ Scan failed: HTTP {r.status_code}\n\nPlease try again or check API health at {API_BASE}/health"

            data = r.json()
            if data.get("success"):
                results = data.get("results", [])
                cached = data.get("cached", False)
                scan_time = data.get("scan_time", 0)

                if results and len(results) > 0:
                    cache_note = " (cached)" if cached else f" (scan took {scan_time}s)"
                    text = f"# Universe Scan Results{cache_note}\n\n"
                    text += f"**Found {len(results)} setups** with score >= {min_score}\n\n"
                    for item in results[:15]:
                        emoji = "🔥" if item['score'] >= 8 else "⭐"
                        text += f"{emoji} **{item['ticker']}** - {item['pattern']} ({item['score']}/10)\n"
                        text += f"   Entry: ${item['entry']:.2f} | Stop: ${item['stop']:.2f} | R:R: {item['risk_reward']:.1f}:1\n\n"
                    return text
                else:
                    return f"📊 No setups found with score >= {min_score}\n\nTry lowering the minimum score or check back later."
            return f"❌ {data.get('detail', 'Scan failed')}"
    except asyncio.TimeoutError:
        return "❌ Scan timed out (120s) - too many stocks or slow APIs"
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}\n\nCheck that the API is running at {API_BASE}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

async def get_watchlist():
    """Get watchlist with error handling"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{API_BASE}/api/watchlist")

            if r.status_code != 200:
                return f"❌ Error: HTTP {r.status_code}\n\nCheck API health at {API_BASE}/health"

            data = r.json()
            if data.get("success"):
                items = data.get("items", [])
                if items and len(items) > 0:
                    text = f"# Your Watchlist ({len(items)} stocks)\n\n"
                    for item in items:
                        ticker = item.get('ticker', 'UNKNOWN')
                        reason = item.get('reason', 'N/A')
                        added = item.get('added_date', 'Unknown')
                        if isinstance(added, str) and len(added) >= 10:
                            added = added[:10]
                        text += f"• **{ticker}**\n"
                        text += f"  Reason: {reason}\n"
                        text += f"  Added: {added}\n\n"
                    return text
                return "📝 Watchlist is empty\n\nAdd stocks using the form above."
            return "❌ Could not fetch watchlist"
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}\n\nCheck that the API is running at {API_BASE}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

async def add_watchlist(ticker, reason):
    """Add to watchlist with error handling"""
    try:
        if not ticker or ticker.strip() == "":
            return "❌ Please enter a ticker symbol"

        ticker = ticker.upper().strip()

        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                f"{API_BASE}/api/watchlist/add",
                json={"ticker": ticker, "reason": reason or "Monitoring"}
            )

            if r.status_code == 422:
                return f"❌ Invalid ticker symbol: {ticker}"
            elif r.status_code == 409:
                return f"⚠️ **{ticker}** is already in your watchlist"
            elif r.status_code != 200:
                return f"❌ Error: HTTP {r.status_code}\n\nCheck API health at {API_BASE}/health"

            data = r.json()
            if data.get("success"):
                return f"✅ Added **{ticker}** to watchlist!\n\n_Reason: {reason or 'Monitoring'}_"
            else:
                return f"❌ {data.get('detail', 'Could not add to watchlist')}"
    except httpx.RequestError as e:
        return f"❌ Network error: {str(e)}\n\nCheck that the API is running at {API_BASE}"
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

