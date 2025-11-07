# Pattern Detector Integration Guide

## Quick Start

### 1. Basic Usage

```python
from app.core.detectors.vcp_detector import VCPDetector
from app.core.detectors.cup_handle_detector import CupHandleDetector
import pandas as pd

# Load your market data
ohlcv = pd.DataFrame({
    'open': [...],
    'high': [...],
    'low': [...],
    'close': [...],
    'volume': [...],
    'datetime': [...]
})

# Create detector instances
vcp = VCPDetector()
cup = CupHandleDetector()

# Find patterns
vcp_results = vcp.find(ohlcv, timeframe='1D', symbol='AAPL')
cup_results = cup.find(ohlcv, timeframe='1D', symbol='AAPL')

# Process results
for pattern in vcp_results:
    if pattern.strong:
        print(f"Strong {pattern.pattern_type}: confidence {pattern.confidence:.2f}")
        print(f"  Breakout at ${pattern.breakout['price']:.2f}")
```

### 2. Integrate with Existing Pattern Detection API

Add to `app/api/patterns.py`:

```python
from app.core.detectors.vcp_detector import VCPDetector
from app.core.detectors.cup_handle_detector import CupHandleDetector

# In your pattern detection endpoint:
async def detect_pattern(request: PatternRequest):
    # ... existing code ...

    # Add new detector results alongside existing PatternResult
    vcp_detector = VCPDetector()
    cup_detector = CupHandleDetector()

    # Run new detectors
    vcp_patterns = vcp_detector.find(ohlcv_df, request.interval, ticker)
    cup_patterns = cup_detector.find(ohlcv_df, request.interval, ticker)

    # Combine with existing results or return separately
    all_patterns = [result] + vcp_patterns + cup_patterns

    # Return with highest confidence pattern
    if all_patterns:
        best = max(all_patterns, key=lambda x: x.confidence if hasattr(x, 'confidence') else 0)
        return best
```

### 3. Configuration Overrides

```python
# Stricter VCP detection (fewer false signals)
vcp_strict = VCPDetector(
    MIN_CONTRACTIONS=4,  # Require 4+ contractions
    SHRINK_RATIO_THRESHOLD=0.70,  # Tighter ratio
    VOLUME_SURGE_Z=2.5  # Higher volume threshold
)

# Looser Cup & Handle detection (catch more setups)
cup_loose = CupHandleDetector(
    ROUNDEDNESS_MIN_SCORE=0.65,  # Lower smoothness requirement
    HANDLE_PULLBACK_RATIO=0.90  # Allow deeper handles
)

patterns = vcp_strict.find(ohlcv, '1D', 'AAPL')
```

---

## Integration Paths

### Option A: Parallel Detection (Recommended for Phase 1)

Run all detectors independently, return combined results:

```python
async def detect_all_patterns(ohlcv: pd.DataFrame, symbol: str, tf: str):
    detectors = [
        VCPDetector(),
        CupHandleDetector(),
        # Add more detectors as they're implemented
    ]

    all_results = []
    for detector in detectors:
        patterns = detector.find(ohlcv, tf, symbol)
        all_results.extend(patterns)

    # Deduplicate and sort by confidence
    unique = ResultDeduplicator.deduplicate(all_results)
    return sorted(unique, key=lambda x: x.confidence, reverse=True)
```

### Option B: Selector Pattern (Phase 2+)

Route to best detector based on market conditions:

```python
async def detect_best_pattern(ohlcv: pd.DataFrame, symbol: str, tf: str):
    # Analyze market condition
    volatility = calculate_volatility(ohlcv)
    trend = calculate_trend(ohlcv)

    # Choose detector based on condition
    if high_volatility and low_trend:
        detector = VCPDetector()  # VCP works well in consolidations
    elif high_trend and low_volatility:
        detector = TriangleDetector()  # Triangle (when implemented)
    else:
        detector = CupHandleDetector()  # Cup & Handle default

    patterns = detector.find(ohlcv, tf, symbol)
    return patterns[0] if patterns else None
```

### Option C: Ensemble (Phase 3+)

Combine predictions from multiple detectors:

```python
async def ensemble_detection(ohlcv: pd.DataFrame, symbol: str, tf: str):
    vcp = VCPDetector()
    cup = CupHandleDetector()

    vcp_results = vcp.find(ohlcv, tf, symbol)
    cup_results = cup.find(ohlcv, tf, symbol)

    # Ensemble voting: pattern type must be consistent across detectors
    # Example: if both VCP and Cup show pattern in overlapping window
    # → high confidence setup

    return aggregate_results(vcp_results, cup_results)
```

---

## Data Format Requirements

### Input DataFrame

```python
ohlcv = pd.DataFrame({
    'open': [float],      # Opening price
    'high': [float],      # High price
    'low': [float],       # Low price
    'close': [float],     # Closing price
    'volume': [int],      # Volume in shares
    'datetime': [datetime]  # OHLCV datetime (ISO8601 or pandas datetime)
})
```

### Output (PatternResult)

```python
{
    "symbol": str,              # "AAPL"
    "timeframe": str,           # "1D"
    "asof": str,                # ISO8601 timestamp
    "pattern_type": str,        # "VCP (Volatility Contraction)"
    "strong": bool,             # True if confidence >= 0.75
    "confidence": float,        # 0.0 to 1.0
    "window_start": str,        # ISO8601 date
    "window_end": str,          # ISO8601 date
    "lines": dict,              # Pattern geometry
    "touches": dict,            # Touch counts
    "breakout": dict,           # Breakout info (if applicable)
    "evidence": dict            # Metrics used in scoring
}
```

---

## Dashboard Integration

### Add to Dashboard Tabs

