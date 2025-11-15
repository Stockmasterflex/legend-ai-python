# Legend AI UI Audit (Playwright MCP)

_Date: 2025-11-14 15:44 _

## Method
- Tool: `node tests/playwright_mcp_dashboard_test.js`
- Target: https://legend-ai-python-production.up.railway.app/dashboard
- Outputs: console/network logs + 12 screenshots in `screenshots/playwright-mcp/`

## Global Observations
1. **Hero clutter / orphan chart** – Landing page shows a TradingView chart strip directly under the hero, before any context. It reads like a stray widget rather than a purposeful element (see `screenshots/playwright-mcp/step-01-dashboard-loaded.png`).
2. **Tabs look empty** – Each tab presents a large blank card with minimal structure. Content is often stacked vertically with huge empty gaps, so the experience feels unfinished.
3. **Charts underused or misplaced** – Analyze tab returns text but no chart; Top Setups + Scanner results lack previews; Market Internals shows three stacked widgets without context headings.
4. **Console/network noise** – TradingView telemetry and policy calls (`widget-sheriff`, `telemetry.tradingview.com`) fail with `net::ERR_ABORTED`. These are harmless but pollute the console.
5. **Dark theme inconsistencies** – Buttons, tables, and cards don’t align on spacing and typography; multiple fonts/weights appear without clear hierarchy.

## Tab-by-Tab Findings

### Analyze
- After scanning NVDA, data fills the `#pattern-results` grid but the chart area under the form stays empty (`step-12`).
- Snapshot CTA points off to Chart-IMG but there’s no inline preview.
- Form + results stretch 100% width, making the page feel flat.

### Pattern Scanner
- Filters limited to universe, limit, min score, and RS. No pattern type, timeframe, ATR filters, etc. Layout uses a simple form grid without grouping (`step-05`).
- Results table lacks sector/entry info and has tiny “Watch / Chart” buttons with no icons.
- No indicator of API latency or last updated timestamp.

### Top Setups
- Section shows generic copy and empty grid until load; once data arrives there’s no chart or additional insight (`step-06`).
- Cards share same styling as Analyze results, so this supposedly premium list feels ordinary.

### Market Internals
- Three stacked TradingView widgets (heatmap, overview, calendar) with zero framing text; heavy vertical scrolling and no summary metrics (`step-07`).
- Missing the index overview / breadth indicators promised in roadmap docs.

### Watchlist
- Form uses stacked inputs with minimal guidance; result cards only show ticker, status, and notes (`step-08`).
- No columns for score, tags, or quick actions beyond Analyze/Remove.
- Filter dropdown works but the empty-state overlay covers entire tab—looks like a loading spinner.

## Known Issues to Fix
- Remove orphan TV widget on landing screen.
- Add inline chart panel to Analyze results (sync symbol/interval to the API response).
- Expand Pattern Scanner filters + results, wire them to `/api/universe/scan/quick` params.
- Polish Top Setups layout and surface quick chart previews / CTA.
- Redesign Market Internals with purposeful TradingView widgets + metrics.
- Improve Watchlist table layout, actions, and persistence cues.
- Investigate reducing/noising out TradingView telemetry errors (optional, but ensure no real API endpoints fail).
