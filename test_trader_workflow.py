import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_step(step):
    print(f"\n{'='*50}")
    print(f"STEP: {step}")
    print(f"{'='*50}")

def test_health():
    print_step("Checking System Health")
    try:
        res = requests.get(f"{BASE_URL}/docs")
        if res.status_code == 200:
            print("✅ System is Online")
        else:
            print(f"❌ System Offline: {res.status_code}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

def test_news():
    print_step("Checking Market News")
    try:
        res = requests.get(f"{BASE_URL}/api/news/general")
        if res.status_code == 200:
            data = res.json()
            print(f"✅ News API Functional. Found {len(data)} articles.")
        elif res.status_code == 404:
             print("⚠️ News API not found (Server restart required?)")
        else:
            print(f"❌ News API Error: {res.status_code}")
    except Exception as e:
        print(f"❌ News Check Failed: {e}")

def test_portfolio():
    print_step("Testing Portfolio Management")
    try:
        # Create
        payload = {"name": "Workflow Test Portfolio", "initial_capital": 50000, "user_id": 999}
        res = requests.post(f"{BASE_URL}/api/portfolio/create", json=payload)
        
        if res.status_code == 200:
            pid = res.json().get("portfolio_id")
            print(f"✅ Portfolio Created (ID: {pid})")
            
            # Add Position
            pos_payload = {
                "portfolio_id": pid,
                "symbol": "AAPL",
                "quantity": 10,
                "entry_price": 150.0
            }
            res = requests.post(f"{BASE_URL}/api/portfolio/position/add", json=pos_payload)
            if res.status_code == 200:
                print("✅ Position Added (AAPL)")
            else:
                print(f"❌ Add Position Failed: {res.status_code}")
                
        elif res.status_code == 404:
            print("⚠️ Portfolio API not found (Server restart required?)")
        else:
            print(f"❌ Create Portfolio Failed: {res.status_code}")
            
    except Exception as e:
        print(f"❌ Portfolio Test Failed: {e}")

def test_backtest():
    print_step("Testing Backtest Engine")
    try:
        payload = {
            "strategy": "VCP_Breakout",
            "symbol": "NVDA",
            "start_date": "2024-01-01",
            "initial_capital": 100000
        }
        res = requests.post(f"{BASE_URL}/api/backtest/run", json=payload)
        
        if res.status_code == 200:
            data = res.json()
            if data.get("success"):
                metrics = data.get("metrics", {})
                print(f"✅ Backtest Successful. Return: {metrics.get('total_return_pct')}%")
            else:
                print(f"❌ Backtest Logic Failed: {data.get('detail')}")
        elif res.status_code == 404:
            print("⚠️ Backtest API not found (Server restart required?)")
        else:
            print(f"❌ Backtest API Error: {res.status_code}")
            
    except Exception as e:
        print(f"❌ Backtest Check Failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Trader Workflow Verification...")
    test_health()
    test_news()
    test_portfolio()
    test_backtest()
    print("\n✅ Verification Complete")
