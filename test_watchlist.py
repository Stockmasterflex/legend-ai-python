import requests
import json
import sys

BASE_URL = "https://legend-ai-python-production.up.railway.app"

def test_watchlist():
    print("Testing Watchlist CRUD...")
    
    # 1. Add to Watchlist
    print("1. Adding NVDA to watchlist...")
    payload = {
        "ticker": "NVDA",
        "reason": "VCP setup forming - test entry",
        "target_entry": 485.00,
        "target_stop": 465.00,
        "target_price": 525.00,
        "status": "Watching"
    }
    try:
        r = requests.post(f"{BASE_URL}/api/watchlist/add", json=payload)
        print(f"Add Status: {r.status_code}")
        print(f"Add Response: {r.text}")
        if r.status_code not in [200, 201]:
            print("FAILED to add to watchlist")
            # Continue anyway to see if it was already there
    except Exception as e:
        print(f"Error adding: {e}")

    # 2. List Watchlist
    print("\n2. Listing watchlist...")
    try:
        r = requests.get(f"{BASE_URL}/api/watchlist")
        print(f"List Status: {r.status_code}")
        items = r.json()
        print(f"Items count: {len(items)}")
        found = False
        for item in items:
            if item.get("ticker") == "NVDA":
                found = True
                print("Found NVDA in watchlist!")
                break
        if not found:
            print("NVDA NOT found in watchlist")
    except Exception as e:
        print(f"Error listing: {e}")

    # 3. Update Watchlist
    print("\n3. Updating NVDA...")
    update_payload = {
        "status": "Breaking Out",
        "notes": "Price crossed entry with volume"
    }
    try:
        r = requests.put(f"{BASE_URL}/api/watchlist/NVDA", json=update_payload)
        print(f"Update Status: {r.status_code}")
        print(f"Update Response: {r.text}")
    except Exception as e:
        print(f"Error updating: {e}")

    # 4. Remove from Watchlist
    print("\n4. Removing NVDA...")
    try:
        r = requests.delete(f"{BASE_URL}/api/watchlist/remove/NVDA")
        print(f"Remove Status: {r.status_code}")
        print(f"Remove Response: {r.text}")
    except Exception as e:
        print(f"Error removing: {e}")

    # 5. Verify Removal
    print("\n5. Verifying removal...")
    try:
        r = requests.get(f"{BASE_URL}/api/watchlist")
        items = r.json()
        found = False
        for item in items:
            if item.get("ticker") == "NVDA":
                found = True
                break
        if found:
            print("FAILED: NVDA still in watchlist")
        else:
            print("SUCCESS: NVDA removed from watchlist")
    except Exception as e:
        print(f"Error verifying: {e}")

if __name__ == "__main__":
    test_watchlist()
