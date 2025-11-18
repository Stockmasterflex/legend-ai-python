"""
Trading Strategy Usage Examples

This module demonstrates how to use the trading strategies:
- Mark Minervini (SEPA, VCP, Stage Analysis)
- William O'Neil (CAN SLIM, Cup & Handle)
- Stan Weinstein (4-Stage Cycle)

Run each example to see how the strategies work with sample data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app.strategies import MinerviniStrategy, ONeilStrategy, WeinsteinStrategy


def generate_sample_data(days=500, trend='uptrend'):
    """
    Generate sample OHLCV data for testing

    Args:
        days: Number of days of data
        trend: 'uptrend', 'downtrend', 'sideways', or 'vcp'
    """
    dates = pd.date_range(end=datetime.now(), periods=days)

    if trend == 'uptrend':
        # Generate uptrending stock data
        close = 100 + np.cumsum(np.random.randn(days) * 2 + 0.3)
    elif trend == 'downtrend':
        close = 100 + np.cumsum(np.random.randn(days) * 2 - 0.3)
    elif trend == 'sideways':
        close = 100 + np.cumsum(np.random.randn(days) * 1)
    elif trend == 'vcp':
        # Generate VCP pattern
        close = []
        base_price = 100

        # Build up
        for i in range(100):
            base_price += np.random.randn() * 1 + 0.5
            close.append(base_price)

        # Contraction 1: -15%
        peak1 = base_price
        for i in range(30):
            base_price -= (peak1 * 0.15) / 30 + np.random.randn() * 0.5
            close.append(base_price)

        # Recovery
        for i in range(20):
            base_price += (peak1 - base_price) * 0.05 + np.random.randn() * 0.3
            close.append(base_price)

        # Contraction 2: -10%
        peak2 = base_price
        for i in range(25):
            base_price -= (peak2 * 0.10) / 25 + np.random.randn() * 0.3
            close.append(base_price)

        # Recovery
        for i in range(20):
            base_price += (peak2 - base_price) * 0.05 + np.random.randn() * 0.2
            close.append(base_price)

        # Contraction 3: -6%
        peak3 = base_price
        for i in range(20):
            base_price -= (peak3 * 0.06) / 20 + np.random.randn() * 0.2
            close.append(base_price)

        # Recovery and tight action
        for i in range(15):
            base_price += (peak3 - base_price) * 0.03 + np.random.randn() * 0.1
            close.append(base_price)

        # Fill remaining days
        remaining = days - len(close)
        for i in range(remaining):
            base_price += np.random.randn() * 0.5
            close.append(base_price)

        close = np.array(close)
    else:
        close = 100 + np.cumsum(np.random.randn(days))

    # Ensure positive prices
    close = np.maximum(close, 10)

    # Generate OHLC from close
    high = close + np.abs(np.random.randn(days) * 2)
    low = close - np.abs(np.random.randn(days) * 2)
    open_price = close + np.random.randn(days) * 1

    # Volume (higher on up days)
    base_volume = 1000000
    volume = base_volume + np.abs(np.random.randn(days) * 300000)
    # Increase volume on big moves
    price_change = np.abs(np.diff(close, prepend=close[0]))
    volume = volume * (1 + price_change / np.mean(price_change))

    df = pd.DataFrame({
        'datetime': dates,
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume.astype(int)
    })

    return df


# ========================================
# Example 1: Mark Minervini Strategy
# ========================================

def example_minervini():
    """Demonstrate Mark Minervini's SEPA methodology"""
    print("=" * 70)
    print("MARK MINERVINI STRATEGY EXAMPLE")
    print("=" * 70)

    # Initialize strategy
    minervini = MinerviniStrategy(
        risk_per_trade=0.01,      # 1% risk per trade
        max_stop_loss=0.10,       # 10% max stop loss
        min_rs_rating=70,         # Minimum RS rating
        account_size=100000       # $100k account
    )

    # Generate sample uptrending stock data with VCP pattern
    print("\n1. Generating sample stock data (VCP pattern)...")
    ohlcv = generate_sample_data(days=500, trend='vcp')
    print(f"   Loaded {len(ohlcv)} days of data")
    print(f"   Current Price: ${ohlcv['close'].iloc[-1]:.2f}")

    # Check Trend Template
    print("\n2. Checking Minervini Trend Template (8 criteria)...")
    trend_result = minervini.check_trend_template(ohlcv)

    print(f"\n   TREND TEMPLATE RESULTS:")
    print(f"   Overall Score: {trend_result.score}/8")
    print(f"   Passes: {'✓ YES' if trend_result.passes else '✗ NO'}")
    print(f"   Stage: {trend_result.stage.name}")
    print(f"\n   Individual Criteria:")
    for criterion, passes in trend_result.criteria.items():
        status = '✓' if passes else '✗'
        print(f"   {status} {criterion}")

    print(f"\n   Key Metrics:")
    print(f"   Current Price: ${trend_result.details['current_price']:.2f}")
    print(f"   50-day MA: ${trend_result.details['ma_50']:.2f}")
    print(f"   150-day MA: ${trend_result.details['ma_150']:.2f}")
    print(f"   200-day MA: ${trend_result.details['ma_200']:.2f}")
    print(f"   52-week High: ${trend_result.details['52_week_high']:.2f}")
    print(f"   52-week Low: ${trend_result.details['52_week_low']:.2f}")
    print(f"   Distance from High: {trend_result.details['distance_from_high_pct']:.1f}%")
    print(f"   RS Proxy: {trend_result.details['rs_proxy']:.0f}")

    # Analyze VCP
    print("\n3. Analyzing for VCP (Volatility Contraction Pattern)...")
    vcp = minervini.analyze_vcp(ohlcv)

    print(f"\n   VCP ANALYSIS:")
    print(f"   Is VCP: {'✓ YES' if vcp.is_vcp else '✗ NO'}")
    print(f"   Number of Contractions: {vcp.num_contractions}")
    print(f"   Contraction Sequence: {[f'{c:.1f}%' for c in vcp.contraction_sequence]}")
    print(f"   Final Contraction: {vcp.final_contraction_pct:.1f}%")
    print(f"   Volume Declining: {'✓ YES' if vcp.volume_declining else '✗ NO'}")
    print(f"   Breakout Imminent: {'✓ YES' if vcp.breakout_imminent else '✗ NO'}")
    print(f"   Pivot Price: ${vcp.pivot_price:.2f}")

    # Generate SEPA Signal
    print("\n4. Generating SEPA Entry Signal...")
    signal = minervini.generate_sepa_signal(
        ohlcv,
        symbol='EXAMPLE',
        fundamental_score=75  # Optional fundamental rating
    )

    if signal:
        print(f"\n   ✓ VALID SEPA SIGNAL FOUND!")
        print(f"\n   ENTRY DETAILS:")
        print(f"   Symbol: {signal.symbol}")
        print(f"   Entry Type: {signal.entry_type.upper()}")
        print(f"   Entry Price: ${signal.entry_price:.2f}")
        print(f"   Stop Loss: ${signal.stop_loss:.2f}")
        print(f"   Initial Target: ${signal.initial_target:.2f}")
        print(f"   Risk/Reward: {signal.risk_reward_ratio:.1f}:1")
        print(f"   Confidence: {signal.confidence:.0f}%")

        print(f"\n   POSITION SIZING:")
        print(f"   Position Size: {signal.position_size_pct:.1f}% of account")

        risk_pct = ((signal.entry_price - signal.stop_loss) / signal.entry_price) * 100
        print(f"   Risk per Share: ${signal.entry_price - signal.stop_loss:.2f} ({risk_pct:.1f}%)")

        print(f"\n   REASONS:")
        for i, reason in enumerate(signal.reasons, 1):
            print(f"   {i}. {reason}")
    else:
        print(f"\n   ✗ No valid SEPA signal found")
        print(f"   Possible reasons:")
        print(f"   - Not in Stage 2 uptrend")
        print(f"   - No valid entry setup (breakout or pullback)")
        print(f"   - Risk too high")

    # Calculate Position Size
    print("\n5. Position Sizing Example (1% Risk Rule)...")
    entry_price = 50.00
    stop_loss = 46.50  # 7% below entry

    position = minervini.calculate_position_size(entry_price, stop_loss)

    print(f"\n   Example Trade:")
    print(f"   Entry Price: ${entry_price:.2f}")
    print(f"   Stop Loss: ${stop_loss:.2f}")
    print(f"   Account Size: ${minervini.account_size:,.0f}")

    print(f"\n   Position Sizing:")
    print(f"   Shares to Buy: {position['shares']}")
    print(f"   Position Value: ${position['position_value']:,.2f}")
    print(f"   Position %: {position['position_pct']:.1f}% of account")
    print(f"   Risk per Share: ${position['risk_per_share']:.2f}")
    print(f"   Risk %: {position['risk_pct']:.1f}%")
    print(f"   Max Loss (if stopped out): ${position['max_loss']:,.2f} (1% of account)")

    print("\n" + "=" * 70 + "\n")


