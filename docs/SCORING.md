# Legend Score & Grade (VCP)

The scanner ranks every hit with a `legend_score` and grade before surfacing it to dashboards or the `/api/scan` response. The logic mirrors the classifiers in `app/services/scanner.py` so both Analyze + Scan use consistent math.

## Legend Score

`legend_score` is built from three moving parts:

| Component | Source | Weight | Notes |
| --- | --- | --- | --- |
| Detector confidence | `VCPDetector` | 70 points | `confidence ∈ [0,1]` is multiplied by 70 so a 0.85 confidence already earns 59.5 points. |
| RS rank | `relative_strength_metrics` | up to 20 points | `(rs_rank or 50) × 0.2` — a perfect rank (99) adds 19.8 points; a middling 50 ranks adds 10 points. |
| Minervini trend | `minervini_trend_template` | ±10 points | passing the trend template adds 10; failing subtracts 5 to penalize weak structure. |

The total is clamped to `[0,100]`:

```
score = min(100, max(0, round(confidence*70 + (rs_rank or 50)*0.2 + (trend_pass ? 10 : -5))))
```

### Example

- Confidence: 0.78 → 54.6 pts
- RS rank: 85 → 17 pts
- Trend pass: true → +10 pts
- Total: ~81 → `legend_score = 81`

## Grade mapping

The `grade` field translates `legend_score` into trader-friendly buckets:

| Score | Grade |
| --- | --- |
| ≥ 95 | `A+` |
| ≥ 85 | `A` |
| ≥ 70 | `B` |
| < 70 | `C` |

Grades dominate the UI badges (A+/A as 🔥, B as 🟩, C as caution). You can replicate this logic in dashboards or alerts by referencing `result.grade`.

## Signals & reasons

Each hit also exports:

- `reasons`: Human-readable reasoning (e.g., `"3 clean contractions"`, `"RS rank 88"`, `"Trend template pass"`).
- `signals`: Structured stats such as contraction count, max pullback, pivot, `ma_dist`, and RS rank so downstream consumers can highlight key edges.
- `rule_failures`: Empty for healthy hits; it includes entries such as `"missing_ohlcv"` when a placeholder record is emitted for a ticker with no data.
