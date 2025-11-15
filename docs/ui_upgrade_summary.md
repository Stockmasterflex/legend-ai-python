# Legend AI UI & Scanner Upgrade

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
