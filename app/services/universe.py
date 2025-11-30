"""
Universe Scanner Service

Manages stock universe (S&P 500 + NASDAQ 100) and bulk scanning operations.
"""
import httpx
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio

from app.config import get_settings
from app.services.cache import get_cache_service
from app.services.universe_store import universe_store

logger = logging.getLogger(__name__)
settings = get_settings()


class UniverseService:
    """
    Service for managing stock universe and bulk scanning
    """
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
        self.cache = get_cache_service()
        
        # Static NASDAQ 100 tickers (most actively traded)
        self.nasdaq_100 = [
            "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA", "TSLA", 
            "AVGO", "ASML", "COST", "NFLX", "AMD", "PEP", "ADBE", "CSCO",
            "CMCSA", "TMUS", "INTC", "TXN", "QCOM", "INTU", "AMGN", "HON",
            "AMAT", "SBUX", "BKNG", "ISRG", "ADP", "GILD", "VRTX", "ADI",
            "REGN", "LRCX", "MDLZ", "PANW", "MU", "KLAC", "SNPS", "CDNS",
            "PYPL", "MELI", "MAR", "ABNB", "CSX", "ORLY", "NXPI", "CTAS",
            "ADSK", "CHTR", "MNST", "WDAY", "FTNT", "MRVL", "AEP", "PCAR",
            "PAYX", "CPRT", "ROST", "ODFL", "AZN", "FAST", "EA", "VRSK",
            "CTSH", "DXCM", "BKR", "GEHC", "EXC", "KDP", "IDXX", "CSGP",
            "LULU", "XEL", "FANG", "ON", "ANSS", "DDOG", "BIIB", "CRWD",
            "ILMN", "TTWO", "ZS", "WBD", "ENPH", "MDB", "GFS", "ARM",
            "TEAM", "MRNA", "SMCI", "COIN", "ZM", "RIVN", "LCID", "DASH"
        ]
    
    async def get_sp500_tickers(self) -> List[str]:
        """
        Fetch S&P 500 ticker list from Wikipedia
        
        Returns:
            List of S&P 500 ticker symbols
        """
        try:
            # Try cache first
            cache_key = "universe:sp500:tickers"
            cached = await self.cache._get_redis()
            cached_data = await cached.get(cache_key)
            
            if cached_data:
                import json
                tickers = json.loads(cached_data)
                logger.info(f"✅ Loaded {len(tickers)} S&P 500 tickers from cache")
                return tickers
            
            # Fetch from Wikipedia
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            response = await self.client.get(url)
            response.raise_for_status()
            
            # Parse HTML table (simplified - using pandas would be better)
            html = response.text
            
            # Extract tickers from table (they're in first column)
            import re
            # Find all ticker symbols (uppercase letters, 1-5 chars, in table cells)
            pattern = r'<td><a[^>]*>([A-Z]{1,5})</a></td>'
            matches = re.findall(pattern, html)
            
            # Get unique tickers (first ~500 should be SP500)
            tickers = list(set(matches[:520]))  # Get extra to ensure we have 500+
            
            logger.info(f"✅ Fetched {len(tickers)} S&P 500 tickers from Wikipedia")
            
            # Cache for 7 days
            import json
            await cached.setex(cache_key, 7 * 24 * 3600, json.dumps(tickers))
            
            return tickers
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch S&P 500 tickers: {e}")
            # Return static fallback list of top 100 SP500
            return [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B",
                "LLY", "V", "UNH", "XOM", "JPM", "JNJ", "WMT", "MA", "PG",
                "AVGO", "HD", "MRK", "CVX", "COST", "ABBV", "KO", "PEP",
                "ADBE", "MCD", "CRM", "CSCO", "TMO", "ACN", "NFLX", "ABT",
                "WFC", "DHR", "BAC", "NKE", "TXN", "DIS", "PM", "VZ",
                "QCOM", "INTC", "INTU", "ORCL", "AMD", "CMCSA", "RTX", "UNP",
                "HON", "AMGN", "NEE", "COP", "IBM", "LOW", "CAT", "SPGI",
                "BA", "GE", "T", "AXP", "BLK", "DE", "AMAT", "SBUX",
                "MDT", "GILD", "ELV", "TJX", "MS", "BKNG", "ISRG", "PLD",
                "SYK", "MMC", "CI", "VRTX", "ADI", "REGN", "ZTS", "C",
                "LRCX", "GS", "AMT", "CB", "SO", "PGR", "MO", "ETN",
                "BMY", "DUK", "BSX", "FI", "NOC", "SCHW", "MDLZ", "PANW"
            ]
    
    async def get_nasdaq100_tickers(self) -> List[str]:
        """
        Get NASDAQ 100 ticker list (static for now)
        
        Returns:
            List of NASDAQ 100 ticker symbols
        """
        return self.nasdaq_100
    
    async def get_full_universe(self, dedupe: bool = True) -> List[Dict[str, Any]]:
        """
        Get combined universe of S&P 500 + NASDAQ 100
        
        Args:
            dedupe: Remove duplicates (default True)
            
        Returns:
            List of ticker dictionaries with metadata
        """
        try:
            seeded = await universe_store.get_all()
            if seeded:
                universe = []
                seen = set()
                for meta in seeded.values():
                    symbol = meta.get("symbol")
                    if not symbol:
                        continue
                    if symbol in seen and dedupe:
                        continue
                    seen.add(symbol)
                    universe.append(
                        {
                            "ticker": symbol,
                            "source": meta.get("universe", "SP500"),
                            "sector": meta.get("sector"),
                            "industry": meta.get("industry"),
                            "added_date": datetime.utcnow().isoformat(),
                        }
                    )
                if universe:
                    return universe

            sp500 = await self.get_sp500_tickers()
            nasdaq100 = await self.get_nasdaq100_tickers()
            
            # Combine and create ticker objects
            universe = []
            seen = set()
            
            # Add S&P 500
            for ticker in sp500:
                if ticker and (ticker not in seen or not dedupe):
                    universe.append({
                        "ticker": ticker,
                        "source": "SP500",
                        "added_date": datetime.utcnow().isoformat()
                    })
                    seen.add(ticker)
            
            # Add NASDAQ 100
            for ticker in nasdaq100:
                if ticker and (ticker not in seen or not dedupe):
                    universe.append({
                        "ticker": ticker,
                        "source": "NASDAQ100",
                        "added_date": datetime.utcnow().isoformat()
                    })
                    seen.add(ticker)
            
            logger.info(f"✅ Built universe: {len(universe)} tickers (SP500: {len(sp500)}, NASDAQ100: {len(nasdaq100)})")
            
            return universe
            
        except Exception as e:
            logger.error(f"❌ Failed to build universe: {e}")
            return []
    
    async def scan_universe(
        self,
        min_score: float = 7.0,
        max_results: int = 20,
        pattern_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Scan full universe for pattern setups
        
        This is rate-limited and cached to avoid API abuse.
        
        Args:
            min_score: Minimum pattern score (default 7.0)
            max_results: Maximum results to return (default 20)
            pattern_types: Filter by pattern types (e.g., ["VCP", "Cup & Handle"])
            
        Returns:
            List of top pattern setups sorted by score
        """
        try:
            # Check if we have a recent scan cached
            cache_key = f"universe:scan:min{min_score}"
            cached = await self.cache._get_redis()
            cached_scan = await cached.get(cache_key)

            if cached_scan:
                import json
                results = json.loads(cached_scan)
                # Don't use cached empty results - they might indicate a failed scan
                if results and len(results) > 0:
                    logger.info(f"✅ Loaded cached universe scan: {len(results)} results")
                    return results[:max_results]
                else:
                    # Invalidate empty cache and run fresh scan
                    logger.warning("⚠️ Cached scan was empty, running fresh scan...")
                    await cached.delete(cache_key)
            
            logger.info("🔍 Starting universe scan... (this may take a while)")

            # Get universe
            universe = await self.get_full_universe()
            logger.info(f"📊 Scanning {len(universe)} tickers from universe (SP500 + NASDAQ100)")

            # Scan in batches to avoid overwhelming APIs
            from app.core.pattern_detector import PatternDetector
            from app.services.market_data import market_data_service

            detector = PatternDetector()
            results = []
            batch_size = 10
            delay_between_batches = 1  # seconds

            for i in range(0, len(universe), batch_size):  # Scan ALL tickers in universe
                batch = universe[i:i+batch_size]
                logger.info(f"📊 Scanning batch {i//batch_size + 1} ({len(batch)} tickers)...")
                
                # Process batch
                for item in batch:
                    ticker = item["ticker"]
                    
                    try:
                        # Try cache first
                        cached_pattern = await self.cache.get_pattern(ticker, "1day")
                        
                        if cached_pattern:
                            # Use cached result
                            from app.core.pattern_detector import PatternResult
                            from datetime import datetime
                            if isinstance(cached_pattern.get("timestamp"), str):
                                cached_pattern["timestamp"] = datetime.fromisoformat(cached_pattern["timestamp"])
                            
                            pattern_result = PatternResult(**cached_pattern)
                        else:
                            # Fetch and analyze (uses smart fallback)
                            price_data = await market_data_service.get_time_series(
                                ticker=ticker,
                                interval="1day",
                                outputsize=500
                            )

                            if not price_data:
                                continue

                            # Get SPY for RS calculation (uses smart fallback)
                            spy_data = await market_data_service.get_time_series("SPY", "1day", 500)
                            
                            # Analyze
                            pattern_result = await detector.analyze_ticker(ticker, price_data, spy_data)
                            
                            if pattern_result:
                                # Cache result
                                await self.cache.set_pattern(ticker, "1day", pattern_result.to_dict())
                        
                        # Add to results if meets criteria
                        if pattern_result and pattern_result.score >= min_score:
                            if pattern_types is None or pattern_result.pattern in pattern_types:
                                results.append({
                                    "ticker": ticker,
                                    "pattern": pattern_result.pattern,
                                    "score": pattern_result.score,
                                    "entry": pattern_result.entry,
                                    "stop": pattern_result.stop,
                                    "target": pattern_result.target,
                                    "risk_reward": pattern_result.risk_reward,
                                    "current_price": pattern_result.current_price,
                                    "source": item["source"],
                                    "chart_url": pattern_result.chart_url
                                })
                                
                                logger.info(f"✅ {ticker}: {pattern_result.pattern} ({pattern_result.score}/10)")
                        
                    except Exception as e:
                        logger.debug(f"⚠️ Error scanning {ticker}: {e}")
                        continue
                
                # Delay between batches
                if i + batch_size < len(universe):
                    await asyncio.sleep(delay_between_batches)
            
            # Sort by score descending
            results.sort(key=lambda x: x["score"], reverse=True)

            logger.info(f"✅ Universe scan complete: {len(results)} setups found (min score: {min_score})")

            # Only cache non-empty results (avoid caching failed/empty scans)
            if results and len(results) > 0:
                import json
                await cached.setex(cache_key, 24 * 3600, json.dumps(results))
                logger.info(f"📦 Cached {len(results)} scan results for 24 hours")
            else:
                logger.warning("⚠️ No results to cache (no patterns found meeting criteria)")

            return results[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Universe scan failed: {e}")
            return []


# Global instance
universe_service = UniverseService()
