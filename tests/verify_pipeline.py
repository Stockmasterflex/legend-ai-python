
import asyncio
import pandas as pd
import numpy as np
from app.core.pattern_engine.pipeline import ScanPipeline

async def verify():
    print("Initializing ScanPipeline...")
    pipeline = ScanPipeline()
    
    # Create mock data (Uptrend)
    dates = pd.date_range("2024-01-01", periods=100)
    prices = np.linspace(100, 150, 100) + np.random.normal(0, 1, 100)
    # Add volume
    volume = np.random.randint(1000000, 2000000, 100)
    
    df = pd.DataFrame({
        "close": prices,
        "high": prices + 1,
        "low": prices - 1,
        "open": prices,
        "volume": volume
    }, index=dates)
    
    print(f"Running pipeline on mock data ({len(df)} bars)...")
    results = await pipeline.run("MOCK", df)
    
    print(f"Pipeline returned {len(results)} pattern candidates.")
    for p in results:
        print(f" - {p.get('pattern')} Score: {p.get('score')} Grade: {p.get('grade')}")
        print(f"   Components: {p.get('score_components')}")

if __name__ == "__main__":
    asyncio.run(verify())
