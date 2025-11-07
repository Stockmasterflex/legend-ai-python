# TradingView Widgets in Legend AI Dashboards

This guide shows how to embed official TradingView widgets inside Python-powered dashboards (FastAPI/Starlette templates, Flask/Jinja, Streamlit, Dash, etc.). The approach loads `tv.js` once and spins up any widget type by describing it with JSON.

---

## ⚙️ Basic Concept

1. Define a list of widget descriptors in Python. Each descriptor has a `type` (maps to a TradingView constructor) and an `options` dict (copied from TradingView’s docs).
2. Render an HTML template that:
   - Creates a `<div>` placeholder for every widget.
   - Stores the JSON config in a `<script type="application/json">` block.
   - Loads `https://s3.tradingview.com/tv.js` once.
   - Runs a small script that reads every config block and instantiates the correct widget.

This keeps layout/CSS under your control while still using the official widgets (which render as iframes).

---

## 🧪 Minimal Flask Example

> Drop-in demo you can run locally; adapt the same pattern to FastAPI or any other framework that can render Jinja-style templates.

`app.py`

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    widgets = [
        {"type": "ticker-tape", "options": {
            "symbols": [
                {"proName": "FOREXCOM:SPXUSD", "title": "S&P 500"},
                {"proName": "NASDAQ:NDX", "title": "Nasdaq 100"},
                {"proName": "DJ:DJI", "title": "Dow"},
                {"proName": "CRYPTO:BTCUSD", "title": "BTC"},
                {"proName": "FX:EURUSD", "title": "EURUSD"},
            ],
            "showSymbolLogo": True
        }},
        {"type": "market-overview", "options": {
            "tabs": [
                {"title": "US Indices", "symbols": [{"s": "FOREXCOM:SPXUSD"}, {"s": "NASDAQ:NDX"}, {"s": "DJ:DJI"}, {"s": "CME_MINI:RTY1!"}]},
                {"title": "Futures", "symbols": [{"s": "CME_MINI:ES1!"}, {"s": "CME_MINI:NQ1!"}, {"s": "NYMEX:CL1!"}, {"s": "COMEX:GC1!"}]},
            ]
        }},
        {"type": "stock-heatmap", "options": {"dataSource": "SPX"}},
        {"type": "screener", "options": {"defaultColumn": "overview", "defaultScreen": "most_capitalized_us"}},
        {"type": "symbol-overview", "options": {"symbols": [["NASDAQ:NVDA|1D"], ["NASDAQ:AAPL|1D"], ["NASDAQ:AMZN|1D"]]}},
        {"type": "advanced-chart", "options": {"symbol": "NASDAQ:NVDA", "interval": "60"}},
        {"type": "top-stories", "options": {}},
        {"type": "economic-calendar", "options": {"importanceFilter": "-1,0,1", "currencyFilter": "USD,EUR"}}
    ]
    return render_template("dashboard.html", widgets=widgets)

if __name__ == "__main__":
    app.run(debug=True)
