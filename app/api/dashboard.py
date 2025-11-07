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
        /* Dark Cyberpunk AI Trading Theme */
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 50%, #0a0e27 100%);
            min-height: 100vh;
            padding: 20px;
            color: #e0e0e0;
            overflow-x: hidden;
            position: relative;
        }

        /* Animated background elements */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background:
                radial-gradient(circle at 20% 50%, rgba(0, 255, 200, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 0, 150, 0.03) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }

        h1 {
            background: linear-gradient(135deg, #00ffcc 0%, #ff00ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 10px;
            font-size: 42px;
            font-weight: 800;
            letter-spacing: 1px;
            text-shadow: 0 0 20px rgba(0, 255, 200, 0.3);
        }

        .subtitle {
            text-align: center;
            color: #00ffcc;
            font-size: 14px;
            margin-bottom: 40px;
            letter-spacing: 2px;
            text-transform: uppercase;
            opacity: 0.8;
        }

        .tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            justify-content: center;
            padding: 8px;
            background: rgba(20, 20, 50, 0.5);
            border-radius: 12px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 200, 0.1);
        }

        .tab-btn {
            padding: 12px 24px;
            border: 2px solid rgba(0, 255, 200, 0.3);
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.4);
            color: #00ffcc;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }

        .tab-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 200, 0.2), transparent);
            transition: left 0.5s ease;
        }

        .tab-btn:hover {
            border-color: rgba(0, 255, 200, 0.8);
            background: rgba(0, 255, 200, 0.05);
            box-shadow: 0 0 20px rgba(0, 255, 200, 0.3);
            transform: translateY(-2px);
        }

        .tab-btn:hover::before {
            left: 100%;
        }

        .tab-btn.active {
            background: linear-gradient(135deg, rgba(0, 255, 200, 0.2) 0%, rgba(255, 0, 150, 0.2) 100%);
            border-color: #00ffcc;
            box-shadow: 0 0 30px rgba(0, 255, 200, 0.5), inset 0 0 20px rgba(0, 255, 200, 0.1);
            color: #00ffcc;
        }

        .tab-content {
            background: rgba(15, 20, 50, 0.7);
            border-radius: 12px;
            padding: 35px;
            box-shadow: 0 0 40px rgba(0, 255, 200, 0.1), inset 0 0 40px rgba(0, 0, 0, 0.3);
            display: none;
            border: 1px solid rgba(0, 255, 200, 0.2);
            backdrop-filter: blur(20px);
            animation: fadeIn 0.3s ease;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .tab-content h2 {
            background: linear-gradient(135deg, #00ffcc 0%, #00aaff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 25px;
            font-size: 28px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .form-group {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            align-items: center;
        }

        input, select {
            padding: 12px 15px;
            border: 2px solid rgba(0, 255, 200, 0.3);
            border-radius: 6px;
            font-size: 14px;
            font-family: inherit;
            background: rgba(0, 0, 0, 0.3);
            color: #e0e0e0;
            transition: all 0.3s ease;
        }

        input::placeholder {
            color: rgba(224, 224, 224, 0.5);
        }

        input:focus, select:focus {
            outline: none;
            border-color: #00ffcc;
            box-shadow: 0 0 15px rgba(0, 255, 200, 0.3), inset 0 0 10px rgba(0, 255, 200, 0.05);
            background: rgba(0, 255, 200, 0.02);
        }

        button {
            padding: 12px 28px;
            background: linear-gradient(135deg, #00ffcc 0%, #00aaff 100%);
            color: #0a0e27;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 700;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 0 20px rgba(0, 255, 200, 0.3);
            position: relative;
            overflow: hidden;
        }

        button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        button:hover {
            box-shadow: 0 0 40px rgba(0, 255, 200, 0.6);
            transform: translateY(-3px);
        }

        button:hover::before {
            width: 300px;
            height: 300px;
        }

        button:active {
            transform: translateY(-1px);
        }

        .result {
            background: rgba(0, 0, 0, 0.4);
            padding: 25px;
            border-radius: 8px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
            max-height: 1200px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-break: break-word;
            border-left: 4px solid #00ffcc;
            display: none;
            color: #00ffcc;
            border: 1px solid rgba(0, 255, 200, 0.2);
        }

        .result.show { display: block; }

        .result.error {
            color: #ff3366;
            border-left-color: #ff3366;
            border-color: rgba(255, 51, 102, 0.2);
            background: rgba(255, 51, 102, 0.05);
        }

        .result.success {
            color: #00ffcc;
            border-left-color: #00ffcc;
            border-color: rgba(0, 255, 200, 0.2);
            background: rgba(0, 255, 200, 0.05);
        }

        .result img {
            max-width: 100%;
            margin-top: 15px;
            border-radius: 6px;
            border: 1px solid rgba(0, 255, 200, 0.2);
        }

        .result iframe {
            width: 100%;
            height: 500px;
            border: 1px solid rgba(0, 255, 200, 0.2);
            border-radius: 6px;
            margin-top: 15px;
            background: rgba(0, 0, 0, 0.5);
        }

        /* Scrollbar styling */
        .result::-webkit-scrollbar {
            width: 8px;
        }

        .result::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
        }

        .result::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #00ffcc 0%, #ff00ff 100%);
            border-radius: 4px;
        }

        .result::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #00ffff 0%, #ff0080 100%);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ LEGEND AI</h1>
        <div class="subtitle">AI-Powered Swing Trading Dashboard | Real-Time Pattern Detection</div>

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

        function createTradingViewWidget(symbol, containerId) {
            """Create TradingView advanced chart widget with studies"""
            const container = document.getElementById(containerId);
            if (!container) return;

            const tvSymbol = symbol.includes(':') ? symbol : 'NASDAQ:' + symbol;

            const widgetHTML = `
                <div class="tradingview-widget-container" style="height:100%;width:100%">
                  <div class="tradingview-widget-container__widget" style="height:calc(100% - 32px);width:100%"></div>
                  <div class="tradingview-widget-copyright">
                    <a href="https://www.tradingview.com/symbols/${tvSymbol}/" rel="noopener nofollow" target="_blank">
                      <span class="blue-text">${symbol} chart</span>
                    </a>
                    <span class="trademark"> by TradingView</span>
                  </div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
                  {
                    "allow_symbol_change": true,
                    "calendar": false,
                    "details": false,
                    "hide_side_toolbar": true,
                    "hide_top_toolbar": false,
                    "hide_legend": false,
                    "hide_volume": false,
                    "hotlist": false,
                    "interval": "D",
                    "locale": "en",
                    "save_image": true,
                    "style": "1",
                    "symbol": "${tvSymbol}",
                    "theme": "dark",
                    "timezone": "Etc/UTC",
                    "backgroundColor": "#0F0F0F",
                    "gridColor": "rgba(242, 242, 242, 0.06)",
                    "withdateranges": false,
                    "studies": [
                      "STD;RSI",
                      "STD;MACD",
                      "Volume@tv-basicstudies",
                      "STD;SMA",
                      "STD;EMA"
                    ],
                    "autosize": true
                  }
                  <\/script>
                </div>
            `;

            container.innerHTML = widgetHTML;

            // Reload the TradingView script
            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.async = true;
            document.body.appendChild(script);
        }

        function createTickerTapeWidget(containerId, symbols) {
            const container = document.getElementById(containerId);
            if (!container) return;

            const widgetHTML = `
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <div class="tradingview-widget-copyright">
                    <a href="https://www.tradingview.com/markets/" rel="noopener nofollow" target="_blank">
                      <span class="blue-text">Ticker tape</span>
                    </a>
                    <span class="trademark"> by TradingView</span>
                  </div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
                  {
                    "symbols": ${JSON.stringify(symbols)},
                    "colorTheme": "dark",
                    "locale": "en",
                    "largeChartUrl": "",
                    "isTransparent": false,
                    "showSymbolLogo": true,
                    "displayMode": "adaptive"
                  }
                  <\/script>
                </div>
            `;

            container.innerHTML = widgetHTML;
            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.async = true;
            document.body.appendChild(script);
        }

        function createStockHeatmapWidget(containerId, options = {}) {
            const container = document.getElementById(containerId);
            if (!container) return;

            const defaultOptions = {
                "dataSource": "SPX500",
                "blockSize": "market_cap_basic",
                "blockColor": "change",
                "grouping": "sector",
                "locale": "en",
                "colorTheme": "dark",
                "isZoomEnabled": true,
                "hasSymbolTooltip": true,
                "width": "100%",
                "height": "100%"
            };

            const config = { ...defaultOptions, ...options };

            const widgetHTML = `
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <div class="tradingview-widget-copyright">
                    <a href="https://www.tradingview.com/heatmap/stock/" rel="noopener nofollow" target="_blank">
                      <span class="blue-text">Stock Heatmap</span>
                    </a>
                    <span class="trademark"> by TradingView</span>
                  </div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
                  ${JSON.stringify(config)}
                  <\/script>
                </div>
            `;

            container.innerHTML = widgetHTML;
            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.async = true;
            document.body.appendChild(script);
        }

        function createETFHeatmapWidget(containerId, options = {}) {
            const container = document.getElementById(containerId);
            if (!container) return;

            const defaultOptions = {
                "dataSource": "AllUSEtf",
                "blockSize": "volume",
                "blockColor": "change",
                "grouping": "asset_class",
                "locale": "en",
                "colorTheme": "dark",
                "isZoomEnabled": true,
                "hasSymbolTooltip": true,
                "width": "100%",
                "height": "100%"
            };

            const config = { ...defaultOptions, ...options };

            const widgetHTML = `
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <div class="tradingview-widget-copyright">
                    <a href="https://www.tradingview.com/heatmap/etf/" rel="noopener nofollow" target="_blank">
                      <span class="blue-text">ETF Heatmap</span>
                    </a>
                    <span class="trademark"> by TradingView</span>
                  </div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-etf-heatmap.js" async>
                  ${JSON.stringify(config)}
                  <\/script>
                </div>
            `;

            container.innerHTML = widgetHTML;
            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.async = true;
            document.body.appendChild(script);
        }

        function createStockScreenerWidget(containerId, options = {}) {
            const container = document.getElementById(containerId);
            if (!container) return;

            const defaultOptions = {
                "market": "america",
                "showToolbar": true,
                "defaultColumn": "overview",
                "defaultScreen": "top_gainers",
                "isTransparent": false,
                "locale": "en",
                "colorTheme": "dark",
                "width": "100%",
                "height": 550
            };

            const config = { ...defaultOptions, ...options };

            const widgetHTML = `
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <div class="tradingview-widget-copyright">
                    <a href="https://www.tradingview.com/screener/" rel="noopener nofollow" target="_blank">
                      <span class="blue-text">Stock Screener</span>
                    </a>
                    <span class="trademark"> by TradingView</span>
                  </div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-screener.js" async>
                  ${JSON.stringify(config)}
                  <\/script>
                </div>
            `;

            container.innerHTML = widgetHTML;
            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.async = true;
            document.body.appendChild(script);
        }

        function createEconomicCalendarWidget(containerId, options = {}) {
            const container = document.getElementById(containerId);
            if (!container) return;

            const defaultOptions = {
                "colorTheme": "dark",
                "isTransparent": false,
                "locale": "en",
                "countryFilter": "us",
                "importanceFilter": "-1,0,1",
                "width": "100%",
                "height": "100%"
            };

            const config = { ...defaultOptions, ...options };

            const widgetHTML = `
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <div class="tradingview-widget-copyright">
                    <a href="https://www.tradingview.com/economic-calendar/" rel="noopener nofollow" target="_blank">
                      <span class="blue-text">Economic Calendar</span>
                    </a>
                    <span class="trademark"> by TradingView</span>
                  </div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
                  ${JSON.stringify(config)}
                  <\/script>
                </div>
            `;

            container.innerHTML = widgetHTML;
            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.async = true;
            document.body.appendChild(script);
        }

        function createTopStoriesWidget(containerId, options = {}) {
            const container = document.getElementById(containerId);
            if (!container) return;

            const defaultOptions = {
                "displayMode": "regular",
                "feedMode": "market",
                "colorTheme": "dark",
                "isTransparent": false,
                "locale": "en",
                "market": "stock",
                "width": "100%",
                "height": "100%"
            };

            const config = { ...defaultOptions, ...options };

            const widgetHTML = `
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <div class="tradingview-widget-copyright">
                    <a href="https://www.tradingview.com/news/" rel="noopener nofollow" target="_blank">
                      <span class="blue-text">Top stories</span>
                    </a>
                    <span class="trademark"> by TradingView</span>
                  </div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
                  ${JSON.stringify(config)}
                  <\/script>
                </div>
            `;

            container.innerHTML = widgetHTML;
            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.async = true;
            document.body.appendChild(script);
        }

        function createSymbolInfoWidget(symbol, containerId, options = {}) {
            const container = document.getElementById(containerId);
            if (!container) return;

            let tvSymbol = symbol;
            if (!symbol.includes(':')) {
                tvSymbol = 'NASDAQ:' + symbol;
            }

            const defaultOptions = {
                "symbol": tvSymbol,
                "colorTheme": "dark",
                "isTransparent": false,
                "locale": "en",
                "width": "100%"
            };

            const config = { ...defaultOptions, ...options };

            const widgetHTML = `
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <div class="tradingview-widget-copyright">
                    <a href="https://www.tradingview.com/symbols/${tvSymbol}/" rel="noopener nofollow" target="_blank">
                      <span class="blue-text">${symbol} performance</span>
                    </a>
                    <span class="trademark"> by TradingView</span>
                  </div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js" async>
                  ${JSON.stringify(config)}
                  <\/script>
                </div>
            `;

            container.innerHTML = widgetHTML;
            const script = document.createElement('script');
            script.src = 'https://s3.tradingview.com/tv.js';
            script.async = true;
            document.body.appendChild(script);
        }

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
                    let html = `<h3>${d.pattern} (Score: ${d.score.toFixed(1)}/10)</h3>`;
                    html += `<p>Entry: $${d.entry.toFixed(2)} | Stop: $${d.stop.toFixed(2)} | Target: $${d.target.toFixed(2)}</p>`;
                    html += `<p>R:R: ${d.risk_reward.toFixed(2)}:1 | Current: $${d.current_price.toFixed(2)}</p>`;

                    if (d.chart_url) {
                        if (d.chart_url.includes('tradingview')) {
                            html += `<iframe src="${d.chart_url}" style="width:100%; height:500px; border: 1px solid #ddd; border-radius: 6px; margin-top: 15px;"></iframe>`;
                        } else {
                            html += `<img src="${d.chart_url}" alt="Chart" style="max-width: 100%; margin-top: 15px; border-radius: 6px;">`;
                        }
                    } else {
                        html += `<p style="text-align: center; color: #999; margin-top: 15px;">📊 Chart not available</p>`;
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
            showResult('watchlistResult', 'Loading watchlist...', false);

            try {
                const response = await fetch(API_BASE + '/api/watchlist');
                if (!response.ok) throw new Error('HTTP ' + response.status);
                const data = await response.json();

                if (data.success && data.items && data.items.length > 0) {
                    let html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(600px, 1fr)); gap: 20px; margin-top: 20px;">';

                    data.items.forEach((item, idx) => {
                        const containerId = 'chart_' + item.ticker + '_' + idx;
                        html += `
                            <div style="border: 1px solid rgba(0, 255, 200, 0.3); border-radius: 8px; padding: 15px; background: rgba(15, 20, 50, 0.5); overflow: hidden;">
                                <div style="margin-bottom: 10px;">
                                    <h3 style="margin: 0 0 5px 0; color: #00ffcc;">${item.ticker}</h3>
                                    <p style="margin: 0 0 10px 0; font-size: 12px; color: #b0b0b0;">
                                        <strong>Reason:</strong> ${item.reason || 'No reason specified'}
                                    </p>
                                    <p style="margin: 0; font-size: 11px; color: #808080;">Added: ${item.added_date}</p>
                                </div>
                                <div style="border-top: 1px solid rgba(0, 255, 200, 0.2); padding-top: 10px; margin-top: 10px; height: 350px;">
                                    <div id="${containerId}" style="height: 100%; width: 100%;"></div>
                                </div>
                            </div>
                        `;
                    });

                    html += '</div>';
                    const resultEl = document.getElementById('watchlistResult');
                    resultEl.innerHTML = html;
                    resultEl.classList.add('show', 'success');

                    // Create TradingView widgets for each stock
                    setTimeout(() => {
                        data.items.forEach((item, idx) => {
                            const containerId = 'chart_' + item.ticker + '_' + idx;
                            createTradingViewWidget(item.ticker, containerId);
                        });
                    }, 100);
                } else {
                    showResult('watchlistResult', 'Watchlist is empty. Add stocks to monitor them!', false);
                }
            } catch (error) {
                showResult('watchlistResult', 'Error: ' + error.message, true);
            }
        }

        async function getMarketData() {
            showResult('marketResult', 'Loading market data with TradingView widgets...', false);

            try {
                const response = await fetch(API_BASE + '/api/market/internals');
                if (!response.ok) throw new Error('HTTP ' + response.status);
                const data = await response.json();

                if (data.success) {
                    const m = data.data;
                    let html = '<div style="margin-top: 20px;">';

                    // Market Status Summary
                    html += '<div style="background: linear-gradient(135deg, #00ffcc 0%, #ff00ff 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 0 30px rgba(0, 255, 200, 0.3);">';
                    html += '<h3 style="margin: 0 0 10px 0;">📊 Market Status</h3>';
                    html += '<p style="margin: 0;"><strong>SPY Price:</strong> $' + m.spy_price.toFixed(2) + '</p>';
                    html += '<p style="margin: 5px 0;"><strong>50 SMA:</strong> $' + m.sma_50.toFixed(2) + '</p>';
                    html += '<p style="margin: 5px 0;"><strong>200 SMA:</strong> $' + m.sma_200.toFixed(2) + '</p>';
                    html += '<p style="margin: 5px 0;"><strong>Regime:</strong> ' + m.regime + '</p>';
                    html += '<p style="margin: 5px 0; font-size: 14px;"><strong>Status:</strong> ' + m.status + '</p>';
                    html += '</div>';

                    // Ticker Tape
                    html += '<div style="margin-top: 30px; margin-bottom: 30px; border: 1px solid rgba(0, 255, 200, 0.3); border-radius: 8px; padding: 0; background: rgba(15, 20, 50, 0.5); overflow: hidden; height: 70px;">';
                    html += '<div id="ticker_tape_container" style="height: 100%; width: 100%;"></div>';
                    html += '</div>';

                    // Main Market Indices
                    html += '<h3 style="color: #00ffcc; margin-top: 30px; margin-bottom: 15px;">📈 Market Indices</h3>';
                    html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(600px, 1fr)); gap: 20px;">';

                    const indices = [
                        { name: 'S&P 500', symbol: 'SPY', emoji: '📊' },
                        { name: 'Nasdaq 100', symbol: 'QQQ', emoji: '🟦' },
                        { name: 'Russell 2000', symbol: 'IWM', emoji: '📉' },
                        { name: 'Dow Jones', symbol: 'DIA', emoji: '📈' }
                    ];

                    indices.forEach((idx, i) => {
                        const containerId = 'chart_' + idx.symbol;
                        html += '<div style="border: 1px solid rgba(0, 255, 200, 0.3); border-radius: 8px; padding: 0; background: rgba(15, 20, 50, 0.5); overflow: hidden;">';
                        html += '<h4 style="margin: 12px 15px; color: #00ffcc;">' + idx.emoji + ' ' + idx.name + ' (' + idx.symbol + ')</h4>';
                        html += '<div id="' + containerId + '" style="height: 300px; width: 100%;"></div>';
                        html += '</div>';
                    });

                    html += '</div>';

                    // Sector Performance Grid
                    html += '<h3 style="color: #00ffcc; margin-top: 30px; margin-bottom: 15px;">🏭 Sector Performance</h3>';
                    html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(600px, 1fr)); gap: 20px;">';

                    const sectors = [
                        { name: 'Technology', symbol: 'XLK', emoji: '💻' },
                        { name: 'Healthcare', symbol: 'XLV', emoji: '⚕️' },
                        { name: 'Financials', symbol: 'XLF', emoji: '💰' },
                        { name: 'Energy', symbol: 'XLE', emoji: '⚡' },
                        { name: 'Industrials', symbol: 'XLI', emoji: '🏗️' },
                        { name: 'Consumer Disc.', symbol: 'XLY', emoji: '🛍️' }
                    ];

                    sectors.forEach(sector => {
                        const containerId = 'chart_' + sector.symbol;
                        html += '<div style="border: 1px solid rgba(0, 255, 200, 0.3); border-radius: 8px; padding: 0; background: rgba(15, 20, 50, 0.5); overflow: hidden;">';
                        html += '<h4 style="margin: 12px 15px; color: #00ffcc;">' + sector.emoji + ' ' + sector.name + ' (' + sector.symbol + ')</h4>';
                        html += '<div id="' + containerId + '" style="height: 280px; width: 100%;"></div>';
                        html += '</div>';
                    });

                    html += '</div>';

                    // Stock Heatmap
                    html += '<h3 style="color: #00ffcc; margin-top: 30px; margin-bottom: 15px;">🔥 Stock Heatmap (S&P 500)</h3>';
                    html += '<div style="border: 1px solid rgba(0, 255, 200, 0.3); border-radius: 8px; padding: 0; background: rgba(15, 20, 50, 0.5); overflow: hidden; height: 600px; margin-bottom: 30px;">';
                    html += '<div id="stock_heatmap_container" style="height: 100%; width: 100%;"></div>';
                    html += '</div>';

                    // ETF Heatmap
                    html += '<h3 style="color: #00ffcc; margin-top: 30px; margin-bottom: 15px;">📊 ETF Heatmap (Asset Classes)</h3>';
                    html += '<div style="border: 1px solid rgba(0, 255, 200, 0.3); border-radius: 8px; padding: 0; background: rgba(15, 20, 50, 0.5); overflow: hidden; height: 600px; margin-bottom: 30px;">';
                    html += '<div id="etf_heatmap_container" style="height: 100%; width: 100%;"></div>';
                    html += '</div>';

                    // Stock Screener
                    html += '<h3 style="color: #00ffcc; margin-top: 30px; margin-bottom: 15px;">🔎 Stock Screener</h3>';
                    html += '<div style="border: 1px solid rgba(0, 255, 200, 0.3); border-radius: 8px; padding: 0; background: rgba(15, 20, 50, 0.5); overflow: hidden; margin-bottom: 30px;">';
                    html += '<div id="stock_screener_container" style="height: 100%; width: 100%;"></div>';
                    html += '</div>';

                    html += '</div>'; // Close main div

                    const resultEl = document.getElementById('marketResult');
                    resultEl.innerHTML = html;
                    resultEl.classList.add('show', 'success');

                    // Create TradingView widgets for all indices and sectors
                    setTimeout(() => {
                        // Ticker Tape
                        const tickerSymbols = [
                            { "proName": "FOREXCOM:SPXUSD", "title": "S&P 500" },
                            { "proName": "FOREXCOM:NSXUSD", "title": "NASDAQ 100" },
                            { "proName": "CBOT:ZB1!", "title": "US Treasury Bonds" },
                            { "proName": "BITSTAMP:BTCUSD", "title": "Bitcoin" },
                            { "proName": "BITSTAMP:ETHUSD", "title": "Ethereum" }
                        ];
                        createTickerTapeWidget('ticker_tape_container', tickerSymbols);

                        // Index and sector charts
                        indices.forEach(idx => {
                            createTradingViewWidget(idx.symbol, 'chart_' + idx.symbol);
                        });
                        sectors.forEach(sector => {
                            createTradingViewWidget(sector.symbol, 'chart_' + sector.symbol);
                        });

                        // Heatmaps and screener
                        createStockHeatmapWidget('stock_heatmap_container');
                        createETFHeatmapWidget('etf_heatmap_container');
                        createStockScreenerWidget('stock_screener_container');
                    }, 100);
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