# ========================================
# Example 2: William O'Neil Strategy
# ========================================

def example_oneil():
    """Demonstrate William O'Neil's CAN SLIM methodology"""
    print("=" * 70)
    print("WILLIAM O'NEIL STRATEGY EXAMPLE")
    print("=" * 70)

    # Initialize strategy
    oneil = ONeilStrategy(
        min_volume_surge=0.40,  # 40% volume increase
        max_stop_loss=0.08,     # 8% max stop loss
        min_rs_rating=80        # Minimum RS rating
    )

    # Generate sample data
    print("\n1. Generating sample stock data...")
    ohlcv = generate_sample_data(days=500, trend='uptrend')
    print(f"   Loaded {len(ohlcv)} days of data")
    print(f"   Current Price: ${ohlcv['close'].iloc[-1]:.2f}")

    # Evaluate CAN SLIM
    print("\n2. Evaluating CAN SLIM Criteria...")

    # Sample fundamental data
    fundamentals = {
        'eps_growth_qoq': 50,      # 50% quarterly EPS growth
        'eps_growth_3yr': 35,      # 35% annual EPS growth
        'institutional_ownership_pct': 40,
        'shares_outstanding': 75_000_000
    }

    canslim = oneil.evaluate_canslim(ohlcv, fundamentals)

    print(f"\n   CAN SLIM SCORE: {canslim.total_score:.0f}/7")
    print(f"   Passes: {'✓ YES' if canslim.passes else '✗ NO'}")
    print(f"   Recommendation: {canslim.recommendation}")

    print(f"\n   Individual Criteria:")
    for criterion, passes in canslim.criteria.items():
        if passes is None:
            status = '⊘'
            result = 'N/A (no data)'
        elif passes:
            status = '✓'
            result = 'PASS'
        else:
            status = '✗'
            result = 'FAIL'
        print(f"   {status} {criterion}: {result}")

    print(f"\n   Details:")
    for key, value in canslim.details.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            print(f"   {key}: {value:.1f}")
        else:
            print(f"   {key}: {value}")

    # Detect Cup & Handle
    print("\n3. Detecting Cup & Handle Pattern...")
    cup_handle = oneil.detect_cup_and_handle(ohlcv)

    if cup_handle.found:
        print(f"\n   ✓ CUP & HANDLE FOUND!")
        print(f"\n   Pattern Details:")
        print(f"   Cup Depth: {cup_handle.cup_depth_pct:.1f}%")
        print(f"   Cup Length: {cup_handle.cup_length_bars} bars")
        print(f"   Handle Depth: {cup_handle.handle_depth_pct:.1f}%")
        print(f"   Quality Score: {cup_handle.quality_score:.0f}/100")
        print(f"   Is Valid: {'✓ YES' if cup_handle.is_valid else '✗ NO'}")

        print(f"\n   Entry Information:")
        print(f"   Pivot Price: ${cup_handle.pivot_price:.2f}")
        print(f"   Buy Point: ${cup_handle.buy_point:.2f}")
        print(f"   Ideal Buy Zone: ${cup_handle.buy_point:.2f} - ${cup_handle.ideal_buy_zone_high:.2f}")
    else:
        print(f"\n   ✗ No Cup & Handle pattern found")

    # Identify Breakout
    print("\n4. Identifying Breakout Signal...")
    breakout = oneil.identify_breakout(ohlcv, symbol='EXAMPLE')

    if breakout:
        print(f"\n   ✓ BREAKOUT SIGNAL FOUND!")
        print(f"\n   Breakout Details:")
        print(f"   Symbol: {breakout.symbol}")
        print(f"   Buy Point: ${breakout.buy_point:.2f}")
        print(f"   Stop Loss: ${breakout.stop_loss:.2f} ({((breakout.buy_point - breakout.stop_loss) / breakout.buy_point * 100):.1f}% risk)")
        print(f"   Volume Surge: +{breakout.volume_surge_pct:.0f}%")
        print(f"   Pattern Type: {breakout.pattern_type}")
        print(f"   Market Condition: {breakout.market_condition.name}")
        print(f"   Confidence: {breakout.confidence:.0f}%")

        print(f"\n   Reasons:")
        for i, reason in enumerate(breakout.reasons, 1):
            print(f"   {i}. {reason}")
    else:
        print(f"\n   ✗ No breakout signal found")
        print(f"   Wait for proper setup or check other stocks")

    # Follow-Through Day
    print("\n5. Detecting Follow-Through Day (Market Timing)...")
    ftd = oneil.detect_follow_through_day(ohlcv)

    print(f"\n   Follow-Through Day Analysis:")
    print(f"   Is FTD: {'✓ YES' if ftd.is_ftd else '✗ NO'}")
    if ftd.is_ftd:
        print(f"   Day Number: {ftd.day_number}")
        print(f"   Index Gain: +{ftd.index_gain_pct:.2f}%")
        print(f"   Volume vs Prior: {ftd.volume_vs_prior:.0%}")
        print(f"   Is Valid: {'✓ YES' if ftd.is_valid else '✗ NO'}")
    print(f"   Details: {ftd.details}")

    print("\n" + "=" * 70 + "\n")


