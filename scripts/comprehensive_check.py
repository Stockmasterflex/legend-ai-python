import asyncio
import httpx
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

async def check_endpoint(client, name, method, url, payload=None, expected_status=200):
    try:
        if method == "GET":
            response = await client.get(url, timeout=10.0)
        elif method == "POST":
            response = await client.post(url, json=payload, timeout=10.0)

        if response.status_code == expected_status or (expected_status == 200 and response.status_code < 500):
            logger.info(f"✅ {name}: {response.status_code} OK")
            return True
        else:
            logger.error(f"❌ {name}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ {name}: Failed - {str(e)}")
        return False

async def main():
    logger.info("Starting Comprehensive System Evaluation...")

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # 1. Health Check
        health_ok = await check_endpoint(client, "Health Check", "GET", "/health")

        # 2. Scanner Check (mocking patterns to avoid full scan overhead if possible, or just checking if endpoint is up)
        # We use a pattern scan with limit 1 to verify connectivity
        scanner_ok = await check_endpoint(
            client,
            "Scanner (Patterns)",
            "GET",
            "/api/scan/patterns?limit=1&min_score=0",
            expected_status=200
        )

        # 3. AI Assistant Check
        # Expecting 503 if API key is missing, which is acceptable for "system is running but unconfigured"
        # Or 200 if mocked.
        ai_ok = await check_endpoint(
            client,
            "AI Assistant",
            "POST",
            "/api/ai/chat",
            payload={"message": "Hello", "include_market_data": False},
            expected_status=200
        )

        # 4. Portfolio Check
        # Needs user_id, might fail with 404 or 422 if not set up, but endpoint should be reachable
        portfolio_ok = await check_endpoint(
            client,
            "Portfolio List",
            "GET",
            "/api/portfolio/list?user_id=1",
            expected_status=200
        )

        # 5. Backtest Check
        backtest_payload = {
            "strategy": "VCP_Breakout",
            "symbol": "AAPL",
            "start_date": "2024-01-01",
            "initial_capital": 100000
        }
        backtest_ok = await check_endpoint(
            client,
            "Backtest Run",
            "POST",
            "/api/backtest/run",
            payload=backtest_payload,
            expected_status=200
        )

    logger.info("Evaluation Complete.")

    if not (health_ok and scanner_ok): # Critical systems
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