```html
<!-- Pattern Analysis Tab -->
<div id="patterns" class="tab-content">
    <h2>🎯 Advanced Pattern Analysis</h2>

    <div class="form-group">
        <input type="text" id="patternTicker" placeholder="Ticker (e.g., NVDA)">
        <select id="patternType">
            <option value="all">All Patterns</option>
            <option value="vcp">VCP (Volatility Contraction)</option>
            <option value="cup_handle">Cup & Handle</option>
            <option value="strong_only">Strong Patterns Only (≥0.75)</option>
        </select>
        <button onclick="analyzePatterns()">Analyze</button>
    </div>

    <div id="patternResult" class="result"></div>
</div>
```

### Dashboard JavaScript

```javascript
async function analyzePatterns() {
    const ticker = document.getElementById('patternTicker').value.toUpperCase();
    const patternType = document.getElementById('patternType').value;

    try {
        const response = await fetch(API_BASE + '/api/patterns/detect-advanced', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker, pattern_type: patternType })
        });

        const data = await response.json();

        if (data.success && data.patterns.length > 0) {
            let html = `<h3>Found ${data.patterns.length} pattern(s):</h3>`;

            data.patterns.forEach((p, i) => {
                const badge = p.strong ? '⭐ STRONG' : '⚠️ Medium';
                html += `<div class="pattern-card">
                    <h4>${badge} ${p.pattern_type}</h4>
                    <p>Confidence: ${(p.confidence * 100).toFixed(1)}%</p>
                    <p>Window: ${p.window_start} → ${p.window_end}</p>
                    <p>Breakout: ${p.breakout?.direction?.toUpperCase() || 'N/A'} @ $${p.breakout?.price?.toFixed(2) || 'N/A'}</p>
                    <details>
                        <summary>Evidence</summary>
                        <pre>${JSON.stringify(p.evidence, null, 2)}</pre>
                    </details>
                </div>`;
            });

            resultEl.innerHTML = html;
            resultEl.classList.add('success');
        } else {
            showResult('patternResult', 'No patterns detected', false);
        }
    } catch (error) {
        showResult('patternResult', 'Error: ' + error.message, true);
    }
}
```

---

## Testing Your Integration

### Unit Test Template

```python
import pytest
from app.core.detectors.vcp_detector import VCPDetector
import pandas as pd
import numpy as np

def test_vcp_detects_valid_pattern():
    """Test VCP detection with synthetic data"""
    # Create synthetic VCP: 3+ shrinking contractions
    data = create_synthetic_vcp_pattern()

    detector = VCPDetector()
    results = detector.find(data, '1D', 'TEST')

    assert len(results) > 0
    assert results[0].strong or results[0].confidence > 0.60

def test_vcp_rejects_false_signals():
    """Test VCP rejects non-VCP patterns"""
    # Create random noise
    data = create_random_price_data()

    detector = VCPDetector()
    results = detector.find(data, '1D', 'TEST')

    assert len(results) == 0 or all(r.confidence < 0.50 for r in results)
```

### Integration Test

```python
async def test_pattern_api_endpoint():
    """Test pattern detection API endpoint"""
    response = await client.post(
        '/api/patterns/detect-advanced',
        json={"ticker": "AAPL", "pattern_type": "vcp"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "patterns" in data
    assert isinstance(data["patterns"], list)

    if len(data["patterns"]) > 0:
        pattern = data["patterns"][0]
        assert "pattern_type" in pattern
        assert "confidence" in pattern
        assert "strong" in pattern
```

---

## Performance Optimization

### Caching

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_vcp_detection(symbol: str, tf: str, data_hash: str):
    """Cache pattern detection results"""
    # Load data and detect
    detector = VCPDetector()
    return detector.find(ohlcv, tf, symbol)

# Usage:
data_hash = hashlib.md5(str(ohlcv.tail(50).values).encode()).hexdigest()
results = cached_vcp_detection('AAPL', '1D', data_hash)
```

### Batch Processing

```python
async def scan_universe(symbols: List[str], tf: str = '1D'):
    """Scan multiple symbols for patterns"""
    vcp = VCPDetector()
    results = {}

    for symbol in symbols:
        try:
            ohlcv = await fetch_market_data(symbol, tf)
            patterns = vcp.find(ohlcv, tf, symbol)
            results[symbol] = patterns
        except Exception as e:
            logger.warning(f"Error scanning {symbol}: {e}")
            results[symbol] = []

    # Filter strong patterns only
    strong = {s: p for s, p in results.items() if p and p[0].strong}
    return strong
```

---

## Configuration in Production

### Environment Variables

```bash
# .env or Railway environment
VCP_MIN_CONTRACTIONS=4
VCP_SHRINK_RATIO=0.70
VCP_VOLUME_SURGE_Z=2.5

CUP_ROUNDEDNESS_SCORE=0.80
CUP_HANDLE_RATIO=0.85
```

### Runtime Override

```python
# Load from environment
import os

vcp_config = {
    'MIN_CONTRACTIONS': int(os.getenv('VCP_MIN_CONTRACTIONS', 3)),
    'SHRINK_RATIO_THRESHOLD': float(os.getenv('VCP_SHRINK_RATIO', 0.75)),
}

vcp = VCPDetector(**vcp_config)
```

---

## Next Steps

1. **Test the detectors** with your market data
2. **Integrate into API** endpoint
3. **Add to dashboard** for manual review
4. **Monitor results** and tune thresholds
5. **Implement other detectors** (Triangle, Channel, Wedge, etc.)
6. **Add backtesting** to validate performance

---

**Questions?** See `PATTERN_DETECTION_IMPROVEMENTS.md` for detailed algorithm documentation.
