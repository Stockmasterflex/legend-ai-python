# Legend AI UI Audit (Playwright MCP)

_Last run: 2025-11-15 06:58 UTC_

## Method
- Script: `node tests/playwright_mcp_dashboard_test.js`
- Target: https://legend-ai-python-production.up.railway.app/dashboard
- Browser: Playwright Chromium, 1920×1080, headless
- Outputs: 24 full-page screenshots under `screenshots/playwright-mcp/step-*.png` (step-01 … step-24), console + network logs streamed to stdout

## Global Observations
1. Dashboard still announces `Dashboard initialized successfully`; Alpine remains absent and unused. Tab switching stays instantaneous.
2. All primary tabs (Analyze, Pattern Scanner, Top Setups, Market Internals, Watchlist) render populated content with no blank panes or orphan widgets.
3. Chart-IMG requests succeed for every Analyze run plus scanner/Top Setup previews; the preset now shows blue 21 EMA, red 50 SMA, volume, and an RSI panel while the retry button never surfaced.
4. Pattern Scanner auto-runs on load, displays a clear “Scanning universe…” message, and the Playwright suite covered the default NASDAQ scan plus Rising Wedge-only and mixed VCP + 21 EMA Pullback + Ascending Triangle scans without errors.
5. TradingView widgets (ticker tape, SPY/QQQ/IWM/VIX minis, Market Overview widget, dedicated stock/ETF heatmaps, screener, and the economic calendar) mount reliably; expected `widget-sheriff` / `telemetry.tradingview.com` `net::ERR_ABORTED` logs remain harmless noise.
6. Watchlist CRUD, the “Editing TICKER” banner, expanded swing-trader tag library, and the TV action links behave as intended—Playwright added tags, edited status/notes/tags, filtered by tag, opened the TV Symbol Lab, and removed the row without stale forms.
7. The new `/tv?tvwidgetsymbol=` page renders ticker tape, symbol info, advanced chart, fundamentals, technicals, news, and the Chart-IMG snapshot for each symbol; Playwright hits the page via the Watchlist TV action and verifies the advanced chart container.

## Tab Notes
### Analyze
- NVDA/IBM daily and AAPL weekly scans return complete intel cards plus Chart-IMG snapshots with blue 21 EMA, red 50 SMA, volume, RSI panel, and trade annotations (steps 10–12).
- Quick Scan on NVDA fires instantly; `/api/analyze` responses remain 200 and the chart status badge flips to “Chart synced” while the plan cards refresh (steps 13–15).
- Snapshot + Add-to-Watchlist CTAs remain enabled post-scan; the inline chart now occupies the full right column with clear status chips and retry messaging.

### Pattern Scanner
- NASDAQ-100 scans with relaxed defaults auto-run in ~4 seconds; stats show universe, candidates, scanned count, cache hits, and thresholds (step 16).
- Additional scans filtered exclusively to Rising Wedge (step 17) and a VCP + 21 EMA Pullback + Ascending Triangle mix (step 18) both ran without errors and surfaced matching setups or the empty-state message.
- Table columns include ticker, pattern, score, RS, ATR%, sector, entry/stop/target, R:R, chart slot, and Analyze/Watch CTAs. Inline preview buttons still spin up Chart-IMG when requested, and the temporary “Scanning…” row plus toast make progress obvious.

### Top Setups
- Cards ship with unified gradient buttons for Analyze, Watchlist, and Preview Chart. Analyze jumps back to the Analyze tab and performs a fresh scan (step 19); Preview regenerates a Chart-IMG thumbnail inline with loading state (step 20).
- Entry/Stop/Target tiles now use `white-space: nowrap`; the Playwright script asserts no values wrap across lines before moving on.

### Market Internals
- Summary cards cover regime, SPY vs SMA50/200, breadth, volatility, and API usage after `/api/market/internals` resolves (step 7).
- The rebuilt layout now includes the bespoke TradingView Market Overview widget, dedicated stock and ETF heatmap cards, the dark-themed economic calendar, ticker tape/minis, and the new TradingView screener card with a caption noting Trend Template limitations.

### Watchlist
- The form uses chip-based tag selectors plus a visible “Adding new ticker” / “Editing TICKER” banner; “Add to watchlist” flips to “Update watchlist” during edits with disabled ticker inputs (steps 21–22).
- Table rows render neon status pills, tag chips, and compact gradient Analyze/Edit/Remove buttons; deletions reflect immediately (step 24).
- Tag filters behave like toggles—Playwright filtered the table to the Leader tag (step 23) and clearing the filter restored the full list without layout shifts. Empty-state text updates when filters hide all entries.

## Outstanding / Watch Items
- TradingView telemetry endpoints (`widget-sheriff`, `telemetry.tradingview.com/widget/report`) still log `net::ERR_ABORTED` in headless mode—expected and harmless.
- TradingView screener embed cannot fully replicate Minervini Trend Template filters; the caption clarifies this, and Legend AI’s internal scanner remains the authoritative TT implementation.
- `window.Alpine` remains undefined in prod; fine today but note if Alpine-driven widgets return later.
- Consider caching additional breadth calculations so `/api/market/internals` remains sub-5s as universes expand.
