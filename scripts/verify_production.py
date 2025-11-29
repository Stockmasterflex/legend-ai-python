"""
Production API Test Suite
Tests all critical Legend AI endpoints
"""
import asyncio
import httpx
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://legend-ai-python-production.up.railway.app"
TIMEOUT = 30.0


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    END = "\033[0m"


def log_pass(msg):
    print(f"{Colors.GREEN}✅ PASS{Colors.END}: {msg}")


def log_fail(msg):
    print(f"{Colors.RED}❌ FAIL{Colors.END}: {msg}")


def log_warn(msg):
    print(f"{Colors.YELLOW}⚠️ WARN{Colors.END}: {msg}")


def log_info(msg):
    print(f"{Colors.BLUE}ℹ️ INFO{Colors.END}: {msg}")


async def test_endpoint(client, method, path, expected_status=200, name=None, json_data=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{path}"
    name = name or path
    
    try:
        if method == "GET":
            response = await client.get(url)
        elif method == "POST":
            response = await client.post(url, json=json_data or {})
        else:
            raise ValueError(f"Unknown method: {method}")
        
        if response.status_code == expected_status:
            log_pass(f"{name} ({response.status_code})")
            return True, response
        else:
            log_fail(f"{name} - Expected {expected_status}, got {response.status_code}")
            return False, response
    except httpx.TimeoutException:
        log_fail(f"{name} - Timeout")
        return False, None
    except Exception as e:
        log_fail(f"{name} - Error: {e}")
        return False, None


async def run_tests():
    """Run all production tests"""
    print("\n" + "=" * 60)
    print(f"🧪 Legend AI Production Test Suite")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 {BASE_URL}")
    print("=" * 60 + "\n")
    
    results = {"pass": 0, "fail": 0, "warn": 0}
    
    async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True) as client:
        
        # ==================== HEALTH CHECKS ====================
        print("\n📋 Health Checks\n" + "-" * 40)
        
        passed, resp = await test_endpoint(client, "GET", "/health", name="Health Check")
        if passed:
            results["pass"] += 1
            data = resp.json()
            log_info(f"Version: {data.get('version', 'unknown')}")
            log_info(f"Status: {data.get('status', 'unknown')}")
        else:
            results["fail"] += 1
        
        passed, _ = await test_endpoint(client, "GET", "/healthz", name="K8s Health")
        results["pass" if passed else "fail"] += 1
        
        # ==================== CORE APIs ====================
        print("\n📊 Core APIs\n" + "-" * 40)
        
        passed, _ = await test_endpoint(client, "GET", "/api/patterns/list", name="Pattern List")
        results["pass" if passed else "fail"] += 1
        
        passed, _ = await test_endpoint(client, "GET", "/api/universe/sp500", name="S&P 500 Universe")
        results["pass" if passed else "fail"] += 1
        
        passed, _ = await test_endpoint(client, "GET", "/api/market/status", name="Market Status")
        results["pass" if passed else "fail"] += 1
        
        # ==================== ANALYSIS ====================
        print("\n🔍 Analysis APIs\n" + "-" * 40)
        
        passed, _ = await test_endpoint(client, "GET", "/api/analyze?ticker=AAPL", name="Analyze AAPL")
        results["pass" if passed else "fail"] += 1
        
        passed, _ = await test_endpoint(client, "GET", "/api/patterns/detect?ticker=MSFT", name="Detect Patterns MSFT")
        results["pass" if passed else "fail"] += 1
        
        # ==================== NEWS (New Feature) ====================
        print("\n📰 News APIs (New)\n" + "-" * 40)
        
        passed, resp = await test_endpoint(client, "GET", "/api/news/general", name="General News")
        if passed:
            results["pass"] += 1
        elif resp and resp.status_code == 404:
            log_warn("News API not deployed yet")
            results["warn"] += 1
        else:
            results["fail"] += 1
        
        passed, resp = await test_endpoint(client, "GET", "/api/news/company/AAPL", name="Company News AAPL")
        if passed:
            results["pass"] += 1
        elif resp and resp.status_code == 404:
            log_warn("News Company API not deployed yet")
            results["warn"] += 1
        else:
            results["fail"] += 1
        
        # ==================== PORTFOLIO (New Feature) ====================
        print("\n💼 Portfolio APIs (New)\n" + "-" * 40)
        
        passed, resp = await test_endpoint(client, "GET", "/api/portfolio/list", name="Portfolio List")
        if passed:
            results["pass"] += 1
        elif resp and resp.status_code == 404:
            log_warn("Portfolio API not deployed yet")
            results["warn"] += 1
        else:
            results["fail"] += 1
        
        # ==================== BACKTEST (New Feature) ====================
        print("\n📈 Backtest APIs (New)\n" + "-" * 40)
        
        passed, resp = await test_endpoint(client, "GET", "/api/backtest/runs", name="Backtest Runs")
        if passed:
            results["pass"] += 1
        elif resp and resp.status_code == 404:
            log_warn("Backtest API not deployed yet")
            results["warn"] += 1
        else:
            results["fail"] += 1
        
        passed, resp = await test_endpoint(client, "GET", "/api/backtest/strategies", name="Backtest Strategies")
        if passed:
            results["pass"] += 1
        elif resp and resp.status_code == 404:
            log_warn("Backtest Strategies API not deployed yet")
            results["warn"] += 1
        else:
            results["fail"] += 1
        
        # ==================== AI CHAT ====================
        print("\n🤖 AI APIs\n" + "-" * 40)
        
        passed, _ = await test_endpoint(client, "GET", "/api/ai/status", name="AI Status")
        results["pass" if passed else "fail"] += 1
        
        # ==================== CACHE ====================
        print("\n💾 Cache APIs\n" + "-" * 40)
        
        passed, _ = await test_endpoint(client, "GET", "/api/cache/health", name="Cache Health")
        results["pass" if passed else "fail"] += 1
        
        # ==================== ALERTS ====================
        print("\n🔔 Alert APIs\n" + "-" * 40)
        
        passed, _ = await test_endpoint(client, "GET", "/api/alerts/health", name="Alerts Health")
        results["pass" if passed else "fail"] += 1
        
    # ==================== SUMMARY ====================
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"{Colors.GREEN}Passed: {results['pass']}{Colors.END}")
    print(f"{Colors.RED}Failed: {results['fail']}{Colors.END}")
    print(f"{Colors.YELLOW}Warnings: {results['warn']}{Colors.END}")
    
    total = results["pass"] + results["fail"]
    if total > 0:
        success_rate = (results["pass"] / total) * 100
        print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    if results["fail"] > 0:
        print(f"\n{Colors.RED}⚠️ Some tests failed! Check the output above.{Colors.END}")
        return 1
    elif results["warn"] > 0:
        print(f"\n{Colors.YELLOW}ℹ️ All critical tests passed, but some new features not deployed yet.{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.GREEN}🎉 All tests passed!{Colors.END}")
        return 0


if __name__ == "__main__":
    exit_code = asyncio.run(run_tests())
    sys.exit(exit_code)
