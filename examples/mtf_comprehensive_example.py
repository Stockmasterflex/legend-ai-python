"""
Comprehensive MTF System Example
Demonstrates the usage of the Multi-Timeframe Trading System

Features:
1. Timeframe Alignment (Daily, Weekly, Monthly)
2. MTF Dashboard with side-by-side charts and indicators
3. MTF Scoring (0-10 scale)
4. Entry Timing Optimization
5. Divergence Detection
6. Alignment Alerts

Usage:
    python examples/mtf_comprehensive_example.py
"""
import asyncio
import logging
from app.services.mtf_comprehensive import get_comprehensive_mtf_service

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def example_basic_analysis():
    """Example 1: Basic MTF Analysis"""
    print("\n" + "=" * 100)
    print("EXAMPLE 1: Basic MTF Analysis")
    print("=" * 100)

    service = get_comprehensive_mtf_service()

    # Analyze a stock
    ticker = "NVDA"
    result = await service.analyze_comprehensive(ticker)

    # Print summary
    print(f"\n📊 MTF Analysis Summary for {ticker}")
    print(f"   Score: {result.mtf_score.overall_score}/10 ({result.mtf_score.category})")
    print(f"   Recommendation: {result.trade_recommendation}")
    print(f"   Alignment: {result.alignment.alignment_type}")
    print(f"   Entry Signal: {result.entry_timing.current_signal.signal_type.upper()}")
    print(f"   Alerts: {len(result.alerts)} active")

    # Print detailed summary
    print(f"\n📋 Detailed Summary:")
    for key, value in result.summary.items():
        print(f"   {key}: {value}")


async def example_full_dashboard():
    """Example 2: Generate and Display Full Dashboard"""
    print("\n" + "=" * 100)
    print("EXAMPLE 2: Full MTF Dashboard")
    print("=" * 100)

    service = get_comprehensive_mtf_service()

    # Analyze with dashboard
    ticker = "AAPL"
    result = await service.analyze_comprehensive(ticker)

    # Display full dashboard
    dashboard_text = service.dashboard_generator.format_dashboard_text(result.dashboard)
    print(dashboard_text)


async def example_alignment_detection():
    """Example 3: Alignment Detection and Alerts"""
    print("\n" + "=" * 100)
    print("EXAMPLE 3: Alignment Detection")
    print("=" * 100)

    service = get_comprehensive_mtf_service()

    # Analyze multiple stocks for alignment
    tickers = ["NVDA", "TSLA", "AAPL", "MSFT"]

    for ticker in tickers:
        result = await service.analyze_comprehensive(ticker)

        print(f"\n{ticker}:")
        print(f"  Alignment: {result.alignment.alignment_type.replace('_', ' ').title()}")
        print(f"  Bullish TFs: {', '.join(result.alignment.bullish_timeframes) or 'None'}")
        print(f"  Bearish TFs: {', '.join(result.alignment.bearish_timeframes) or 'None'}")
        print(f"  MTF Score: {result.mtf_score.overall_score}/10")

        # Show critical alerts
        critical_alerts = [a for a in result.alerts if a.severity.value in ["critical", "high"]]
        if critical_alerts:
            print(f"  🚨 {len(critical_alerts)} High-Priority Alerts:")
            for alert in critical_alerts[:3]:  # Show top 3
                print(f"     • {alert.title}")


async def example_entry_timing():
    """Example 4: Entry Timing Optimization"""
    print("\n" + "=" * 100)
    print("EXAMPLE 4: Entry Timing Optimization")
    print("=" * 100)

    service = get_comprehensive_mtf_service()

    ticker = "TSLA"
    result = await service.analyze_comprehensive(ticker)

    signal = result.entry_timing.current_signal

    print(f"\n🎯 Entry Timing for {ticker}")
    print(f"   Optimal Entry TF: {result.entry_timing.optimal_entry_tf}")
    print(f"   Signal Type: {signal.signal_type.upper()}")
    print(f"   Confidence: {signal.confidence:.0%}")

    if signal.signal_type != "wait":
        print(f"\n   Entry Details:")
        print(f"     Entry Price: ${signal.entry_price:.2f}")
        print(f"     Stop Loss: ${signal.stop_loss:.2f}")
        print(f"     Take Profit: ${signal.take_profit:.2f}")
        print(f"     Risk:Reward: {signal.risk_reward_ratio:.2f}")
        print(f"     Reason: {signal.entry_reason}")

        print(f"\n   Confirmation Status:")
        print(f"     Higher TF Confirmed: {'✅' if signal.higher_tf_confirmed else '❌'}")
        print(f"     Volume Confirmed: {'✅' if signal.volume_confirmed else '❌'}")
        print(f"     Pattern Confirmed: {'✅' if signal.pattern_confirmed else '❌'}")

    # Show timing notes
    if result.entry_timing.timing_notes:
        print(f"\n   Timing Notes:")
        for note in result.entry_timing.timing_notes:
            print(f"     {note}")

    # Show wait conditions
    if result.entry_timing.wait_for:
        print(f"\n   ⏳ Wait For:")
        for condition in result.entry_timing.wait_for:
            print(f"     • {condition}")