# ========================================
# Example 3: Stan Weinstein Strategy
# ========================================

def example_weinstein():
    """Demonstrate Stan Weinstein's Stage Analysis methodology"""
    print("=" * 70)
    print("STAN WEINSTEIN STRATEGY EXAMPLE")
    print("=" * 70)

    # Initialize strategy
    weinstein = WeinsteinStrategy(
        use_weekly=False,       # Use daily charts with 150-day MA
        min_volume_surge=2.0,   # 2x volume
        ma_period=150           # 150-day MA (equivalent to 30-week)
    )

    # Generate sample data
    print("\n1. Generating sample stock data...")
    stock_ohlcv = generate_sample_data(days=500, trend='uptrend')
    market_ohlcv = generate_sample_data(days=500, trend='uptrend')  # S&P 500 proxy

    print(f"   Loaded {len(stock_ohlcv)} days of stock data")
    print(f"   Loaded {len(market_ohlcv)} days of market data")
    print(f"   Current Price: ${stock_ohlcv['close'].iloc[-1]:.2f}")

    # Analyze Stage
    print("\n2. Performing Stage Analysis...")
    stage_result = weinstein.analyze_stage(stock_ohlcv)

    print(f"\n   STAGE ANALYSIS RESULTS:")
    print(f"   Current Stage: {stage_result.stage.name}")
    print(f"   Sub-Stage: {stage_result.sub_stage}")
    print(f"   Confidence: {stage_result.confidence:.0f}%")

    print(f"\n   Moving Average Analysis:")
    print(f"   30-week MA: ${stage_result.ma_30w:.2f}")
    print(f"   MA Slope: {stage_result.ma_slope.upper()}")
    print(f"   Price vs MA: {stage_result.price_vs_ma.upper()}")
    print(f"   Volume Trend: {stage_result.volume_trend.upper()}")

    print(f"\n   Additional Details:")
    for key, value in stage_result.details.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            print(f"   {key}: {value:.2f}")
        else:
            print(f"   {key}: {value}")

    # Stage interpretation
    print(f"\n   STAGE INTERPRETATION:")
    if stage_result.stage.name == 'STAGE_1_BASING':
        print(f"   📊 Stock is in BASING phase (Stage 1)")
        print(f"   Action: Watch and wait. Consider small positions late in stage.")
        print(f"   Next: Wait for breakout to Stage 2")
    elif stage_result.stage.name == 'STAGE_2_ADVANCING':
        print(f"   📈 Stock is in UPTREND (Stage 2)")
        if stage_result.sub_stage == '2A':
            print(f"   Action: BUY AGGRESSIVELY - Early Stage 2 is best entry!")
        elif stage_result.sub_stage == '2B':
            print(f"   Action: Be cautious - Late Stage 2, consider taking profits")
        else:
            print(f"   Action: BUY on pullbacks to 30-week MA")
    elif stage_result.stage.name == 'STAGE_3_TOPPING':
        print(f"   📉 Stock is in TOPPING phase (Stage 3)")
        print(f"   Action: SELL - Take profits, reduce positions")
        print(f"   Next: Expect transition to Stage 4 decline")
    elif stage_result.stage.name == 'STAGE_4_DECLINING':
        print(f"   🔴 Stock is in DOWNTREND (Stage 4)")
        print(f"   Action: AVOID - Do not buy! Exit all positions")
        print(f"   Next: Wait for Stage 1 base to form")
    else:
        print(f"   🔄 Stock is in TRANSITION")
        print(f"   Action: Monitor closely for stage confirmation")

    # Calculate Mansfield RS
    print("\n3. Calculating Mansfield Relative Strength...")
    mansfield = weinstein.calculate_mansfield_rs(stock_ohlcv, market_ohlcv)

    print(f"\n   MANSFIELD RS RESULTS:")
    print(f"   Current Value: {mansfield.current_value:.2f}")
    print(f"   Direction: {mansfield.direction.upper()}")
    print(f"   Crosses Zero Line: {'✓ YES' if mansfield.crosses_zero_line else '✗ NO'}")
    print(f"   Is Strong: {'✓ YES' if mansfield.is_strong else '✗ NO'}")
    print(f"   Percentile Rank: {mansfield.percentile_rank:.0f}%")

    print(f"\n   Interpretation:")
    if mansfield.current_value > 0:
        print(f"   ✓ Stock is OUTPERFORMING the market")
    else:
        print(f"   ✗ Stock is UNDERPERFORMING the market")

    if mansfield.is_strong:
        print(f"   ✓ Strong momentum - Rising RS above zero line")
    elif mansfield.direction == 'rising':
        print(f"   ⚠ Improving - RS is rising")
    elif mansfield.direction == 'falling':
        print(f"   ⚠ Weakening - RS is falling")

    # Identify Stage 2 Breakout
    print("\n4. Identifying Stage 2 Breakout...")
    breakout = weinstein.identify_stage2_breakout(
        stock_ohlcv,
        symbol='EXAMPLE',
        market_ohlcv=market_ohlcv
    )

    if breakout:
        print(f"\n   ✓ STAGE 2 BREAKOUT SIGNAL FOUND!")
        print(f"\n   Breakout Details:")
        print(f"   Symbol: {breakout.symbol}")
        print(f"   Breakout Price: ${breakout.breakout_price:.2f}")
        print(f"   Entry Price: ${breakout.entry_price:.2f}")
        print(f"   Stop Loss: ${breakout.stop_loss:.2f}")

        risk_pct = ((breakout.entry_price - breakout.stop_loss) / breakout.entry_price) * 100
        print(f"   Risk: {risk_pct:.1f}%")

        print(f"\n   Confirmation:")
        print(f"   Volume Confirmed: {'✓ YES' if breakout.volume_confirmation else '✗ NO'}")
        print(f"   Volume vs Avg: {breakout.volume_vs_avg:.1f}x")
        print(f"   30-week MA: ${breakout.ma_30w:.2f}")
        print(f"   Mansfield RS: {breakout.mansfield_rs:.2f}")
        print(f"   Confidence: {breakout.confidence:.0f}%")

        print(f"\n   Reasons:")
        for i, reason in enumerate(breakout.reasons, 1):
            print(f"   {i}. {reason}")

        print(f"\n   Action Plan:")
        print(f"   1. Buy at ${breakout.entry_price:.2f} (just above breakout)")
        print(f"   2. Set stop loss at ${breakout.stop_loss:.2f}")
        print(f"   3. Hold while price stays above 30-week MA")
        print(f"   4. Exit if closes below 30-week MA or Stage changes")
    else:
        print(f"\n   ✗ No Stage 2 breakout signal found")
        print(f"   Possible reasons:")
        print(f"   - Not in Stage 2 or early transition")
        print(f"   - No breakout above resistance yet")
        print(f"   - Volume not confirmed")
        print(f"   - Risk too high")

    print("\n" + "=" * 70 + "\n")


