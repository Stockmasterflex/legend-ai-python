#!/usr/bin/env python3
"""Test Chart-IMG API with the fixed payload"""
import httpx
import asyncio

async def test_chartimg():
    api_key = "tGvkXDWnfI5G8WX6VnsIJ3xLvnfLt56x6Q8UaNbU"
    # Use /storage endpoint to get a URL instead of raw PNG
    url = "https://api.chart-img.com/v2/tradingview/advanced-chart/storage"

    # Fixed payload with only 4 total parameters (3 studies + 1 drawing)
    payload = {
        "symbol": "NASDAQ:NVDA",
        "interval": "1D",
        "theme": "dark",
        "studies": [
            {"name": "Volume", "forceOverlay": True},
            {"name": "Moving Average Exponential", "input": {"length": 21, "source": "close"}},
            {"name": "Moving Average", "input": {"length": 50, "source": "close"}},
        ],
        "drawings": [
            {
                "name": "Long Position",
                "input": {
                    "startDatetime": "2025-01-01T00:00:00.000Z",
                    "entryPrice": 150.00,
                    "stopPrice": 145.00,
                    "targetPrice": 160.00,
                },
            }
        ],
    }

    headers = {"x-api-key": api_key}

    print(f"Testing Chart-IMG API with {len(payload['studies']) + len(payload['drawings'])} parameters...")
    print(f"- Studies: {len(payload['studies'])}")
    print(f"- Drawings: {len(payload['drawings'])}")
    print()

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        print(f"Status: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('content-type')}")

        if resp.status_code in (200, 201):
            # Check if response is an image or JSON
            content_type = resp.headers.get('content-type', '')
            if 'image' in content_type:
                print(f"✅ SUCCESS! Got PNG image directly ({len(resp.content)} bytes)")
                print(f"   First bytes: {resp.content[:20].hex()}")
                return "image_data"
            else:
                try:
                    data = resp.json()
                    chart_url = data.get("url") or data.get("imageUrl") or data.get("image_url")
                    if chart_url:
                        print(f"✅ SUCCESS! Got chart URL:")
                        print(f"   {chart_url[:100]}...")
                        return chart_url
                    else:
                        print(f"❌ Got 200 but no URL in response:")
                        print(f"   {data}")
                except Exception as e:
                    print(f"❌ Could not parse response: {e}")
                    print(f"   Content starts with: {resp.content[:50]}")
        else:
            print(f"❌ ERROR: {resp.text}")

    return None

if __name__ == "__main__":
    asyncio.run(test_chartimg())