async def example_divergence_detection():
    """Example 5: Divergence Detection"""
    print("\n" + "=" * 100)
    print("EXAMPLE 5: Divergence Detection")
    print("=" * 100)

    service = get_comprehensive_mtf_service()

    ticker = "SPY"
    result = await service.analyze_comprehensive(ticker)

    print(f"\n🔄 Divergence Analysis for {ticker}")

    if result.divergences:
        print(f"   Found {len(result.divergences)} divergence(s):")
        for div in result.divergences:
            print(f"\n   • {div.description}")
            print(f"     Type: {div.divergence_type.upper()}")
            print(f"     Severity: {div.severity.upper()}")
            print(f"     Timeframes: {', '.join(div.timeframes_involved)}")
            print(f"     Confirmation: {div.confirmation_score:.0%}")
    else:
        print("   No divergences detected")

    # Check for divergence alerts
    div_alerts = [a for a in result.alerts if a.alert_type.value == "divergence"]
    if div_alerts:
        print(f"\n   🔔 Divergence Alerts:")
        for alert in div_alerts:
            print(f"     {alert.title}")
            print(f"     {alert.message}")


async def example_mtf_scoring():
    """Example 6: MTF Scoring Breakdown"""
    print("\n" + "=" * 100)
    print("EXAMPLE 6: MTF Scoring Breakdown")
    print("=" * 100)

    service = get_comprehensive_mtf_service()

    ticker = "MSFT"
    result = await service.analyze_comprehensive(ticker)

    print(f"\n📊 MTF Scoring for {ticker}")
    print(f"   Overall Score: {result.mtf_score.overall_score}/10 ({result.mtf_score.category})")

    print(f"\n   Score Breakdown:")
    for component, score in result.mtf_score.score_breakdown.items():
        bar_length = int(score) if score >= 0 else 0
        bar = "█" * bar_length + "░" * (10 - bar_length)
        print(f"     {component:<18}: {score:>5.1f}/10 |{bar}|")

    print(f"\n   Scoring Notes:")
    for note in result.mtf_score.scoring_notes:
        print(f"     {note}")


async def example_complete_report():
    """Example 7: Complete MTF Report"""
    print("\n" + "=" * 100)
    print("EXAMPLE 7: Complete MTF Report")
    print("=" * 100)

    service = get_comprehensive_mtf_service()

    ticker = "NVDA"
    result = await service.analyze_comprehensive(ticker)

    # Generate full report
    report = service.format_comprehensive_report(result, include_dashboard=True)

    print(report)


async def example_multiple_stocks_scan():
    """Example 8: Scan Multiple Stocks for Best Setups"""
    print("\n" + "=" * 100)
    print("EXAMPLE 8: Multi-Stock MTF Scan")
    print("=" * 100)

    service = get_comprehensive_mtf_service()

    # Scan watchlist
    watchlist = ["NVDA", "AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "META"]

    print(f"\n🔍 Scanning {len(watchlist)} stocks for best MTF setups...\n")

    results = []

    for ticker in watchlist:
        try:
            result = await service.analyze_comprehensive(ticker)
            results.append({
                "ticker": ticker,
                "score": result.mtf_score.overall_score,
                "category": result.mtf_score.category,
                "alignment": result.alignment.alignment_type,
                "signal": result.entry_timing.current_signal.signal_type,
                "confidence": result.entry_timing.current_signal.confidence,
                "alerts": len([a for a in result.alerts if a.severity.value in ["critical", "high"]])
            })
        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {e}")

    # Sort by score (best first)
    results.sort(key=lambda x: x["score"], reverse=True)

    print(f"{'Rank':<6} {'Ticker':<8} {'Score':<12} {'Category':<12} {'Alignment':<20} {'Signal':<10} {'Alerts':<8}")
    print("-" * 90)

    for i, r in enumerate(results, 1):
        alignment_short = r['alignment'].replace('_', ' ').title()[:18]
        print(
            f"{i:<6} "
            f"{r['ticker']:<8} "
            f"{r['score']:.1f}/10{'':<5} "
            f"{r['category']:<12} "
            f"{alignment_short:<20} "
            f"{r['signal'].upper():<10} "
            f"{r['alerts']:<8}"
        )

    print(f"\n🎯 Top 3 Best Setups:")
    for i, r in enumerate(results[:3], 1):
        print(f"   {i}. {r['ticker']}: {r['score']:.1f}/10 - {r['category']} - {r['signal'].upper()} signal")


async def main():
    """Run all examples"""
    print("\n" + "=" * 100)
    print("COMPREHENSIVE MTF SYSTEM - EXAMPLES")
    print("=" * 100)
    print("\nDemonstrating the comprehensive Multi-Timeframe Trading System")
    print("This system provides:")
    print("  1. Timeframe Alignment Analysis (Daily, Weekly, Monthly)")
    print("  2. MTF Dashboard with Indicators and Patterns")
    print("  3. MTF Scoring System (0-10 scale)")
    print("  4. Entry Timing Optimization")
    print("  5. Divergence Detection")
    print("  6. Automated Alerts")
    print("\n" + "=" * 100)

    # Run examples
    await example_basic_analysis()
    await example_alignment_detection()
    await example_entry_timing()
    await example_divergence_detection()
    await example_mtf_scoring()
    await example_multiple_stocks_scan()

    # Optionally run the full dashboard and report (commented out as they're verbose)
    # await example_full_dashboard()
    # await example_complete_report()

    print("\n" + "=" * 100)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 100)
    print("\nTo see full dashboard or report, uncomment the relevant examples in main()")


if __name__ == "__main__":
    asyncio.run(main())