# ========================================
# Example 4: Combined Strategy Approach
# ========================================

def example_combined():
    """Demonstrate how to combine all three strategies"""
    print("=" * 70)
    print("COMBINED STRATEGY EXAMPLE")
    print("=" * 70)
    print("\nBest Practice: Use elements from all three strategies!\n")

    # Initialize all strategies
    minervini = MinerviniStrategy(risk_per_trade=0.01, account_size=100000)
    oneil = ONeilStrategy(min_volume_surge=0.40)
    weinstein = WeinsteinStrategy(use_weekly=False, ma_period=150)

    # Generate data
    print("1. Generating sample data...")
    ohlcv = generate_sample_data(days=500, trend='vcp')
    market_ohlcv = generate_sample_data(days=500, trend='uptrend')

    symbol = 'COMBINED_EXAMPLE'
    print(f"   Analyzing: {symbol}")
    print(f"   Current Price: ${ohlcv['close'].iloc[-1]:.2f}")

    # Step 1: Weinstein Stage Filter
    print("\n2. Step 1: Weinstein Stage Filter")
    print("   " + "-" * 40)
    stage_result = weinstein.analyze_stage(ohlcv)
    print(f"   Stage: {stage_result.stage.name} ({stage_result.sub_stage})")

    if stage_result.stage.name != 'STAGE_2_ADVANCING':
        print(f"   ✗ REJECT - Not in Stage 2 uptrend")
        print(f"   Only buy stocks in Stage 2!")
        return
    else:
        print(f"   ✓ PASS - Stock in Stage 2 uptrend")

    # Step 2: O'Neil CAN SLIM Filter
    print("\n3. Step 2: O'Neil CAN SLIM Filter")
    print("   " + "-" * 40)
    fundamentals = {
        'eps_growth_qoq': 60,
        'eps_growth_3yr': 40,
        'institutional_ownership_pct': 35,
        'shares_outstanding': 50_000_000
    }
    canslim = oneil.evaluate_canslim(ohlcv, fundamentals)
    print(f"   CAN SLIM Score: {canslim.total_score:.0f}/7")

    if canslim.total_score < 5:
        print(f"   ✗ REJECT - CAN SLIM score too low")
        print(f"   Need at least 5/7 criteria met")
        return
    else:
        print(f"   ✓ PASS - Strong CAN SLIM fundamentals")

    # Step 3: Minervini VCP Entry
    print("\n4. Step 3: Minervini VCP Pattern")
    print("   " + "-" * 40)
    vcp = minervini.analyze_vcp(ohlcv)
    print(f"   VCP Found: {'✓ YES' if vcp.is_vcp else '✗ NO'}")

    if vcp.is_vcp:
        print(f"   ✓ PASS - VCP pattern present")
        print(f"   Contractions: {vcp.num_contractions}")
        print(f"   Final Contraction: {vcp.final_contraction_pct:.1f}%")
    else:
        print(f"   ⚠ WARNING - No VCP, but may still be valid")

    # Step 4: Generate Entry Signal
    print("\n5. Step 4: Generate Entry Signal (SEPA)")
    print("   " + "-" * 40)
    signal = minervini.generate_sepa_signal(ohlcv, symbol=symbol, fundamental_score=75)

    if signal:
        print(f"   ✓ VALID ENTRY SIGNAL FOUND!")
        print(f"\n   === TRADE PLAN ===")
        print(f"   Symbol: {signal.symbol}")
        print(f"   Entry: ${signal.entry_price:.2f} ({signal.entry_type})")
        print(f"   Stop Loss: ${signal.stop_loss:.2f}")
        print(f"   Target: ${signal.initial_target:.2f} (4R)")
        print(f"   Position Size: {signal.position_size_pct:.1f}% of account")
        print(f"   Confidence: {signal.confidence:.0f}%")

        print(f"\n   === SUPPORTING FACTORS ===")
        print(f"   ✓ Weinstein Stage 2 ({stage_result.sub_stage})")
        print(f"   ✓ CAN SLIM Score: {canslim.total_score}/7")
        if vcp.is_vcp:
            print(f"   ✓ VCP Pattern: {vcp.num_contractions} contractions")
        print(f"   ✓ Volume Trend: {stage_result.volume_trend}")

        print(f"\n   === RISK MANAGEMENT ===")
        risk_pct = ((signal.entry_price - signal.stop_loss) / signal.entry_price) * 100
        risk_dollars = (signal.entry_price - signal.stop_loss) * \
                      (minervini.account_size * 0.01) / (signal.entry_price - signal.stop_loss)
        print(f"   Max Risk: {risk_pct:.1f}% per share")
        print(f"   Max Loss: ${minervini.account_size * 0.01:,.0f} (1% of account)")
        print(f"   R:R Ratio: {signal.risk_reward_ratio:.1f}:1")

        print(f"\n   === EXIT STRATEGY ===")
        print(f"   1. Stop Loss: ${signal.stop_loss:.2f} (7-8% rule)")
        print(f"   2. Trailing Stop: Raise to 50-day MA as it rises")
        print(f"   3. Profit Target 1: ${signal.initial_target:.2f} (Take 25%)")
        print(f"   4. Profit Target 2: Let rest run with trailing stop")
        print(f"   5. Emergency Exit: Break below 30-week MA on volume")

    else:
        print(f"   ✗ No entry signal - wait for proper setup")

    print("\n" + "=" * 70 + "\n")


# ========================================
# Main Execution
# ========================================

if __name__ == "__main__":
    """Run all examples"""

    # Run individual strategy examples
    example_minervini()
    example_oneil()
    example_weinstein()

    # Run combined strategy example
    example_combined()

    print("\n" + "=" * 70)
    print("EXAMPLES COMPLETE")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Review docs/TRADING_STRATEGIES.md for detailed documentation")
    print("2. Test strategies with your own data")
    print("3. Backtest before using real money")
    print("4. Start with paper trading")
    print("5. Follow risk management rules strictly!")
    print("\n" + "=" * 70 + "\n")
