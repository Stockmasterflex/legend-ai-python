"""
Legend AI - Load Testing with Locust
Tests all critical endpoints under load to find bottlenecks and establish baselines
"""

from locust import HttpUser, task, between, events
import random
import json
from datetime import datetime


# Sample tickers for testing
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "AMD",
    "NFLX", "DIS", "BA", "JPM", "GS", "V", "MA", "PYPL",
    "SHOP", "SQ", "COIN", "RBLX"
]


class LegendAIUser(HttpUser):
    """Simulates a typical Legend AI user"""

    # Wait 1-3 seconds between tasks (realistic user behavior)
    wait_time = between(1, 3)

    def on_start(self):
        """Called when a user starts"""
        print(f"User {self.environment.runner.user_count} started")

    @task(10)
    def health_check(self):
        """Test health endpoint - highest frequency"""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")

    @task(5)
    def get_version(self):
        """Test version endpoint"""
        with self.client.get("/api/version", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if "version" in data or "build_sha" in data:
                    response.success()
                else:
                    response.failure("Missing version data")
            else:
                response.failure(f"Version check failed: {response.status_code}")

    @task(8)
    def analyze_ticker(self):
        """Test pattern analysis endpoint"""
        ticker = random.choice(TICKERS)

        with self.client.get(
            f"/api/analyze?ticker={ticker}&interval=1d",
            catch_response=True,
            name="/api/analyze"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "ticker" in data or "patterns" in data:
                        response.success()
                    else:
                        response.failure("Invalid response structure")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            elif response.status_code == 422:
                # Validation error is acceptable
                response.success()
            else:
                response.failure(f"Analysis failed: {response.status_code}")

    @task(3)
    def scan_universe(self):
        """Test universe scan endpoint - slower, less frequent"""
        with self.client.get(
            "/api/scan?limit=10",
            catch_response=True,
            name="/api/scan"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list) or "results" in data:
                        response.success()
                    else:
                        response.failure("Invalid scan response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            elif response.status_code == 422:
                response.success()
            else:
                response.failure(f"Scan failed: {response.status_code}")

    @task(6)
    def get_watchlist(self):
        """Test watchlist endpoint"""
        with self.client.get("/api/watchlist", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        response.success()
                    else:
                        response.failure("Invalid watchlist response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Watchlist failed: {response.status_code}")

    @task(4)
    def add_to_watchlist(self):
        """Test adding to watchlist"""
        ticker = random.choice(TICKERS)

        with self.client.post(
            "/api/watchlist/add",
            json={
                "symbol": ticker,
                "reason": "Load test",
                "tags": ["test"]
            },
            catch_response=True,
            name="/api/watchlist/add"
        ) as response:
            if response.status_code in [200, 201, 409]:  # 409 = already exists
                response.success()
            else:
                response.failure(f"Add to watchlist failed: {response.status_code}")

    @task(2)
    def get_chart(self):
        """Test chart generation endpoint"""
        ticker = random.choice(TICKERS)

        with self.client.get(
            f"/api/charts/{ticker}",
            catch_response=True,
            name="/api/charts/{ticker}"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 422:
                response.success()
            else:
                response.failure(f"Chart failed: {response.status_code}")

    @task(3)
    def get_market_quote(self):
        """Test market quote endpoint"""
        ticker = random.choice(TICKERS)

        with self.client.get(
            f"/api/market/quote?ticker={ticker}",
            catch_response=True,
            name="/api/market/quote"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "symbol" in data or "price" in data:
                        response.success()
                    else:
                        response.failure("Invalid quote response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Quote failed: {response.status_code}")

    @task(1)
    def get_detailed_health(self):
        """Test detailed health endpoint - least frequent"""
        with self.client.get("/health/detailed", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "status" in data:
                        response.success()
                    else:
                        response.failure("Invalid health response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Detailed health failed: {response.status_code}")


class HeavyUser(HttpUser):
    """Simulates a power user who does expensive operations"""

    wait_time = between(2, 5)

    @task(5)
    def full_universe_scan(self):
        """Test full universe scan - very expensive"""
        with self.client.get(
            "/api/scan?limit=50",
            catch_response=True,
            name="/api/scan?limit=50"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 422:
                response.success()
            else:
                response.failure(f"Full scan failed: {response.status_code}")

    @task(3)
    def analyze_multiple_tickers(self):
        """Analyze multiple tickers in sequence"""
        for _ in range(3):
            ticker = random.choice(TICKERS)
            with self.client.get(
                f"/api/analyze?ticker={ticker}&interval=1d",
                catch_response=True,
                name="/api/analyze (batch)"
            ) as response:
                if response.status_code not in [200, 422]:
                    response.failure(f"Batch analysis failed: {response.status_code}")


# Event listeners for metrics collection
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when test starts"""
    print(f"\n{'='*60}")
    print(f"Load Test Started: {datetime.now()}")
    print(f"Target: {environment.host}")
    print(f"{'='*60}\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when test stops - print summary"""
    stats = environment.stats

    print(f"\n{'='*60}")
    print(f"Load Test Completed: {datetime.now()}")
    print(f"{'='*60}")
    print(f"\nSummary Statistics:")
    print(f"  Total Requests: {stats.total.num_requests}")
    print(f"  Total Failures: {stats.total.num_failures}")
    print(f"  Failure Rate: {stats.total.fail_ratio * 100:.2f}%")
    print(f"  Median Response Time: {stats.total.median_response_time} ms")
    print(f"  95th Percentile: {stats.total.get_response_time_percentile(0.95)} ms")
    print(f"  99th Percentile: {stats.total.get_response_time_percentile(0.99)} ms")
    print(f"  Average Response Time: {stats.total.avg_response_time:.2f} ms")
    print(f"  Min Response Time: {stats.total.min_response_time} ms")
    print(f"  Max Response Time: {stats.total.max_response_time} ms")
    print(f"  Requests per Second: {stats.total.total_rps:.2f}")
    print(f"\nTop 10 Slowest Endpoints:")

    # Sort by average response time
    sorted_stats = sorted(
        [(name, endpoint) for name, endpoint in stats.entries.items()],
        key=lambda x: x[1].avg_response_time,
        reverse=True
    )[:10]

    for name, endpoint in sorted_stats:
        print(f"  {name[0]}: {endpoint.avg_response_time:.0f} ms (median: {endpoint.median_response_time} ms)")

    print(f"\n{'='*60}\n")

    # Write results to file
    with open("tests/load/results/load_test_results.txt", "a") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Load Test: {datetime.now()}\n")
        f.write(f"{'='*60}\n")
        f.write(f"Total Requests: {stats.total.num_requests}\n")
        f.write(f"Total Failures: {stats.total.num_failures}\n")
        f.write(f"Failure Rate: {stats.total.fail_ratio * 100:.2f}%\n")
        f.write(f"Median Response Time: {stats.total.median_response_time} ms\n")
        f.write(f"95th Percentile: {stats.total.get_response_time_percentile(0.95)} ms\n")
        f.write(f"99th Percentile: {stats.total.get_response_time_percentile(0.99)} ms\n")
        f.write(f"Requests per Second: {stats.total.total_rps:.2f}\n")
        f.write(f"\n")
