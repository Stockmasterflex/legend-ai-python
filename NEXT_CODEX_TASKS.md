# Next Codex Tasks - Priority Queue

## ✅ Completed by Claude (Tasks 1-5)
- ✅ Task 1: MMU/VCP Pattern (Minervini's signature pattern)
- ✅ Task 2: High Tight Flag (explosive breakout pattern)
- ✅ Task 3: Bull/Bear Flags & Pennants
- ✅ Task 4: Rising/Falling Wedges
- ✅ Task 5: Integration complete (all patterns working)

## 🔄 Completed by Codex (Tasks 1-7)
- ✅ Task 1: Candlestick Patterns (105 patterns)
- ✅ Task 2: Single-Day Patterns (15 patterns)
- ✅ Task 3: Filter System
- ✅ Task 4: Export System
- ✅ Task 5: Scoring System
- ✅ Task 6: Scanner Integration
- ✅ Task 7: API Endpoints

---

## 🎯 NEXT: Advanced Chart Patterns (Codex Tasks #8-12)

### Task #8: Triple Tops/Bottoms ⭐⭐⭐⭐
**Priority:** HIGH  
**Estimated Time:** 3-4 hours

```prompt
Port Triple Bottoms and Triple Tops from FindPatterns.cs

Create: /app/core/pattern_engine/patterns/triple_formations.py

Requirements:
1. Extract FindTripleBottoms() from FindPatterns.cs (search for "private static void FindTripleBottoms")
2. Extract FindTripleTops() from FindPatterns.cs (search for "private static void FindTripleTops")
3. Port the logic to Python
4. Follow the same structure as mmu_vcp.py and flags.py

Pattern Recognition:
- Find 3 bottoms at approximately same price level
- Verify nearness tolerance (use helpers.check_nearness)
- Confirm each bottom is separated by meaningful peaks
- Calculate breakout target (measure move from pattern height)

Structure:
```python
def find_triple_bottoms(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False
) -> List[Dict[str, Any]]:
    """Find Triple Bottom patterns"""
    # Implementation
    pass

def find_triple_tops(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False
) -> List[Dict[str, Any]]:
    """Find Triple Top patterns"""
    # Implementation
    pass
```

Create tests: /tests/test_triple_formations.py

Add imports to:
- /app/core/pattern_engine/patterns/__init__.py
- /app/core/pattern_engine/detector.py (add to detect_all_patterns method)
```

---

### Task #9: Head & Shoulders ⭐⭐⭐⭐⭐
**Priority:** CRITICAL  
**Estimated Time:** 4-6 hours

```prompt
Port Head & Shoulders Top and Bottom patterns from FindPatterns.cs

Create: /app/core/pattern_engine/patterns/head_shoulders.py

Requirements:
1. Extract FindHeadShouldersTop() from FindPatterns.cs
2. Extract FindHeadShouldersBottom() from FindPatterns.cs
3. Port both classic and complex variants

Pattern Recognition:
Head & Shoulders Top:
- Find left shoulder (peak)
- Find head (higher peak)
- Find right shoulder (peak similar to left)
- Draw neckline through troughs
- Calculate downside target (head to neckline distance)

Head & Shoulders Bottom (Inverse):
- Find left shoulder (trough)
- Find head (lower trough)
- Find right shoulder (trough similar to left)
- Draw neckline through peaks
- Calculate upside target

Structure:
```python
def find_head_shoulders_top(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False
) -> List[Dict[str, Any]]:
    """Find Head & Shoulders Top patterns"""
    pass

def find_head_shoulders_bottom(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False
) -> List[Dict[str, Any]]:
    """Find Head & Shoulders Bottom (Inverse) patterns"""
    pass
```

Special Features:
- Include complex H&S (with multiple shoulders)
- Validate neckline slope
- Confirm volume characteristics (declining into head, surging on breakout)

Create tests: /tests/test_head_shoulders.py
```

---

### Task #10: Rectangle Patterns ⭐⭐⭐
**Priority:** MEDIUM  
**Estimated Time:** 3-4 hours

```prompt
Port Rectangle (consolidation box) patterns from FindPatterns.cs

Create: /app/core/pattern_engine/patterns/rectangles.py

Requirements:
1. Extract FindRectangles() from FindPatterns.cs
2. Support both bullish and bearish rectangles

Pattern Recognition:
- Find horizontal resistance (multiple touches at same level)
- Find horizontal support (multiple touches at same level)
- Verify price bounces between support and resistance
- Minimum duration (10+ bars)
- Breakout in either direction

Structure:
```python
def find_rectangles(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False
) -> List[Dict[str, Any]]:
    """Find Rectangle consolidation patterns"""
    pass
```

Create tests: /tests/test_rectangles.py
```

---

### Task #11: Channel Patterns ⭐⭐⭐
**Priority:** MEDIUM  
**Estimated Time:** 4-5 hours

```prompt
Port Channel patterns (ascending, descending, horizontal) from FindPatterns.cs

Create: /app/core/pattern_engine/patterns/channels.py

Requirements:
1. Extract FindChannels() from FindPatterns.cs
2. Support ascending, descending, and horizontal channels

Pattern Recognition:
- Find two parallel trendlines
- Upper line connects peaks
- Lower line connects troughs
- Price oscillates within channel
- Breakout signals trend change

Structure:
```python
def find_ascending_channel(...):
    """Find ascending channel patterns"""
    pass

def find_descending_channel(...):
    """Find descending channel patterns"""
    pass

def find_horizontal_channel(...):
    """Find horizontal channel patterns"""
    pass

def find_channels(...):
    """Find all channel types"""
    # Calls all 3 functions above
    pass
```

Create tests: /tests/test_channels.py
```

---

### Task #12: Broadening Formations ⭐⭐⭐
**Priority:** MEDIUM  
**Estimated Time:** 4-5 hours

```prompt
Port Broadening Formation patterns from FindPatterns.cs

Create: /app/core/pattern_engine/patterns/broadening.py

Requirements:
1. Extract FindBroadeningPatterns() from FindPatterns.cs
2. Support all 4 variants (top, bottom, ascending, descending)

Pattern Recognition:
- Find diverging trendlines (opposite of triangles)
- Volatility expands over time
- Higher highs AND lower lows
- Typically occurs at market tops (distribution)

4 Variants:
- Broadening Top (bearish)
- Broadening Bottom (bullish)
- Ascending Broadening Wedge
- Descending Broadening Wedge

Structure:
```python
def find_broadening_top(...):
    """Find broadening top patterns"""
    pass

def find_broadening_bottom(...):
    """Find broadening bottom patterns"""
    pass

def find_broadening_formations(...):
    """Find all broadening formation types"""
    pass
```

Create tests: /tests/test_broadening.py
```

---

## 🎯 How to Execute These Tasks

### For Each Task:

1. **Read Source Code**
   ```bash
   # Search for the pattern function
   grep -n "private static void FindTripleBottoms" patternz_source/Patternz/FindPatterns.cs -A 100
   ```

2. **Create Pattern File**
   - Copy structure from existing patterns (mmu_vcp.py, flags.py)
   - Port the C# logic to Python
   - Use numpy arrays for price data
   - Use helpers for FindAllTops/Bottoms

3. **Return Format**
   ```python
   {
       'pattern': 'Pattern Name',
       'type': 'PATTERN_CODE',
       'confidence': 0.75,  # 0-1 scale
       'score': 7.5,  # 0-10 scale
       'entry': 100.00,
       'stop': 95.00,
       'target': 110.00,
       'risk_reward': 2.0,
       'width': 25,  # bars
       'height': 10.00,  # price range
       'current_price': 98.00,
       'confirmed': True,
       'metadata': {
           # Pattern-specific details
       }
   }
   ```

4. **Update Imports**
   - Add to `/app/core/pattern_engine/patterns/__init__.py`
   - Add to `/app/core/pattern_engine/detector.py` in `detect_all_patterns()` method

5. **Create Tests**
   - Test with simulated OHLCV data
   - Verify pattern detection works
   - Check entry/stop/target calculations

6. **Run Tests**
   ```bash
   pytest tests/test_triple_formations.py -v
   ```

---

## 📊 Progress Tracking

| Task | Pattern | Status | Priority | ETA |
|------|---------|--------|----------|-----|
| #8 | Triple Tops/Bottoms | 🔜 Queued | HIGH | 3-4h |
| #9 | Head & Shoulders | 🔜 Queued | CRITICAL | 4-6h |
| #10 | Rectangles | 🔜 Queued | MEDIUM | 3-4h |
| #11 | Channels | 🔜 Queued | MEDIUM | 4-5h |
| #12 | Broadening | 🔜 Queued | MEDIUM | 4-5h |

**Total Estimated Time:** 18-24 hours  
**Recommended Approach:** Parallel execution (all 5 tasks at once if possible)

---

## 🎓 Tips for Success

1. **Follow Existing Patterns**
   - Look at `mmu_vcp.py` and `flags.py` for structure
   - Copy the function signatures
   - Use the same return format

2. **Use Helpers Effectively**
   ```python
   # Find peaks
   tops = helpers.find_all_tops(high, trade_days=5)
   
   # Find troughs
   bottoms = helpers.find_all_bottoms(low, trade_days=5)
   
   # Check nearness
   is_near = helpers.check_nearness(price1, price2, tolerance=0.03)
   ```

3. **Calculate Proper Levels**
   - Entry: Breakout point (resistance for bullish, support for bearish)
   - Stop: Invalidation level (below support or above resistance)
   - Target: Measured move (pattern height from breakout)

4. **Confidence Scoring**
   - Base: 0.7 for confirmed pattern
   - +0.05 for each bonus criteria met
   - Max: 1.0

5. **Test Thoroughly**
   - Create synthetic data for testing
   - Verify all edge cases
   - Check that patterns don't overlap incorrectly

---

## 🚀 After Tasks #8-12 Complete

Next phase will be:
- **Harmonic Patterns** (Gartley, Bat, Butterfly, Crab, Shark)
- **Candlestick Enhancements** (scoring, combos, confirmation)
- **Professional Features** (forecast, backtest, seasonality, relative strength)

But for now, focus on getting Tasks #8-12 done! 🎯

---

**Questions? Check existing code in:**
- `/app/core/pattern_engine/patterns/mmu_vcp.py`
- `/app/core/pattern_engine/patterns/flags.py`
- `/app/core/pattern_engine/patterns/wedges.py`
- `/app/core/pattern_engine/detector.py`

