# `/api/scan`

Returns the freshest VCP scan payload for the seeded universe that powers the Pattern Scanner + Top Setups tabs. This endpoint is feature-gated; it only runs when `LEGEND_FLAGS.enable_scanner` evaluates to `true`.

---

## Request

```
GET /api/scan?limit=<int>&sector=<optional string>
```

| Parameter | Type | Notes |
| --- | --- | --- |
| `limit` | integer | Number of hits to return (1‑200). The service always tops the list with the highest `legend_score` entries. |
| `sector` | string (optional) | Filters to symbols whose universe metadata reports a case-insensitive match. |

Any additional query parameters are ignored.

---

## Header behavior

- When `LEGEND_FLAGS.enable_scanner` is `false`, the endpoint still returns a payload with `results: []`, `universe_size: 0`, and `meta.reason: "scanner_disabled"` so clients can differentiate the flag state.
- Every response contains `meta.build_sha`, so the UI can tag tiles with the exact build that produced the scan.

---

## Response

```jsonc
{
  "as_of": "2025-11-08T00:00:00Z",
  "universe_size": 600,
  "results": [
    {
      "symbol": "AAPL",
      "timeframe": "1D",
      "pattern": "VCP",
      "legend_score": 92,
      "grade": "A",
      "reasons": ["3 clean contractions", "RS rank 88", "Trend template last pass"],
      "signals": {
        "vol_contractions": 3,
        "max_pullback_pct": 7.1,
        "base_days": 32,
        "pivot": 160.12,
        "rs_rank": 88,
        "ma_dist": {"ema21": 1.5, "sma50": 2.6, "sma200": 6.2}
      },
      "rule_failures": [],
      "atr_plan": {"atr": 3.2, "stop": 152.5, "risk_unit": 0.46},
      "chart_url": null,
      "sources": {"price": "twelvedata", "spy": "cache", "sector": "Information Technology"}
    },
    {
      "symbol": "ZNGA",
      "timeframe": "1D",
      "pattern": null,
      "legend_score": null,
      "grade": null,
      "reasons": [],
      "signals": {
        "vol_contractions": null,
        "max_pullback_pct": null,
        "base_days": null,
        "pivot": null,
        "rs_rank": null,
        "ma_dist": {"ema21": null, "sma50": null, "sma200": null}
      },
      "rule_failures": ["missing_ohlcv"],
      "atr_plan": {"atr": null, "stop": null, "risk_unit": null},
      "chart_url": null,
      "sources": {"price": null, "spy": null, "sector": null}
    }
  ],
  "meta": {
    "build_sha": "abc123",
    "duration_ms": 1234.5,
    "result_count": 2,
    "total_hits": 47
  }
}
```

### Result shapes

- `results` is limited to `limit` entries. When scanners skip symbols because they lack OHLCV, the API still preserves a placeholder entry with `rule_failures: ["missing_ohlcv"]` so callers can surface why a ticker is absent.
- Each success entry carries full VCP telemetry (signals, ATR plan, reasons, grade) plus a `sources` object showing the price source + sector.
- `meta.result_count` reflects the number of buckets actually serialized (placeholders + hits). `meta.total_hits` counts the number of full detections before the `limit` was applied.

---

## Usage notes

- `scan_request_duration_seconds{status,universe_size}` records this route’s latency so Grafana panels can show p50/p95 latency against the filtered universe size.
- Use `limit=1` as a cheap smoke check for deployments; cached results typically return in <200 ms.
- Missing data placeholders always include `rule_failures: ["missing_ohlcv"]`, allowing the UI to gray out a ticker while still showing the sector and symbol.

## Flag details

`LEGEND_FLAGS.enable_scanner` gates the entire endpoint. When the flag is disabled, clients receive a stub payload, metrics still record the request, and logs include `flag_scanner_enabled=false` so telemetry dashboards can track flag flips.
