#!/usr/bin/env python3
"""
Performance Baseline Establishment
Measures baseline performance metrics for critical endpoints
"""

import asyncio
import aiohttp
import time
import statistics
import json
from typing import List, Dict, Any
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


class PerformanceBaseline:
    """Establishes performance baselines for critical endpoints"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {}

    async def measure_endpoint(
        self,
        session: aiohttp.ClientSession,
        method: str,
        endpoint: str,
        iterations: int = 100,
        **kwargs
    ) -> Dict[str, Any]:
        """Measure performance of a single endpoint"""

        response_times = []
        status_codes = []
        errors = 0

        for i in range(iterations):
            start = time.perf_counter()
            try:
                async with session.request(
                    method,
                    f"{self.base_url}{endpoint}",
                    **kwargs
                ) as response:
                    await response.text()
                    end = time.perf_counter()

                    response_time = (end - start) * 1000  # Convert to ms
                    response_times.append(response_time)
                    status_codes.append(response.status)

            except Exception as e:
                errors += 1
                print(f"Error on iteration {i}: {str(e)}")

            # Small delay to avoid overwhelming the server
            await asyncio.sleep(0.01)

        # Calculate statistics
        if response_times:
            return {
                "endpoint": endpoint,
                "method": method,
                "iterations": iterations,
                "errors": errors,
                "min_ms": min(response_times),
                "max_ms": max(response_times),
                "mean_ms": statistics.mean(response_times),
                "median_ms": statistics.median(response_times),
                "stdev_ms": statistics.stdev(response_times) if len(response_times) > 1 else 0,
                "p95_ms": statistics.quantiles(response_times, n=20)[18] if len(response_times) >= 20 else max(response_times),
                "p99_ms": statistics.quantiles(response_times, n=100)[98] if len(response_times) >= 100 else max(response_times),
                "success_rate": (iterations - errors) / iterations * 100,
            }
        else:
            return {
                "endpoint": endpoint,
                "method": method,
                "iterations": iterations,
                "errors": errors,
                "error": "All requests failed"
            }

    async def run_baseline_tests(self):
        """Run baseline performance tests on all critical endpoints"""

        print("=" * 60)
        print(f"Performance Baseline Test - {datetime.now()}")
        print(f"Target: {self.base_url}")
        print("=" * 60)
        print()

        async with aiohttp.ClientSession() as session:
            # Test 1: Health Check
            print("Testing /health endpoint...")
            self.results["health"] = await self.measure_endpoint(
                session, "GET", "/health", iterations=100
            )

            # Test 2: Version
            print("Testing /api/version endpoint...")
            self.results["version"] = await self.measure_endpoint(
                session, "GET", "/api/version", iterations=100
            )

            # Test 3: Watchlist
            print("Testing /api/watchlist endpoint...")
            self.results["watchlist"] = await self.measure_endpoint(
                session, "GET", "/api/watchlist", iterations=100
            )

            # Test 4: Analyze (with params)
            print("Testing /api/analyze endpoint...")
            self.results["analyze"] = await self.measure_endpoint(
                session, "GET", "/api/analyze?ticker=AAPL&interval=1d", iterations=50
            )

            # Test 5: Scan (limited)
            print("Testing /api/scan endpoint...")
            self.results["scan"] = await self.measure_endpoint(
                session, "GET", "/api/scan?limit=5", iterations=20
            )

            # Test 6: Detailed Health
            print("Testing /health/detailed endpoint...")
            self.results["health_detailed"] = await self.measure_endpoint(
                session, "GET", "/health/detailed", iterations=50
            )

            # Test 7: Market Quote
            print("Testing /api/market/quote endpoint...")
            self.results["market_quote"] = await self.measure_endpoint(
                session, "GET", "/api/market/quote?ticker=AAPL", iterations=50
            )

    def print_results(self):
        """Print baseline results in a formatted table"""

        print("\n" + "=" * 60)
        print("PERFORMANCE BASELINE RESULTS")
        print("=" * 60)
        print()

        # Print header
        print(f"{'Endpoint':<30} {'Mean':<10} {'Median':<10} {'P95':<10} {'P99':<10}")
        print("-" * 60)

        # Print each endpoint
        for name, result in self.results.items():
            if "error" not in result:
                print(
                    f"{result['endpoint']:<30} "
                    f"{result['mean_ms']:<10.1f} "
                    f"{result['median_ms']:<10.1f} "
                    f"{result['p95_ms']:<10.1f} "
                    f"{result['p99_ms']:<10.1f}"
                )

        print()
        print("Detailed Statistics:")
        print()

        for name, result in self.results.items():
            if "error" not in result:
                print(f"{result['endpoint']}:")
                print(f"  Min:         {result['min_ms']:.1f} ms")
                print(f"  Max:         {result['max_ms']:.1f} ms")
                print(f"  Mean:        {result['mean_ms']:.1f} ms")
                print(f"  Median:      {result['median_ms']:.1f} ms")
                print(f"  Std Dev:     {result['stdev_ms']:.1f} ms")
                print(f"  P95:         {result['p95_ms']:.1f} ms")
                print(f"  P99:         {result['p99_ms']:.1f} ms")
                print(f"  Success:     {result['success_rate']:.1f}%")
                print(f"  Iterations:  {result['iterations']}")
                print()

    def save_results(self, filename: str = "tests/load/results/baseline.json"):
        """Save results to JSON file"""

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        data = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "results": self.results
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Results saved to: {filename}")

    def check_thresholds(self):
        """Check if performance meets acceptable thresholds"""

        print("\n" + "=" * 60)
        print("THRESHOLD CHECKS")
        print("=" * 60)
        print()

        thresholds = {
            "health": {"p95_ms": 100, "p99_ms": 200},
            "version": {"p95_ms": 100, "p99_ms": 200},
            "watchlist": {"p95_ms": 500, "p99_ms": 1000},
            "analyze": {"p95_ms": 2000, "p99_ms": 5000},
            "scan": {"p95_ms": 5000, "p99_ms": 10000},
            "health_detailed": {"p95_ms": 500, "p99_ms": 1000},
            "market_quote": {"p95_ms": 1000, "p99_ms": 2000},
        }

        all_passed = True

        for name, threshold in thresholds.items():
            if name in self.results:
                result = self.results[name]

                if "error" in result:
                    print(f"❌ {name}: FAILED - {result['error']}")
                    all_passed = False
                    continue

                p95_pass = result["p95_ms"] <= threshold["p95_ms"]
                p99_pass = result["p99_ms"] <= threshold["p99_ms"]

                status = "✅" if (p95_pass and p99_pass) else "❌"

                print(f"{status} {name}:")
                print(f"   P95: {result['p95_ms']:.1f} ms (threshold: {threshold['p95_ms']} ms) {'✓' if p95_pass else '✗'}")
                print(f"   P99: {result['p99_ms']:.1f} ms (threshold: {threshold['p99_ms']} ms) {'✓' if p99_pass else '✗'}")

                if not (p95_pass and p99_pass):
                    all_passed = False

        print()

        if all_passed:
            print("✅ All performance thresholds met!")
            return True
        else:
            print("❌ Some performance thresholds exceeded!")
            return False


async def main():
    """Main entry point"""

    base_url = os.getenv("BASE_URL", "http://localhost:8000")

    baseline = PerformanceBaseline(base_url)
    await baseline.run_baseline_tests()
    baseline.print_results()
    baseline.save_results()

    passed = baseline.check_thresholds()

    return 0 if passed else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
