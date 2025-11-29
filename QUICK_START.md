# 🚀 Quick Start - Bulkowski Pattern Detection

## Running the Tests

```bash
cd /Users/kyleholthaus/Projects/legend-ai-python
PYTHONPATH=/Users/kyleholthaus/Projects/legend-ai-python python tests/test_bulkowski_integration.py
```

Expected output:
```
✓ PatternData creation
✓ FindAllTops
✓ FindAllBottoms
✓ CheckNearness
✓ Cup detection
✓ Double Bottom detection
✓ Full Bulkowski detector
✓ Data conversion

=== ALL TESTS PASSED ===
```

## Using in Python

```python
from app.core.bulkowski.detector import get_bulkowski_detector

# Sample data
ohlcv_data = {
    'o': [100, 102, 101, ...],  # Opens
    'h': [105, 106, 104, ...],  # Highs
    'l': [99, 100, 99, ...],    # Lows
    'c': [103, 104, 102, ...],  # Closes
    'v': [1M, 2M, 1.5M, ...],   # Volumes
}

# Detect patterns
detector = get_bulkowski_detector()
patterns = detector.detect_all_patterns(ohlcv_data, ticker="AAPL")

# Print results
for p in patterns:
    print(f"{p['pattern']}: {p['score']}/10")
    print(f"  Entry: ${p['entry']:.2f}")
    print(f"  Stop: ${p['stop']:.2f}")
    print(f"  Target: ${p['target']:.2f}")
    print(f"  R/R: {p['risk_reward']:.2f}:1")
```

## Using via API

```bash
# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test endpoint
curl -X POST http://localhost:8000/api/patterns/detect \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "interval": "1day",
    "use_bulkowski": true
  }'
```

## Available Patterns

Currently implemented:
1. **Cup & Handle** - Bullish continuation, 35-325 day formation
2. **Double Bottom** - Bullish reversal, Adam/Eve variants
   - Adam-Adam: Both sharp V-shaped
   - Eve-Eve: Both rounded U-shaped
   - Adam-Eve: First sharp, second rounded
   - Eve-Adam: First rounded, second sharp
3. **Ascending Triangle** - Bullish continuation, flat top + rising lows
4. **Descending Triangle** - Bearish continuation, flat bottom + falling highs
5. **Symmetrical Triangle** - Neutral consolidation, converging trendlines

## Helper Functions

All ported from Patternz:
- `find_all_tops()` - Find validated peaks
- `find_all_bottoms()` - Find validated troughs
- `check_nearness()` - Price similarity checking
- `check_confirmation()` - Breakout validation
- `find_bottom_spike_length()` - Adam vs Eve classification

## File Structure

```
app/core/bulkowski/
├── __init__.py              # Exports
├── helpers.py               # Core helper functions
├── detector.py              # Main detector class
└── patterns/
    ├── cup_handle.py        # Cup & Handle
    ├── double_bottoms.py    # Double Bottoms
    └── triangles.py         # All triangles
```

## Configuration

```python
# Strict mode (tighter tolerances)
detector = get_bulkowski_detector(strict=True)

# Normal mode (recommended)
detector = get_bulkowski_detector(strict=False)
```

## Troubleshooting

**No patterns detected?**
- Need 100+ bars of data (200+ recommended)
- Some patterns are rare
- Try different stocks (NVDA, TSLA, AAPL known to have patterns)

**Import errors?**
- Set PYTHONPATH: `export PYTHONPATH=/path/to/legend-ai-python`

**Tests failing?**
- Make sure numpy is installed: `pip install numpy pandas`

## Next Steps

1. Run tests to verify installation
2. Test API endpoint with real stocks
3. Integrate into scanning pipeline
4. Monitor pattern detection rates
5. Port additional patterns as needed

## Documentation

- Full diagnosis: `/DIAGNOSIS.md`
- Implementation details: `/IMPLEMENTATION_SUMMARY.md`
- Original source: `/patternz_source/Patternz/FindPatterns.cs`

