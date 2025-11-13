#!/usr/bin/env python3
"""Quick test to verify Phase 2 scanner endpoints work."""
import asyncio
import os
import sys

# Enable scanner for testing
os.environ["LEGEND_FLAGS_ENABLE_SCANNER"] = "1"

async def test_scanner():
    """Test scanner service directly."""
    from app.services.scanner import ScannerService

    print("🧪 Testing Scanner Service...")
    scanner = ScannerService()

    # Test with a small universe
    result = await scanner.run_daily_vcp_scan(
        universe=["AAPL", "NVDA", "TSLA"],
        limit=10
    )

    print(f"✅ Scanner returned {len(result.get('results', []))} results")
    print(f"   Universe size: {result.get('universe_size', 0)}")
    print(f"   Duration: {result.get('meta', {}).get('duration_ms', 0)}ms")

    if result.get("results"):
        print(f"\n📊 Sample Result:")
        sample = result["results"][0]
        print(f"   Symbol: {sample.get('symbol')}")
        print(f"   Pattern: {sample.get('pattern')}")
        print(f"   Score: {sample.get('score')}")

    return result

async def test_universe_store():
    """Test universe store."""
    from app.services.universe_store import universe_store

    print("\n🧪 Testing Universe Store...")

    # Seed if empty
    universe = await universe_store.get_all()
    if not universe:
        print("   Seeding universe...")
        await universe_store.seed()
        universe = await universe_store.get_all()

    print(f"✅ Universe has {len(universe)} symbols")

    if universe:
        sample = list(universe.keys())[0]
        print(f"   Sample: {sample} -> {universe[sample]}")

    return universe

async def main():
    print("🚀 Phase 2 Scanner Test\n" + "=" * 50)

    try:
        # Test universe first
        universe = await test_universe_store()

        # Test scanner
        if universe:
            scan_result = await test_scanner()

        print("\n✅ All tests passed!")
        return 0

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