```

`templates/dashboard.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Legend AI – TradingView Widgets</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <!-- Optional CSP if you enforce one:
  <meta http-equiv="Content-Security-Policy"
        content="default-src 'self';
                 script-src 'self' https://s3.tradingview.com;
                 frame-src https://s.tradingview.com https://www.tradingview.com;
                 img-src * data:;
                 style-src 'self' 'unsafe-inline'"> -->
  <style>
    body { margin:0; background:#0b0e11; color:#e5e7eb; font-family: system-ui,-apple-system,Segoe UI,Roboto,sans-serif; }
    .grid { display:grid; gap:16px; grid-template-columns:repeat(auto-fit, minmax(320px,1fr)); padding:16px; }
    .card { background:#111418; border:1px solid #1f242b; border-radius:12px; padding:8px; min-height:220px; }
    .full { grid-column: 1/-1; min-height:520px; }
  </style>
</head>
<body>
  <div class="grid" id="tv-root">
    {% for w in widgets %}
      <div class="card {% if w.type in ['advanced-chart','market-overview'] %}full{% endif %}">
        <div class="tv-container" id="tv_{{ loop.index }}"></div>
        <script type="application/json" class="tv-config" data-target="tv_{{ loop.index }}">
          {{ (w | tojson) | safe }}
        </script>
      </div>
    {% endfor %}
  </div>

  <script async src="https://s3.tradingview.com/tv.js"></script>
  <script>
    const TV_CONSTRUCTORS = {
      "advanced-chart":        "widget",
      "symbol-overview":       "SymbolOverviewWidget",
      "mini-chart":            "MiniWidget",
      "market-overview":       "MarketOverviewWidget",
      "stock-market":          "StockMarketWidget",
      "market-quotes":         "MarketQuotesWidget",
      "ticker-tape":           "tickerTape",
      "ticker":                "TickerWidget",
      "single-ticker":         "SingleTickerWidget",
      "stock-heatmap":         "StockHeatmapWidget",
      "crypto-heatmap":        "CryptoHeatmapWidget",
      "etf-heatmap":           "ETFHeatmapWidget",
      "forex-cross-rates":     "ForexCrossRatesWidget",
      "forex-heatmap":         "ForexHeatmapWidget",
      "screener":              "ScreenerWidget",
      "crypto-mkt-screener":   "CryptoMarketWidget",
      "symbol-info":           "SymbolInfoWidget",
      "technical-analysis":    "TechnicalAnalysisWidget",
      "fundamental-data":      "FundamentalDataWidget",
      "company-profile":       "CompanyProfileWidget",
      "top-stories":           "TopStoriesWidget",
      "economic-calendar":     "EconomicCalendarWidget"
    };

    (function mountWhenReady(){
      if (!window.TradingView) { return setTimeout(mountWhenReady, 50); }

      document.querySelectorAll('.tv-config').forEach(scriptTag => {
        const cfg = JSON.parse(scriptTag.textContent);
        const containerId = scriptTag.dataset.target;
        const type = cfg.type;
        const options = cfg.options || {};
        const ctorName = TV_CONSTRUCTORS[type];

        if (!ctorName) {
          console.warn("Unknown TradingView widget type:", type);
          return;
        }

        const baseOptions = {
          container_id: containerId,
          autosize: true,
          theme: "dark",
          locale: "en",
          ...options
        };

        if (type === "advanced-chart") {
          new window.TradingView.widget(baseOptions);
        } else {
          new window.TradingView[ctorName](baseOptions);
        }
      });
    })();
  </script>
</body>
</html>
```

Run `python app.py` and open `http://127.0.0.1:5000/`.

---

## 🔁 Reusing in Legend AI / FastAPI

- Add an endpoint that prepares the `widgets` list and renders a template (or returns `HTMLResponse`).
- The same template works with FastAPI/Jinja because it only relies on standard templating features.
- For the existing Legend AI dashboards, you can embed the HTML block inside the HTMX/Gradio view or expose it behind `/dashboard/widgets`.

---

## 📦 Using in Streamlit or Dash

| Framework | How to render |
|-----------|---------------|
| **Streamlit** | `html = render_template("dashboard.html", widgets=widgets)` then `st.components.v1.html(html, height=1200, scrolling=True)` |
| **Plotly Dash** | Pass `srcDoc=rendered_html` into an `html.Iframe`, or copy the `<div>` + script tags into Dash layouts (ensure Dash allows inline scripts/CSP). |
| **Gradio / HTMX** | Serve the rendered HTML as part of your FastAPI endpoint and embed it via `<iframe src="/dashboard/widgets">`. |

---

## 🧱 Adding New Widgets

1. Pick a widget from the [TradingView Widgets Catalog](https://www.tradingview.com/widget/).
2. Grab the JSON snippet from their builder.
3. Append a dict to the Python `widgets` list: `{"type": "technical-analysis", "options": { ... }}`.
4. If the widget should be full-width, add logic similar to the `{% if ... %}full{% endif %}` class assignment.
5. Theme/light mode: either set `theme: "light"` globally in the JS script or per widget inside `options`.

---

## ⚠️ Notes & Limitations

- Widgets are iframe embeds; they do **not** give you data back. Keep using TwelveData/Redis cache for server-side analytics.
- Free widgets include TradingView branding and may deliver delayed quotes depending on the exchange.
- Follow TradingView’s terms of service; some widgets require users to accept their cookies.
- If you enforce CSPs, remember to allow scripts from `https://s3.tradingview.com` and frames from `https://www.tradingview.com` / `https://s.tradingview.com`.
- For dynamic pages like `/symbol/AAPL`, set the widget’s `symbol` option from the route parameter and re-render the template.

---

## ✅ Checklist When Embedding

- [ ] Load `tv.js` once per page.
- [ ] Ensure every widget `type` maps to a constructor in `TV_CONSTRUCTORS`.
- [ ] Pass `container_id` and unique `div` IDs to avoid collisions.
- [ ] Lazy-mount widgets after `window.TradingView` is defined.
- [ ] Keep CSS responsive (use grid/flex) so widgets resize with the dashboard.

With this pattern you can build rich client dashboards (market overview, watchlists, single stock drill-downs) without leaving Python.
