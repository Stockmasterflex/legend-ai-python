import requests
import json
import sys

BASE_URL = "https://legend-ai-python-production.up.railway.app"

def test_journal():
    print("Testing Trade Journal...")
    
    # 1. Log a Trade
    print("1. Logging a trade for NVDA...")
    payload = {
        "ticker": "NVDA",
        "pattern": "VCP",
        "entry_date": "2025-11-29",
        "entry_price": 485.00,
        "stop_price": 465.00,
        "target_price": 525.00,
        "shares": 50,
        "notes": "Clean VCP setup with volume dry-up"
    }
    trade_id = None
    try:
        r = requests.post(f"{BASE_URL}/api/journal/trade", json=payload)
        print(f"Log Status: {r.status_code}")
        print(f"Log Response: {r.text}")
        if r.status_code in [200, 201]:
            data = r.json()
            trade_id = data.get("id")
            print(f"Logged Trade ID: {trade_id}")
        else:
            print("FAILED to log trade")
    except Exception as e:
        print(f"Error logging: {e}")

    if not trade_id:
        print("Skipping remaining tests due to log failure")
        return

    # 2. List Trades
    print("\n2. Listing trades...")
    try:
        r = requests.get(f"{BASE_URL}/api/journal/trades")
        print(f"List Status: {r.status_code}")
        trades = r.json()
        print(f"Total trades: {len(trades)}")
        found = False
        for t in trades:
            if t.get("id") == trade_id:
                found = True
                print("Found logged trade!")
                break
        if not found:
            print("FAILED: Logged trade not found in list")
    except Exception as e:
        print(f"Error listing: {e}")

    # 3. Close Trade
    print("\n3. Closing trade...")
    close_payload = {
        "exit_date": "2025-12-05",
        "exit_price": 510.00,
        "status": "Closed"
    }
    try:
        r = requests.put(f"{BASE_URL}/api/journal/trade/{trade_id}", json=close_payload)
        print(f"Close Status: {r.status_code}")
        print(f"Close Response: {r.text}")
    except Exception as e:
        print(f"Error closing: {e}")

    # 4. Get Stats
    print("\n4. Getting stats...")
    try:
        r = requests.get(f"{BASE_URL}/api/journal/stats")
        print(f"Stats Status: {r.status_code}")
        if r.status_code == 200:
            stats = r.json()
            print(f"Stats: {json.dumps(stats, indent=2)}")
            if stats.get("total_trades") > 0:
                print("SUCCESS: Stats returned correctly")
            else:
                print("WARNING: Stats show 0 trades?")
    except Exception as e:
        print(f"Error getting stats: {e}")

    # 5. Export CSV
    print("\n5. Exporting CSV...")
    try:
        r = requests.get(f"{BASE_URL}/api/journal/export")
        print(f"Export Status: {r.status_code}")
        if r.status_code == 200:
            content = r.text
            lines = content.splitlines()
            print(f"CSV Lines: {len(lines)}")
            if len(lines) > 1:
                print("SUCCESS: CSV exported with data")
            else:
                print("WARNING: CSV empty or header only")
    except Exception as e:
        print(f"Error exporting: {e}")

if __name__ == "__main__":
    test_journal()
