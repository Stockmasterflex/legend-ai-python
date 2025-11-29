import requests
import json
import sys

BASE_URL = "https://legend-ai-python-production.up.railway.app"

def test_trade_planner():
    print("Testing Trade Planner...")
    
    # 1. Calculate Position Size
    print("1. Calculating position size for NVDA...")
    payload = {
        "ticker": "NVDA",
        "pattern": "VCP",
        "entry": 485.00,
        "stop": 465.00,
        "target": 525.00,
        "account_size": 100000,
        "risk_percent": 1.0
    }
    try:
        r = requests.post(f"{BASE_URL}/api/trade/plan", json=payload)
        print(f"Plan Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Plan Response: {json.dumps(data, indent=2)}")
            
            # Verify calculations
            risk_per_share = 485 - 465 # 20
            expected_shares = (100000 * 0.01) / 20 # 50
            
            if data.get("position_size") == 50:
                print("SUCCESS: Position size calculation correct (50 shares)")
            else:
                print(f"FAILED: Position size mismatch. Expected 50, got {data.get('position_size')}")
                
            if data.get("risk_amount") == 1000.0:
                print("SUCCESS: Risk amount correct ($1000)")
            else:
                print(f"FAILED: Risk amount mismatch. Expected 1000, got {data.get('risk_amount')}")
                
        else:
            print(f"FAILED: Plan request failed with {r.status_code}: {r.text}")
    except Exception as e:
        print(f"Error planning: {e}")

    # 2. Test Edge Cases
    print("\n2. Testing Edge Cases...")
    
    # High concentration
    print("  - High concentration warning...")
    payload_conc = {
        "entry": 10.00,
        "stop": 9.50,
        "target": 12.00,
        "account_size": 10000,
        "risk_percent": 1.0
    }
    try:
        r = requests.post(f"{BASE_URL}/api/trade/plan", json=payload_conc)
        if r.status_code == 200:
            data = r.json()
            warnings = data.get("warnings", [])
            print(f"    Warnings: {warnings}")
            if any("concentration" in w.lower() for w in warnings):
                print("    SUCCESS: Concentration warning triggered")
            else:
                print("    FAILED: No concentration warning")
    except Exception as e:
        print(f"    Error: {e}")

    # Low R:R
    print("  - Low R:R warning...")
    payload_rr = {
        "entry": 100.00,
        "stop": 95.00,
        "target": 104.00,
        "account_size": 100000,
        "risk_percent": 1.0
    }
    try:
        r = requests.post(f"{BASE_URL}/api/trade/plan", json=payload_rr)
        if r.status_code == 200:
            data = r.json()
            warnings = data.get("warnings", [])
            print(f"    Warnings: {warnings}")
            if any("reward/risk" in w.lower() for w in warnings):
                print("    SUCCESS: Low R:R warning triggered")
            else:
                print("    FAILED: No Low R:R warning")
    except Exception as e:
        print(f"    Error: {e}")

if __name__ == "__main__":
    test_trade_planner()
