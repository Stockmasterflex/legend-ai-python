"""
Simple API-based dashboard endpoints (no Gradio queue issues)
Returns HTML for browser or JSON for API clients
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
import os

router = APIRouter(tags=["dashboard"])

# Auto-detect API_BASE - on production it should use same domain
API_BASE = os.getenv("API_BASE", "http://localhost:8000")

HTML_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <title>Legend AI Trading Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: white; margin-bottom: 30px; text-align: center; }}
        .tabs {{ display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
        .tab-btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            background: rgba(255,255,255,0.2);
            color: white;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s;
        }}
        .tab-btn.active {{
            background: white;
            color: #667eea;
            font-weight: 600;
        }}
        .tab-btn:hover {{ background: rgba(255,255,255,0.3); }}
        .tab-content {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: none;
        }}
        .tab-content.active {{ display: block; }}
        .form-group {{
            margin-bottom: 20px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }}
        input, select {{
            padding: 10px 15px;
            border: 2px solid #667eea;
            border-radius: 6px;
            font-size: 14px;
        }}
        button {{
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: background 0.3s;
        }}
        button:hover {{ background: #764ba2; }}
        button:disabled {{
            background: #ccc;
            cursor: not-allowed;
        }}
        .result {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            white-space: pre-wrap;
            font-family: monospace;
            max-height: 500px;
            overflow-y: auto;
        }}
        .result.error {{ color: #d32f2f; background: #ffebee; }}
        .result.success {{ color: #388e3c; background: #e8f5e9; }}
        .loading {{
            text-align: center;
            color: #667eea;
            font-weight: 600;
        }}
        .spinner {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #667eea;
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Legend AI Trading Dashboard</h1>

        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('pattern')">Pattern Scanner</button>
            <button class="tab-btn" onclick="switchTab('universe')">Universe Scan</button>
            <button class="tab-btn" onclick="switchTab('watchlist')">Watchlist</button>
            <button class="tab-btn" onclick="switchTab('market')">Market</button>
        </div>

        <!-- Pattern Scanner Tab -->
        <div id="pattern" class="tab-content active">
            <h2>📊 Pattern Analysis</h2>
            <div class="form-group">
                <input type="text" id="patternTicker" placeholder="Ticker (e.g., NVDA)" value="NVDA" style="width: 150px;">
                <select id="patternInterval" style="width: 150px;">
                    <option value="1day">Daily</option>
                    <option value="1week">Weekly</option>
                </select>
                <button onclick="analyzePattern()" id="patternBtn">Analyze</button>
            </div>
            <div id="patternResult" class="result" style="display: none;"></div>
        </div>

        <!-- Universe Scan Tab -->
        <div id="universe" class="tab-content">
            <h2>🔍 Universe Scan</h2>
            <div class="form-group">
                <label>Min Score:
                    <input type="number" id="scanMinScore" min="6" max="10" value="7" style="width: 100px;">
                </label>
                <button onclick="scanUniverse()" id="universeBtn">Run Scan</button>
            </div>
            <div id="universeResult" class="result" style="display: none;"></div>
        </div>

        <!-- Watchlist Tab -->
        <div id="watchlist" class="tab-content">
            <h2>📋 Watchlist</h2>
            <div class="form-group">
                <input type="text" id="watchTicker" placeholder="Ticker" style="width: 150px;">
                <input type="text" id="watchReason" placeholder="Reason" style="width: 150px;">
                <button onclick="addToWatchlist()" id="addBtn">Add</button>
                <button onclick="refreshWatchlist()" style="background: #764ba2;">Refresh</button>
            </div>
            <div id="watchlistResult" class="result" style="display: none;"></div>
        </div>

        <!-- Market Tab -->
        <div id="market" class="tab-content">
            <h2>📈 Market Internals</h2>
            <div class="form-group">
                <button onclick="getMarketData()" id="marketBtn">Get Market Data</button>
            </div>
            <div id="marketResult" class="result" style="display: none;"></div>
        </div>
    </div>

    <script>
        // Auto-detect API base from current URL
        // If on https://example.com/dashboard/, API should be https://example.com
        const API_BASE = window.location.protocol + '//' + window.location.host;

        function switchTab(tabName) {{
            document.querySelectorAll('.tab-content').forEach(e => e.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(e => e.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}

        async function analyzePattern() {{
            const ticker = document.getElementById('patternTicker').value;
            const interval = document.getElementById('patternInterval').value;
            const result = document.getElementById('patternResult');
            const btn = document.getElementById('patternBtn');

            if (!ticker) {{ alert('Please enter a ticker'); return; }}

            btn.disabled = true;
            result.style.display = 'block';
            result.textContent = '⏳ Analyzing...';
            result.classList.remove('error', 'success');

            try {{
                const response = await fetch(API_BASE + '/api/patterns/detect', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{ticker: ticker.toUpperCase(), interval}})
                }});
                const data = await response.json();

                if (data.success) {{
                    const d = data.data;
                    result.textContent = `Pattern: ${{d.pattern}}
Score: ${{d.score}}/10
Entry: $${{d.entry.toFixed(2)}}
Stop: $${{d.stop.toFixed(2)}}
Target: $${{d.target.toFixed(2)}}
R:R Ratio: ${{d.risk_reward.toFixed(2)}}:1
Current: $${{d.current_price.toFixed(2)}}
RS Rating: ${{d.rs_rating.toFixed(0)}}`;
                    result.classList.add('success');
                }} else {{
                    result.textContent = '❌ Error: ' + (data.detail || 'Could not analyze');
                    result.classList.add('error');
                }}
            }} catch (e) {{
                result.textContent = '❌ Error: ' + e.message;
                result.classList.add('error');
            }}
            btn.disabled = false;
        }}

        async function scanUniverse() {{
            const minScore = parseFloat(document.getElementById('scanMinScore').value);
            const result = document.getElementById('universeResult');
            const btn = document.getElementById('universeBtn');

            btn.disabled = true;
            result.style.display = 'block';
            result.textContent = '⏳ Scanning... (this may take 1-2 minutes)';
            result.classList.remove('error', 'success');

            try {{
                const response = await fetch(API_BASE + '/api/universe/scan', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{min_score: minScore, limit: 20}})
                }});
                const data = await response.json();

                if (data.success) {{
                    let text = `Found ${{data.results.length}} setups:\\n\\n`;
                    data.results.forEach((r, i) => {{
                        text += `${{i+1}}. ${{r.ticker}} - ${{r.pattern}} (Score: ${{r.score}}/10)
   Entry: $${{r.entry.toFixed(2)}} | Stop: $${{r.stop.toFixed(2)}} | R:R: ${{r.risk_reward.toFixed(1)}}:1\\n\\n`;
                    }});
                    result.textContent = text;
                    result.classList.add('success');
                }} else {{
                    result.textContent = '❌ Error: ' + (data.detail || 'Scan failed');
                    result.classList.add('error');
                }}
            }} catch (e) {{
                result.textContent = '❌ Error: ' + e.message;
                result.classList.add('error');
            }}
            btn.disabled = false;
        }}

        async function addToWatchlist() {{
            const ticker = document.getElementById('watchTicker').value;
            const reason = document.getElementById('watchReason').value;
            const result = document.getElementById('watchlistResult');
            const btn = document.getElementById('addBtn');

            if (!ticker) {{ alert('Please enter a ticker'); return; }}

            btn.disabled = true;
            result.style.display = 'block';
            result.textContent = '⏳ Adding...';
            result.classList.remove('error', 'success');

            try {{
                const response = await fetch(API_BASE + '/api/watchlist/add', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{ticker: ticker.toUpperCase(), reason: reason || 'Monitoring'}})
                }});
                const data = await response.json();

                if (data.success) {{
                    result.textContent = `✅ Added ${{ticker.toUpperCase()}} to watchlist!`;
                    result.classList.add('success');
                    document.getElementById('watchTicker').value = '';
                    document.getElementById('watchReason').value = '';
                }} else {{
                    result.textContent = '❌ Error: ' + (data.detail || 'Failed to add');
                    result.classList.add('error');
                }}
            }} catch (e) {{
                result.textContent = '❌ Error: ' + e.message;
                result.classList.add('error');
            }}
            btn.disabled = false;
        }}

        async function refreshWatchlist() {{
            const result = document.getElementById('watchlistResult');
            result.style.display = 'block';
            result.textContent = '⏳ Loading...';
            result.classList.remove('error', 'success');

            try {{
                const response = await fetch(API_BASE + '/api/watchlist');
                const data = await response.json();

                if (data.success && data.items.length > 0) {{
                    let text = `Your Watchlist (${{data.items.length}} stocks):\\n\\n`;
                    data.items.forEach(item => {{
                        text += `• ${{item.ticker}} - ${{item.reason}}\\n  Added: ${{item.added_date}}\\n\\n`;
                    }});
                    result.textContent = text;
                    result.classList.add('success');
                }} else {{
                    result.textContent = '📝 Watchlist is empty';
                    result.classList.add('success');
                }}
            }} catch (e) {{
                result.textContent = '❌ Error: ' + e.message;
                result.classList.add('error');
            }}
        }}

        async function getMarketData() {{
            const result = document.getElementById('marketResult');
            const btn = document.getElementById('marketBtn');

            btn.disabled = true;
            result.style.display = 'block';
            result.textContent = '⏳ Loading...';
            result.classList.remove('error', 'success');

            try {{
                const response = await fetch(API_BASE + '/api/market/internals');
                const data = await response.json();

                if (data.success) {{
                    const m = data.data;
                    result.textContent = `SPY: $${{m.spy_price.toFixed(2)}}
50 SMA: $${{m.sma_50.toFixed(2)}}
200 SMA: $${{m.sma_200.toFixed(2)}}
Regime: ${{m.regime}}
Status: ${{m.status}}`;
                    result.classList.add('success');
                }} else {{
                    result.textContent = '❌ Error: ' + (data.detail || 'Failed');
                    result.classList.add('error');
                }}
            }} catch (e) {{
                result.textContent = '❌ Error: ' + e.message;
                result.classList.add('error');
            }}
            btn.disabled = false;
        }}
    </script>
</body>
</html>
"""

@router.get("/")
async def dashboard():
    """Serve the dashboard HTML"""
    return HTMLResponse(HTML_DASHBOARD)
