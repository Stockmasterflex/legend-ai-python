"""
Simple API-based dashboard endpoints (no Gradio queue issues)
Returns HTML for browser or JSON for API clients
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["dashboard"])

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Legend AI Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 32px;
        }
        .tab-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .tab-btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .tab-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        .tab-btn.active {
            background: white;
            color: #667eea;
            font-weight: 600;
        }
        .tab-content {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            display: none;
        }
        .tab-content.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .tab-content h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 24px;
        }
        .form-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            align-items: center;
        }
        input, select {
            padding: 10px 15px;
            border: 2px solid #667eea;
            border-radius: 6px;
            font-size: 14px;
            font-family: inherit;
        }
        button {
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        button:hover {
            background: #764ba2;
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(0);
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .result {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            max-height: 500px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-break: break-word;
            border-left: 4px solid #667eea;
            display: none;
        }
        .result.show { display: block; }
        .result.error {
            color: #d32f2f;
            background: #ffebee;
            border-left-color: #d32f2f;
        }
        .result.success {
            color: #388e3c;
            background: #e8f5e9;
            border-left-color: #388e3c;
        }
        label {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 500;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Legend AI Trading Dashboard</h1>

        <div class="tab-buttons">
            <button class="tab-btn active" onclick="showTab('pattern')">📊 Pattern Scanner</button>
            <button class="tab-btn" onclick="showTab('universe')">🔍 Universe Scan</button>
            <button class="tab-btn" onclick="showTab('watchlist')">📋 Watchlist</button>
            <button class="tab-btn" onclick="showTab('market')">📈 Market</button>
        </div>

        <!-- Pattern Scanner Tab -->
        <div id="pattern" class="tab-content active">
            <h2>📊 Pattern Analysis</h2>
            <div class="form-group">
                <input type="text" id="patternTicker" placeholder="Ticker (e.g., NVDA)" value="NVDA">
                <select id="patternInterval">
                    <option value="1day">Daily</option>
                    <option value="1week">Weekly</option>
                </select>
                <button onclick="analyzePattern()">Analyze Pattern</button>
            </div>
            <div id="patternResult" class="result"></div>
        </div>

        <!-- Universe Scan Tab -->
        <div id="universe" class="tab-content">
            <h2>🔍 Universe Scan</h2>
            <div class="form-group">
                <label>Min Score: <input type="number" id="scanMinScore" min="6" max="10" value="7" style="width: 80px;"></label>
                <button onclick="scanUniverse()">Run Scan</button>
            </div>
            <div id="universeResult" class="result"></div>
        </div>

        <!-- Watchlist Tab -->
        <div id="watchlist" class="tab-content">
            <h2>📋 Watchlist</h2>
            <div class="form-group">
                <input type="text" id="watchTicker" placeholder="Ticker" style="width: 150px;">
                <input type="text" id="watchReason" placeholder="Reason" style="width: 200px;">
                <button onclick="addToWatchlist()">Add to Watchlist</button>
            </div>
            <div class="form-group">
                <button onclick="refreshWatchlist()" style="background: #764ba2;">Refresh Watchlist</button>
            </div>
            <div id="watchlistResult" class="result"></div>
        </div>

        <!-- Market Tab -->
        <div id="market" class="tab-content">
            <h2>📈 Market Internals</h2>
            <div class="form-group">
                <button onclick="getMarketData()">Get Market Data</button>
            </div>
            <div id="marketResult" class="result"></div>
        </div>
    </div>

    <script>
        const API_BASE = window.location.protocol + '//' + window.location.host;

        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        function showResult(elementId, message, isError = false) {
            const el = document.getElementById(elementId);
            el.textContent = message;
            el.classList.add('show');
            el.classList.toggle('error', isError);
            el.classList.toggle('success', !isError);
        }

        async function analyzePattern() {
            const ticker = document.getElementById('patternTicker').value.toUpperCase();
            const interval = document.getElementById('patternInterval').value;

            if (!ticker) {
                showResult('patternResult', 'Please enter a ticker', true);
                return;
            }

            const resultEl = document.getElementById('patternResult');
            resultEl.classList.remove('show', 'error', 'success');
            resultEl.innerHTML = '<div style="text-align: center;">⏳ Analyzing ' + ticker + '...<br>(Generating chart...)</div>';
            resultEl.classList.add('show');

            try {
                const response = await fetch(API_BASE + '/api/patterns/detect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ticker, interval })
                });

                if (!response.ok) throw new Error('HTTP ' + response.status);
                const data = await response.json();

                if (data.success) {
                    const d = data.data;

                    // Format score with color
                    const scoreColor = d.score >= 8 ? '#388e3c' : d.score >= 6 ? '#ff9800' : '#d32f2f';
                    const scoreEmoji = d.score >= 8 ? '✅' : d.score >= 6 ? '⚠️' : '❌';

                    // Build formatted HTML result
                    let html = `
                    <div style="background: #f5f5f5; padding: 15px; border-radius: 6px; margin-bottom: 15px;">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">
                            ${scoreEmoji} ${d.pattern} <span style="color: ${scoreColor}; font-size: 16px;">${d.score.toFixed(1)}/10</span>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px;">
                            <div>📍 Entry: <strong>$${d.entry.toFixed(2)}</strong></div>
                            <div>🎯 Target: <strong>$${d.target.toFixed(2)}</strong></div>
                            <div>🛑 Stop: <strong>$${d.stop.toFixed(2)}</strong></div>
                            <div>📊 R:R: <strong>${d.risk_reward.toFixed(2)}:1</strong></div>
                            <div>💰 Current: <strong>$${d.current_price.toFixed(2)}</strong></div>
                            <div>⭐ RS: <strong>${d.rs_rating ? d.rs_rating.toFixed(0) : 'N/A'}</strong></div>
                        </div>
                    </div>`;

                    // Add chart if available
                    if (d.chart_url) {
                        html += '<img src="' + d.chart_url + '" style="max-width: 100%; margin-top: 15px; border-radius: 6px; border: 2px solid #667eea;" onerror="this.style.display=\'none\';">';
                    } else {
                        html += '<div style="text-align: center; color: #999; padding: 20px;">📊 Chart not available</div>';
                    }

                    resultEl.innerHTML = html;
                    resultEl.classList.add('success');
                } else {
                    showResult('patternResult', 'Error: ' + (data.detail || 'Analysis failed'), true);
                }
            } catch (error) {
                showResult('patternResult', 'Error: ' + error.message, true);
            }
        }

        async function scanUniverse() {
            const minScore = parseFloat(document.getElementById('scanMinScore').value);
            showResult('universeResult', '⏳ Scanning ' + minScore + '+ patterns... (1-2 minutes)', false);

            try {
                const response = await fetch(API_BASE + '/api/universe/scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ min_score: minScore, limit: 20 })
                });

                if (!response.ok) throw new Error('HTTP ' + response.status);
                const data = await response.json();

                if (data.success && data.results.length > 0) {
                    const resultEl = document.getElementById('universeResult');
                    let html = `<div style="margin-bottom: 15px; font-weight: bold;">Found <span style="color: #388e3c;">${data.results.length}</span> high-quality setups:</div>`;

                    data.results.forEach((r, i) => {
                        const scoreColor = r.score >= 8 ? '#388e3c' : r.score >= 6 ? '#ff9800' : '#d32f2f';
                        html += `
                        <div style="background: #f5f5f5; padding: 12px; border-radius: 6px; margin-bottom: 10px; border-left: 4px solid ${scoreColor};">
                            <div style="font-weight: bold; margin-bottom: 5px;">
                                ${i + 1}. ${r.ticker} - ${r.pattern} <span style="color: ${scoreColor}; font-weight: bold;">${r.score.toFixed(1)}/10</span>
                            </div>
                            <div style="font-size: 13px;">
                                📍 Entry: $${r.entry.toFixed(2)} | 🛑 Stop: $${r.stop.toFixed(2)} | 🎯 Target: $${r.target.toFixed(2)}
                            </div>
                        </div>`;
                    });

                    resultEl.innerHTML = html;
                    resultEl.classList.remove('error');
                    resultEl.classList.add('success');
                } else if (data.success) {
                    showResult('universeResult', '🔍 No setups found matching score ' + minScore + '+', false);
                } else {
                    showResult('universeResult', 'Error: ' + (data.detail || 'Scan failed'), true);
                }
            } catch (error) {
                showResult('universeResult', 'Error: ' + error.message, true);
            }
        }

        async function addToWatchlist() {
            const ticker = document.getElementById('watchTicker').value.toUpperCase();
            const reason = document.getElementById('watchReason').value;

            if (!ticker) {
                showResult('watchlistResult', 'Please enter a ticker', true);
                return;
            }

            showResult('watchlistResult', 'Adding...', false);

            try {
                const response = await fetch(API_BASE + '/api/watchlist/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ticker, reason: reason || 'Monitoring' })
                });

                if (!response.ok) throw new Error('HTTP ' + response.status);
                const data = await response.json();

                if (data.success) {
                    showResult('watchlistResult', 'Added ' + ticker + ' to watchlist!', false);
                    document.getElementById('watchTicker').value = '';
                    document.getElementById('watchReason').value = '';
                } else {
                    showResult('watchlistResult', 'Error: ' + (data.detail || 'Failed to add'), true);
                }
            } catch (error) {
                showResult('watchlistResult', 'Error: ' + error.message, true);
            }
        }

        async function refreshWatchlist() {
            showResult('watchlistResult', 'Loading...', false);

            try {
                const response = await fetch(API_BASE + '/api/watchlist');
                if (!response.ok) throw new Error('HTTP ' + response.status);
                const data = await response.json();

                if (data.success && data.items && data.items.length > 0) {
                    let msg = 'Your Watchlist (' + data.items.length + ' stocks):\\n\\n';
                    data.items.forEach(item => {
                        msg += `• ${item.ticker} - ${item.reason}\\n  Added: ${item.added_date}\\n\\n`;
                    });
                    showResult('watchlistResult', msg, false);
                } else {
                    showResult('watchlistResult', 'Watchlist is empty', false);
                }
            } catch (error) {
                showResult('watchlistResult', 'Error: ' + error.message, true);
            }
        }

        async function getMarketData() {
            showResult('marketResult', 'Loading...', false);

            try {
                const response = await fetch(API_BASE + '/api/market/internals');
                if (!response.ok) throw new Error('HTTP ' + response.status);
                const data = await response.json();

                if (data.success) {
                    const m = data.data;
                    const msg = `SPY Price: $${m.spy_price.toFixed(2)}
50 SMA: $${m.sma_50.toFixed(2)}
200 SMA: $${m.sma_200.toFixed(2)}
Market Regime: ${m.regime}
Status: ${m.status}`;
                    showResult('marketResult', msg, false);
                } else {
                    showResult('marketResult', 'Error: ' + (data.detail || 'Failed to fetch'), true);
                }
            } catch (error) {
                showResult('marketResult', 'Error: ' + error.message, true);
            }
        }
    </script>
</body>
</html>"""

@router.get("/")
async def dashboard():
    """Serve the dashboard HTML"""
    return HTMLResponse(HTML_DASHBOARD)
