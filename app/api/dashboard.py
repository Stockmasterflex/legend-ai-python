"""
Simple API-based dashboard endpoints
Returns HTML for browser with working buttons
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["dashboard"])

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Legend AI Trading Dashboard</title>
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
        .tabs {
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
        .result {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
            max-height: 1200px;
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
        .result img {
            max-width: 100%;
            margin-top: 15px;
            border-radius: 6px;
        }
        .result iframe {
            width: 100%;
            height: 500px;
            border: 1px solid #ddd;
            border-radius: 6px;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Legend AI Trading Dashboard</h1>

        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab(event, 'pattern')">📊 Pattern Scanner</button>
            <button class="tab-btn" onclick="switchTab(event, 'universe')">🔍 Universe Scan</button>
            <button class="tab-btn" onclick="switchTab(event, 'watchlist')">📋 Watchlist</button>
            <button class="tab-btn" onclick="switchTab(event, 'market')">📈 Market</button>
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

        function switchTab(evt, tabName) {
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(el => el.classList.remove('active'));

            const btns = document.querySelectorAll('.tab-btn');
            btns.forEach(btn => btn.classList.remove('active'));

            document.getElementById(tabName).classList.add('active');
            if (evt && evt.target) {
                evt.target.classList.add('active');
            }
        }

        function showResult(elementId, text, isError) {
            const el = document.getElementById(elementId);
            el.textContent = text;
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
            resultEl.classList.remove('error', 'success');
            resultEl.innerHTML = '<div style="text-align: center; padding: 20px;">⏳ Analyzing ' + ticker + '...</div>';
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
                    let html = '<h3>' + d.pattern + ' (Score: ' + d.score.toFixed(1) + '/10)</h3>';
                    html += '<p>Entry: $' + d.entry.toFixed(2) + ' | Stop: $' + d.stop.toFixed(2) + ' | Target: $' + d.target.toFixed(2) + '</p>';
                    html += '<p>R:R: ' + d.risk_reward.toFixed(2) + ':1 | Current: $' + d.current_price.toFixed(2) + '</p>';

                    if (d.chart_url) {
                        // Check if it's a TradingView URL (needs iframe) or direct image
                        if (d.chart_url.includes('tradingview')) {
                            html += '<iframe src="' + d.chart_url + '" style="width:100%; height:500px; border: 1px solid #ddd; border-radius: 6px; margin-top: 15px;"></iframe>';
                        } else if (d.chart_url.includes('chart-img')) {
                            // Try as image but fallback to TradingView if it fails
                            html += '<img src="' + d.chart_url + '" alt="Chart" style="max-width: 100%; margin-top: 15px; border-radius: 6px;" onerror="this.parentElement.innerHTML += \'<p style=\\\"color: #999;\\\">Chart image unavailable. <a href=\\\"https://www.tradingview.com/?symbol=' + document.getElementById(\'patternTicker\').value + '\\\" target=\\\"_blank\\\">View on TradingView</a></p>\'">';
                        } else {
                            html += '<img src="' + d.chart_url + '" alt="Chart" style="max-width: 100%; margin-top: 15px; border-radius: 6px;">';
                        }
                    } else {
                        html += '<p style="text-align: center; color: #999; margin-top: 15px;">📊 Chart not available</p>';
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
            showResult('universeResult', '⏳ Scanning... This may take 1-2 minutes', false);

            try {
                const response = await fetch(API_BASE + '/api/universe/scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ min_score: minScore, limit: 20 })
                });

                if (!response.ok) throw new Error('HTTP ' + response.status);
                const data = await response.json();

                if (data.success) {
                    const resultEl = document.getElementById('universeResult');
                    let html = 'Found ' + data.results.length + ' setups:\\n\\n';
                    data.results.forEach((r, i) => {
                        html += (i + 1) + '. ' + r.ticker + ' - ' + r.pattern + ' (Score: ' + r.score.toFixed(1) + '/10)\\n';
                        html += '   Entry: $' + r.entry.toFixed(2) + ' | Stop: $' + r.stop.toFixed(2) + ' | Target: $' + r.target.toFixed(2) + '\\n\\n';
                    });
                    resultEl.textContent = html;
                    resultEl.classList.add('show', 'success');
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
                        msg += '• ' + item.ticker + ' - ' + item.reason + '\\n  Added: ' + item.added_date + '\\n\\n';
                    });
                    const resultEl = document.getElementById('watchlistResult');
                    resultEl.textContent = msg;
                    resultEl.classList.add('show', 'success');
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
                    const msg = 'SPY Price: $' + m.spy_price.toFixed(2) + '\\n' +
                               '50 SMA: $' + m.sma_50.toFixed(2) + '\\n' +
                               '200 SMA: $' + m.sma_200.toFixed(2) + '\\n' +
                               'Market Regime: ' + m.regime + '\\n' +
                               'Status: ' + m.status;
                    const resultEl = document.getElementById('marketResult');
                    resultEl.textContent = msg;
                    resultEl.classList.add('show', 'success');
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

@router.get("/test")
async def dashboard_test():
    """Simple test dashboard to verify buttons work"""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Legend AI - Test Dashboard</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        button { padding: 10px 20px; margin: 5px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #764ba2; }
        .result { margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 4px; min-height: 100px; font-family: monospace; }
        .loading { color: #667eea; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Legend AI - Test Dashboard</h1>

        <h2>Test Pattern Detection</h2>
        <button onclick="testPatternAPI()">Test Pattern Detection</button>

        <h2>Test Universe Scan</h2>
        <button onclick="testUniverseAPI()">Test Universe Scan</button>

        <h2>Test Market Data</h2>
        <button onclick="testMarketAPI()">Test Market Data</button>

        <div id="result" class="result">Click a button to test...</div>
    </div>

    <script>
        const API_BASE = window.location.protocol + '//' + window.location.host;

        function setResult(text, className = '') {
            const el = document.getElementById('result');
            el.innerHTML = '<pre>' + text + '</pre>';
            el.className = 'result ' + className;
        }

        async function testPatternAPI() {
            setResult('Loading...', 'loading');
            try {
                const response = await fetch(API_BASE + '/api/patterns/detect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ticker: 'AAPL', interval: '1day' })
                });
                const data = await response.json();
                setResult(JSON.stringify(data, null, 2), data.success ? 'success' : 'error');
            } catch (e) {
                setResult('Error: ' + e.message, 'error');
            }
        }

        async function testUniverseAPI() {
            setResult('Loading...', 'loading');
            try {
                const response = await fetch(API_BASE + '/api/universe/scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ min_score: 7.0, limit: 5 })
                });
                const data = await response.json();
                setResult(JSON.stringify(data, null, 2), data.success ? 'success' : 'error');
            } catch (e) {
                setResult('Error: ' + e.message, 'error');
            }
        }

        async function testMarketAPI() {
            setResult('Loading...', 'loading');
            try {
                const response = await fetch(API_BASE + '/api/market/internals');
                const data = await response.json();
                setResult(JSON.stringify(data, null, 2), data.success ? 'success' : 'error');
            } catch (e) {
                setResult('Error: ' + e.message, 'error');
            }
        }
    </script>
</body>
</html>"""
    return HTMLResponse(html)
