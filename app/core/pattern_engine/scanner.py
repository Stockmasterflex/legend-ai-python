from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.core.pattern_engine.filter import PatternFilter
from app.core.pattern_engine.scoring import PatternScorer


# Pattern priority values (higher = more important)
# Used to resolve when multiple patterns match the same ticker
PATTERN_PRIORITIES = {
    # Premium patterns (100+)
    "VCP": 120,
    "MMU": 120,
    "Cup & Handle": 100,
    "Cup": 100,

    # Strong continuation patterns (60-90)
    "Bull Flag": 85,
    "Flag": 85,
    "High Tight Flag": 90,
    "Pennant": 80,
    "Falling Wedge": 75,
    "Wedge Falling": 75,

    # Triangle patterns (50-70)
    "Ascending Triangle": 60,
    "Triangle Ascending": 60,
    "Symmetrical Triangle": 55,
    "Triangle Symmetrical": 55,
    "Descending Triangle": 50,
    "Triangle Descending": 50,

    # Reversal patterns (40-60)
    "Double Bottom": 65,
    "Triple Bottom": 60,
    "Inverse Head & Shoulders": 70,
    "Head & Shoulders Bottom": 70,

    # Other patterns (30-50)
    "Rectangle": 45,
    "Channel": 40,
    "Rising Wedge": 35,
    "Wedge Rising": 35,

    # Default for unknown patterns
    "_default": 30
}


def get_pattern_priority(pattern_name: str) -> int:
    """Get priority for a pattern by name."""
    # Try exact match first
    if pattern_name in PATTERN_PRIORITIES:
        return PATTERN_PRIORITIES[pattern_name]

    # Try case-insensitive partial matches
    pattern_lower = pattern_name.lower()
    for key, priority in PATTERN_PRIORITIES.items():
        if key != "_default" and key.lower() in pattern_lower:
            return priority

    return PATTERN_PRIORITIES["_default"]


@dataclass
class ScanConfig:
    universe: List[str]  # Ticker list
    interval: str = "1day"
    max_concurrent: int = 10
    apply_filters: bool = True
    apply_scoring: bool = True
    min_score: float = 6.0
    filter_config: Optional[Dict[str, Any]] = None



from app.core.pattern_engine.pipeline import ScanPipeline

class UniverseScanner:
    """Async universe scanner that wires detector, filters, and scoring together."""

    def __init__(self, detector, filter_system: PatternFilter, scorer: PatternScorer):
        self.detector = detector
        self.filter = filter_system
        self.scorer = scorer
        self.pipeline = ScanPipeline()

    async def scan_universe(self, config: ScanConfig) -> Dict[str, Any]:
        """Scan a list of tickers and return ranked results."""
        started = time.perf_counter()
        sem = asyncio.Semaphore(config.max_concurrent)

        async def _run(ticker: str):
            async with sem:
                try:
                    # Use the new pipeline
                    from app.services.market_data import market_data_service
                    price_data = await market_data_service.get_time_series(
                        ticker=ticker,
                        interval=config.interval,
                        outputsize=320,
                    )
                    
                    if not price_data or not price_data.get("c"):
                        return ticker, [], None
                        
                    # Convert to minimal DF for pipeline (it expects DF)
                    # We might need to move conversion logic here or pipeline handles it
                    # Pipeline expects DF.
                    # reusing _to_dataframe from pattern_scanner logic?
                    # Or implement a helper. 
                    # For now minimal conversion:
                    import pandas as pd
                    df = pd.DataFrame({
                        'close': price_data.get('c', []),
                        'high': price_data.get('h', []),
                        'low': price_data.get('l', []),
                        'open': price_data.get('o', []),
                        'volume': price_data.get('v', [])
                    })
                    
                    patterns = await self.pipeline.run(ticker, df)
                    return ticker, patterns, None
                except Exception as exc:  # pragma: no cover - defensive
                    return ticker, [], exc

        tasks = [_run(ticker) for ticker in config.universe]
        raw_results = await asyncio.gather(*tasks)

        aggregated: List[Dict[str, Any]] = []
        errors: Dict[str, str] = {}
        for ticker, patterns, error in raw_results:
            if error:
                errors[ticker] = str(error)
                continue

            # Filtering and Scoring are now part of Pipeline (Stages E, F)
            # But pipeline returns scored patterns.
            # config.apply_filters / apply_scoring checks?
            # Pipeline does it all. We assume config matches pipeline default or pass config to pipeline.run
            
            # The pipeline runs detection, validation, scoring.
            
            for pat in patterns:
                pat.setdefault("ticker", ticker)
                pat.setdefault("symbol", ticker)

            # Keep only the best pattern per ticker (by priority, then score, then confidence)
            if patterns:
                # Need to robustly handle missing keys if pipeline output differs slightly
                best_pattern = max(
                    patterns,
                    key=lambda p: (
                        get_pattern_priority(p.get("pattern", "")),
                        p.get("score", 0.0),
                        p.get("confidence", 0.0)
                    )
                )
                aggregated.append(best_pattern)

        ranked = self.rank_results(aggregated)
        if config.apply_scoring:
            ranked = [p for p in ranked if p.get("score", 0.0) >= config.min_score]

        duration_ms = (time.perf_counter() - started) * 1000
        return {
            "as_of": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "universe_size": len(config.universe),
            "results": ranked,
            "errors": errors,
            "meta": {
                "duration_ms": round(duration_ms, 2),
                "result_count": len(ranked),
            },
        }

    async def scan_ticker(self, ticker: str, interval: str) -> List[Dict[str, Any]]:
        """Deprecated: Use pipeline directly."""
        return [] 


    def rank_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort and rank scan results."""
        if not results:
            return []

        ranked = sorted(
            results,
            key=lambda item: (item.get("score") or 0.0, item.get("confidence") or 0.0),
            reverse=True,
        )
        for idx, item in enumerate(ranked, start=1):
            item.setdefault("rank", idx)
        return ranked
