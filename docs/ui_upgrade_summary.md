# Legend AI UI & Scanner Upgrade

<<<<<<< HEAD
<<<<<<< HEAD
## Highlights
- **Analyze tab** now renders Chart-IMG snapshots with 21 EMA, 50 SMA, volume, and annotated entry/stop/target overlays plus clear loading/error states.
- **Pattern Scanner** backend accepts timeframe, sector, ATR, and pattern filters with normalized stats while the UI exposes richer controls, inline chart previews, and CSV export.
- **Top Setups** cards ship with matching gradient action buttons and no-click Preview Chart images; Market Internals reuses TradingView tape/heatmap/mini widgets.
- **Watchlist** supports edit/update operations, multi-select tags, status/tag filters, and gradient action buttons across the dashboard for consistency.
- **Playwright regression** exercises chart rendering, scanner runs, top setup preview, and watchlist CRUD on the live deployment.

## Notes
- Advanced pattern detectors (triangles, wedges, etc.) piggy-back on the Minervini/VCP engine; enabling deeper detection will require additional detectors inside `app/core/detectors`.
- TradingView telemetry requests still log failures in headless mode (
`widget-sheriff` / `telemetry`), but the widgets render correctly after this pass.
=======
=======
>>>>>>> remotes/origin/claude/add-crypto-analysis-01XGmBZsBCfF6bHWVEa7RYZd
## Highlights (Nov 15, 2025)
- **Analyze / Chart stack** – Chart-IMG snapshots now default to blue 21 EMA, red 50 SMA, volume, and RSI overlays with automatic entry/stop/target annotations plus retry/inline error states. TradingView Symbol Lab reuses the same color scheme for its advanced chart embed and links are exposed via `TV` buttons in Analyze, Pattern Scanner, Top Setups, and Watchlist.
- **Pattern Scanner + detectors** – Backend accepts timeframe, sector, ATR, and multi-pattern filters covering VCP, cups/flat bases, breakouts, pullbacks to 21/50, wedges, triangles, and head & shoulders structures. UI adds richer controls, stats cards, inline Chart-IMG previews, and an optional TradingView screener card (documented TT limitations).
- **Top Setups** – Cards ship with unified gradient Analyze/Watchlist/Preview/TV buttons, nowrap price tiles, and modal Chart-IMG previews. Detector badges align with scanner enums.
- **Market Internals** – Section reorganized into neon cards that host ticker tape, SPY/QQQ/IWM/VIX minis, the user-specified TradingView Market Overview widget, SPX + ETF heatmaps, screener, and the economic calendar. Async guards maintain <5s loads even with stacked widgets.
- **Watchlist** – Form now supports edit mode with banner + disabled ticker input, expanded swing-trader tag chips (Breakout, Momentum, VCP, Pullback, Earnings, Post-Earnings Drift, Leader, Laggard, Reclaim 21/50, First Pullback, Late-Stage Base, Extended, etc.), status/tag filters, gradient action buttons, and direct Analyze/TV shortcuts per row. Playwright covers add → edit → filter → remove flows.
- **TV Symbol Lab** – New `/tv?tvwidgetsymbol=` route + template combine ticker tape, symbol info, advanced chart (w/ EMA21/SMA50/RSI), profile, fundamentals, technical analysis, news, and our Chart-IMG snapshot so users can inspect any ticker in a dedicated TradingView stack; Watchlist/Scanner/Analyze actions open it in a new tab.

## Notes
- Advanced pattern detectors for wedges, triangles, and head & shoulders formations now sit alongside legacy detectors inside `app/core/pattern_detector.py`, and `app/api/universe.py` exposes canonical pattern names for both scanner + Top Setups filtering.
- TradingView telemetry requests (`widget-sheriff`, `telemetry.tradingview.com/widget/report`) still log `net::ERR_ABORTED` in headless mode; documented as benign noise.
- TradingView Screener embed cannot fully mirror Minervini’s Trend Template filters; the card caption clarifies the limitation and points users to Legend AI’s native scanner for the full TT implementation.
<<<<<<< HEAD
>>>>>>> remotes/origin/claude/add-crypto-analysis-01XGmBZsBCfF6bHWVEa7RYZd
=======
>>>>>>> remotes/origin/claude/add-crypto-analysis-01XGmBZsBCfF6bHWVEa7RYZd
